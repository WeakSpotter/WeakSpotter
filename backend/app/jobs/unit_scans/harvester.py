import docker
from app.jobs.job import Job
from app.jobs.tools import run_container
from app.models.scan import Scan


class EmailHarvesterJob(Job):
    def __init__(self):
        super().__init__("Email Harvester", "email_harvester", self.harvest_emails)

    @staticmethod
    def harvest_emails(scan: Scan) -> dict:
        """Performs an email harvesting scan with theHarvester."""
        domain = scan.data_dict.get("domain")

        if not domain:
            print("No domain specified.")
            return {}

        try:
            result = run_container(
                "ghcr.io/ozeliurs/ozeliurs/theharvester",
                f"-d {domain} -l 100 -b crtsh",
                entrypoint="/root/.local/bin/theHarvester",
            )
            return EmailHarvesterJob.parse_theharvester_output(result)
        except docker.errors.DockerException as e:
            print(f"Erreur lors de l'exécution du conteneur Docker: {e}")
            return None

    @staticmethod
    def parse_theharvester_output(output: str) -> dict:
        """Parses the output of theHarvester and extracts emails."""
        emails = set()
        lines = output.splitlines()
        print(lines)
        for line in lines:
            if "@" in line and line.strip().startswith("-"):
                # Example format: "- email@example.com"
                email = line.strip().split("-")[-1].strip()
                if "@" in email:
                    emails.add(email)

        return {"emails": list(emails)}
