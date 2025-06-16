# G4 API - Open WebUI Pipelines

docker run -d -p 9099:9099 --add-host=host.docker.internal:host-gateway -e PIPELINES_URLS="https://raw.githubusercontent.com/g4-api/g4-webui-pipelines/main/pipelines/echo_pipeline.yaml" -v pipelines:/app/pipelines --name pipelines --restart always ghcr.io/open-webui/pipelines:main


# Tools

curl https://sh.rustup.rs -sSf | sh
refreshenv
pip install pydantic==2.7.1


Invoke-WebRequest -Uri https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe -OutFile rustup-init.exe
.\rustup-init.exe -y
pip install pydantic==2.7.1
