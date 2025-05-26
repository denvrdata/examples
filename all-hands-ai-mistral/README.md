
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


### 3. Serve the Model

Start the server for the `Devstral-Small-2505` model:

```bash
screen -S vllm
vllm serve mistralai/Devstral-Small-2505 --tokenizer_mode mistral --config_format mistral --load_format mistral --tool-call-parser mistral --enable-auto-tool-choice --tensor-parallel-size 8
```



### 4. Run OpenHands App in Docker

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

### 5. Setup Docker to export  all metrics

Enable Docker metrics export for Prometheus

`/etc/docker/daemon.json`

```
{
  "metrics-addr": "127.0.0.1:9323"
}
```

`service docker restart`

### 6. Launch the Prometheus stack to monitor

`docker compose up -d`
