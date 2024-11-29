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
            print("Aucun domaine spécifié.")
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
            # Exécuter la commande en temps réel
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            output = []
            # Lire la sortie ligne par ligne
            for line in process.stdout:
                print(line.strip())  # Affiche chaque ligne de la sortie standard
                output.append(line.strip())

            for line in process.stderr:
                print(f"ERREUR : {line.strip()}")  # Affiche chaque ligne de la sortie d'erreur

            process.wait()  # Attendre la fin de l'exécution

            # Vérifier si le processus s'est terminé correctement
            if process.returncode != 0:
                print(f"theHarvester a échoué avec le code : {process.returncode}")
                return None

            # Retourner la sortie complète après exécution
            return EmailHarvesterJob.parse_theharvester_output("\n".join(output))
        except FileNotFoundError:
            print("Python ou theHarvester est introuvable dans l'environnement.")
            return None

    @staticmethod
    def parse_theharvester_output(output: str) -> dict:
        """Analyse la sortie de theHarvester et extrait les emails."""
        emails = set()
        lines = output.splitlines()
        print(lines)
        for line in lines:
            if "@" in line and line.strip().startswith("-"):
                # Format d'exemple : "- email@example.com"
                email = line.strip().split("-")[-1].strip()
                if "@" in email:
                    emails.add(email)

        return {"emails": list(emails)}
