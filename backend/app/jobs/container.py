import uuid
from pathlib import Path

import docker
from kubernetes import client, config

DOCKER_SOCK = "unix://var/run/docker.sock"


def run_container(image: str, command: str, entrypoint: str | None = None) -> str:
    namespace = Path("/var/run/secrets/kubernetes.io/serviceaccount/namespace")

    kubernetes_enabled = False

    if namespace.exists():
        kubernetes_enabled = True
        namespace = namespace.read_text().strip()

    if kubernetes_enabled:
        config.load_incluster_config()

        v1 = client.CoreV1Api()

        pod_name = f"weakspotter-{uuid.uuid4()}"
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": pod_name, "namespace": namespace},
            "spec": {
                "containers": [
                    {
                        "name": "container",
                        "image": image,
                        "command": [entrypoint] if entrypoint else ["/bin/sh", "-c"],
                        "args": [command],
                    }
                ],
                "restartPolicy": "Never",
            },
        }

        v1.create_namespaced_pod(namespace=namespace, body=pod_manifest)

        # Wait for the Pod to complete
        while True:
            pod_status = v1.read_namespaced_pod_status(pod_name, namespace)
            if pod_status.status.phase in ["Succeeded", "Failed"]:
                break

        # Get the logs from the Pod
        logs = v1.read_namespaced_pod_log(pod_name, namespace)

        # Clean up the Pod
        v1.delete_namespaced_pod(pod_name, namespace)

        return logs
    else:
        client = docker.DockerClient(base_url=DOCKER_SOCK)

        container_name = f"weakspotter-{uuid.uuid4()}"

        result = client.containers.run(
            image, command, name=container_name, entrypoint=entrypoint
        ).decode("utf-8")
        client.containers.get(container_name).remove()
        return result
