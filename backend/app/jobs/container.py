import logging
import uuid
from pathlib import Path

import docker
from docker.errors import DockerException
from kubernetes import client as k8s_client
from kubernetes import config as k8s_config

DOCKER_SOCK = "unix://var/run/docker.sock"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContainerError(Exception):
    pass


def run_container(
    image: str,
    command: str,
    entrypoint: str | None = None,
    remove=True,
    ignore_errors=False,
) -> str:
    namespace_path = Path("/var/run/secrets/kubernetes.io/serviceaccount/namespace")

    if namespace_path.exists():
        namespace = namespace_path.read_text().strip()
        k8s_config.load_incluster_config()
        v1 = k8s_client.CoreV1Api()

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

        logger.info(f"Creating Kubernetes Pod: {pod_name} in namespace: {namespace}")
        v1.create_namespaced_pod(namespace=namespace, body=pod_manifest)

        # Wait for the Pod to complete
        while True:
            pod_status = v1.read_namespaced_pod_status(pod_name, namespace)
            logger.info(f"Pod {pod_name} status: {pod_status.status.phase}")
            if pod_status.status.phase in ["Succeeded", "Failed"]:
                break

        # Get the logs from the Pod
        logs = v1.read_namespaced_pod_log(pod_name, namespace)
        logger.info(f"Logs from Pod {pod_name}: {logs}")

        # Clean up the Pod
        v1.delete_namespaced_pod(pod_name, namespace)
        logger.info(f"Deleted Kubernetes Pod: {pod_name}")

        return logs
    else:
        try:
            docker_client = docker.DockerClient(base_url=DOCKER_SOCK)
        except DockerException as e:
            logger.error(f"Failed to connect to Docker: {e}")
            raise ContainerError(f"Failed to connect to Docker: {e}")

        container_name = f"weakspotter-{uuid.uuid4()}"
        logger.info(
            f'Running Docker container: {container_name} with image "{image}" and command "{command}"'
        )

        try:
            container = docker_client.containers.run(
                image=image,
                command=command,
                name=container_name,
                entrypoint=entrypoint,
                stdout=True,
                stderr=True,
            )
        except DockerException as e:
            logger.error(f"Error running Docker container: {e}")
            if not ignore_errors:
                raise ContainerError(f"Failed to run Docker container: {e}")
            logger.info("Ignoring error.")

        logging.info(f"Reading logs of {container_name}")
        container = docker_client.containers.get(container_name)
        result = container.logs().decode("utf-8")

        if remove:
            container.remove()
            logger.info(f"Removed Docker container: {container_name}")

        return result
