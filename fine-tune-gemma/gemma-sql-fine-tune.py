import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    AutoModelForImageTextToText,
    BitsAndBytesConfig,
    pipeline
)
from huggingface_hub import login
from trl import SFTTrainer, SFTConfig
from peft import LoraConfig, PeftModel
import re
from random import randint

# Login to Hugging Face Hub

# System message and prompt template
system_message = """You are a text to SQL query translator. Users will ask you questions in English and you will generate a SQL query based on the provided SCHEMA."""
user_prompt = """Given the <USER_QUERY> and the <SCHEMA>, generate the corresponding SQL command to retrieve the desired data, considering the query's syntax, semantics, and schema constraints.

<SCHEMA>
{context}
</SCHEMA>

<USER_QUERY>
{question}
</USER_QUERY>
"""

def create_conversation(sample):
    return {
        "messages": [
            {"role": "user", "content": user_prompt.format(question=sample["sql_prompt"], context=sample["sql_context"])} ,
            {"role": "assistant", "content": sample["sql"]}
        ]
    }

# Load and preprocess dataset
dataset = load_dataset("philschmid/gretel-synthetic-text-to-sql", split="train")
dataset = dataset.shuffle().select(range(12500))
dataset = dataset.map(create_conversation, remove_columns=dataset.features, batched=False)
dataset = dataset.train_test_split(test_size=2500/12500)

# Model setup
model_id = "google/gemma-3-1b-pt"
model_class = AutoModelForCausalLM if model_id == "google/gemma-3-1b-pt" else AutoModelForImageTextToText

torch_dtype = torch.bfloat16 if torch.cuda.get_device_capability()[0] >= 8 else torch.float16

model_kwargs = dict(
    attn_implementation="eager",
    torch_dtype=torch_dtype,
    device_map="auto",
    quantization_config=BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type='nf4',
        bnb_4bit_compute_dtype=torch_dtype,
        bnb_4bit_quant_storage=torch_dtype,
    )
)

model = model_class.from_pretrained(model_id, **model_kwargs)
tokenizer = AutoTokenizer.from_pretrained("google/gemma-3-1b-it")

# PEFT config
peft_config = LoraConfig(
    lora_alpha=16,
    lora_dropout=0.05,
    r=16,
    bias="none",
    target_modules="all-linear",
    task_type="CAUSAL_LM",
    modules_to_save=["lm_head", "embed_tokens"]
)

# Training config
args = SFTConfig(
    output_dir="gemma-text-to-sql",
    max_seq_length=512,
    packing=True,
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    gradient_checkpointing=True,
    optim="adamw_torch_fused",
    logging_steps=10,
    save_strategy="epoch",
    learning_rate=2e-4,
    fp16=torch_dtype == torch.float16,
    bf16=torch_dtype == torch.bfloat16,
    max_grad_norm=0.3,
    warmup_ratio=0.03,
    lr_scheduler_type="constant",
    push_to_hub=True,
    report_to="tensorboard",
    dataset_kwargs={
        "add_special_tokens": False,
        "append_concat_token": True
    }
)

trainer = SFTTrainer(
    model=model,
    args=args,
    train_dataset=dataset["train"],
    peft_config=peft_config,
    processing_class=tokenizer
)

# Train model
trainer.train()
trainer.save_model()

# Clean up
del model
del trainer
torch.cuda.empty_cache()

# Merge adapters into base model
model = model_class.from_pretrained(model_id, low_cpu_mem_usage=True)
peft_model = PeftModel.from_pretrained(model, args.output_dir)
merged_model = peft_model.merge_and_unload()
merged_model.save_pretrained("merged_model", safe_serialization=True, max_shard_size="2GB")
tokenizer.save_pretrained("merged_model")

# Inference test
model = model_class.from_pretrained("gemma-text-to-sql", device_map="auto", torch_dtype=torch_dtype, attn_implementation="eager")
tokenizer = AutoTokenizer.from_pretrained("gemma-text-to-sql")
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

rand_idx = randint(0, len(dataset["test"]))
test_sample = dataset["test"][rand_idx]
stop_token_ids = [tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids("<end_of_turn>")]
prompt = pipe.tokenizer.apply_chat_template(test_sample["messages"][:2], tokenize=False, add_generation_prompt=True)

outputs = pipe(prompt, max_new_tokens=256, do_sample=False, temperature=0.1, top_k=50, top_p=0.1, eos_token_id=stop_token_ids, disable_compile=True)

print(f"Context:\n", re.search(r'<SCHEMA>\n(.*?)\n</SCHEMA>', test_sample['messages'][0]['content'], re.DOTALL).group(1).strip())
print(f"Query:\n", re.search(r'<USER_QUERY>\n(.*?)\n</USER_QUERY>', test_sample['messages'][0]['content'], re.DOTALL).group(1).strip())
print(f"Original Answer:\n{test_sample['messages'][1]['content']}")
print(f"Generated Answer:\n{outputs[0]['generated_text'][len(prompt):].strip()}")

