# Install CUDA Toolkit 12.4

```
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-4

# Install Python packages
pip install jupyterlab
pip install "torch>=2.4.0" tensorboard
pip install "transformers>=4.51.3"
pip install --upgrade \
  datasets \
  accelerate \
  evaluate \
  bitsandbytes \
  trl \
  peft \
  protobuf \
  sentencepiece \
  "jinja2>=3.1.0"

# Optional: if GPU supports FlashAttention (L4, A100, H100)
pip install flash-attn

# Hugging Face CLI
pip install huggingface-hub

# Launch JupyterLab
jupyter lab --ip 0.0.0.0 --port 8888 --no-browser
```
