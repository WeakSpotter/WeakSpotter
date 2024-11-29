import subprocess

from app.jobs.job import Job
from app.models.scan import Scan
from pathlib import Path


class EmailHarvesterJob(Job):
    def __init__(self):
        super().__init__("Email Harvester", "email_harvester", self.harvest_emails)

    @staticmethod
    def harvest_emails(scan: Scan) -> dict:
        """Effectue un scan de récolte d'emails avec theHarvester."""
        domain = scan.data_dict.get("domain")
        if not domain:
            return None

        # Chemin absolu vers theHarvester.py
        theharvester_path = Path("/opt/theHarvester/theHarvester.py")

        # Vérification si theHarvester est bien installé
        if not theharvester_path.exists():
            print("theHarvester n'est pas installé ou le chemin est incorrect.")
            return None

        # Commande pour exécuter theHarvester
        command = [
            "python3",
            str(theharvester_path),
            "-d",
            domain,
            "-l",
            "100",
            "-b",
            "crtsh"
        ]

        print(f"Commande exécutée : {' '.join(command)}")

        try:
            result = subprocess.check_output(command, shell=True).decode("utf-8")
            print(result)
            return EmailHarvesterJob.parse_theharvester_output(result)
        except subprocess.CalledProcessError as e:
            print(f"theHarvester scan failed for domain {domain}\nError: {e}")
            return None

    @staticmethod
    def parse_theharvester_output(output: str) -> dict:
        """Analyse la sortie de theHarvester et extrait les emails."""
        emails = set()
        lines = output.splitlines()

        for line in lines:
            if "@" in line and line.strip().startswith("-"):
                # Format d'exemple : "- email@example.com"
                email = line.strip().split("-")[-1].strip()
                if "@" in email:
                    emails.add(email)

        return {"emails": list(emails)}
