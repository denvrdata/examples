
## Setup Instructions

### 1. Install `vllm`
Upgrade `vllm` to the latest version:

```bash
pip install vllm --upgrade
pip install --upgrade pyopenssl
````

### 2. Verify `mistral_common` Installation

Check the installed version of `mistral_common`:

```bash
python -c "import mistral_common; print(mistral_common.__version__)"
```

### 3. Run Docker with `vllm`

Run the Docker container using NVIDIA GPUs:

```bash
docker run --runtime nvidia --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HUGGING_FACE_HUB_TOKEN=<secret>" \
    -p 8000:8000 \
    --ipc=host \
    vllm/vllm-openai:latest \
    --model mistralai/Mistral-7B-v0.1
```

### 4. Serve the Model

Start the server for the `Devstral-Small-2505` model:

```bash
vllm serve mistralai/Devstral-Small-2505 --tokenizer_mode mistral --config_format mistral --load_format mistral --tool-call-parser mistral --enable-auto-tool-choice --tensor-parallel-size 8
```



### 5. Run OpenHands App in Docker

Start the OpenHands app in a Docker container:

```bash
docker run -it --rm --pull=always \
    -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:0.38-nikolaik \
    -e LOG_ALL_EVENTS=true \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v ~/.openhands-state:/.openhands-state \
    -p 3001:3000 \
    --add-host host.docker.internal:host-gateway \
    --name openhands-app \
    docker.all-hands.dev/all-hands-ai/openhands:0.38
```

### 6. Setup Prometheus to capture all metrics

Enable Docker metrics export for Prometheus

`/etc/docker/daemon.json`

```
{
  "metrics-addr": "127.0.0.1:9323"
}
```

Restart docker service

```
docker run --name my-prometheus \
    --mount type=bind,source=./prometheus.yml,destination=/etc/prometheus/prometheus.yml \
    -p 9090:9090 \
    --add-host host.docker.internal=host-gateway \
    prom/prometheus
```