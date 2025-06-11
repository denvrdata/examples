
# From Base Image of Ubuntu 22

```
export distro=ubuntu2204
export arch=x86_64
wget https://developer.download.nvidia.com/compute/cuda/repos/$distro/$arch/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
wget https://developer.download.nvidia.com/compute/cuda/repos/$distro/$arch/cuda-archive-keyring.gpg
sudo mv cuda-archive-keyring.gpg /usr/share/keyrings/cuda-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/cuda-archive-keyring.gpg] https://developer.download.nvidia.com/compute/cuda/repos/$distro/$arch/ /" \
    | tee /etc/apt/sources.list.d/cuda-$distro-$arch.list

sudo apt install cuda-drivers-550
```

# Steps for Pre-installed CUDA 12.4 driver Image

```
export distro=ubuntu2204
export arch=x86_64
wget https://developer.download.nvidia.com/compute/cuda/repos/$distro/$arch/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-4
```

# Install Python packages
```
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

```

# Launch JupyterLab (Optional)
```
jupyter lab --ip 0.0.0.0 --port 8888 --no-browser
```
