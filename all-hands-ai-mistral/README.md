
## Setup Instructions

###  Install `vllm`
Upgrade `vllm` to the latest version:

```bash
pip install vllm --upgrade
pip install --upgrade pyopenssl
````

###  Verify `mistral_common` Installation

Check the installed version of `mistral_common`:

```bash
python -c "import mistral_common; print(mistral_common.__version__)"
```


###  Serve the Model

Start the server for the `Devstral-Small-2505` model:

```bash
screen -S vllm
vllm serve mistralai/Devstral-Small-2505 --tokenizer_mode mistral --config_format mistral --load_format mistral --tool-call-parser mistral --enable-auto-tool-choice --tensor-parallel-size 8
```


### Setup Docker to export  all metrics

Enable Docker metrics export for Prometheus

`/etc/docker/daemon.json`

```
{
  "metrics-addr": "127.0.0.1:9323"
}
```

`service docker restart`

###  Launch the Prometheus stack to monitor

`docker compose up -d`

###  Run OpenHands App in Docker

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

Open the OpenHands Web session at `http://<IP>:3001`

![image](https://github.com/user-attachments/assets/ce63605a-eb9d-4066-8771-a3134ce898a2)

Click on Advanced Setting and point to your self hosted LLM

![image](https://github.com/user-attachments/assets/94424d7c-74cd-4880-a9db-49a273a6c29e)

Start the new conversion to begin your "Vibe Coding"

![image](https://github.com/user-attachments/assets/d3ab6749-5722-4dab-b7a0-8c8e63852ebc)


