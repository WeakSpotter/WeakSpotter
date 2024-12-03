import uuid

import docker

DOCKER_SOCK = "unix:///var/run/docker.sock"


def sanitize_url(url: str) -> str:
    if not url.startswith("http"):
        url = f"https://{url}"
    return url


def add_data(scan, key, value):
    data = scan.data_dict
    data[key] = value
    scan.data_dict = data


def run_container(image: str, command: str, entrypoint: str | None = None) -> str:
    client = docker.DockerClient(base_url=DOCKER_SOCK)

    container_name = f"weakspotter-{uuid.uuid4()}"

    result = client.containers.run(
        image, command, name=container_name, entrypoint=entrypoint
    ).decode("utf-8")
    client.containers.get(container_name).remove()
    return result
