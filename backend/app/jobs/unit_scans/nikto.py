import subprocess
from app.jobs.job import Job
from app.models.scan import Scan


class NiktoJob(Job):
    def __init__(self):
        super().__init__("Nikto Scanner", "nikto_scan", self.perform_scan)

    @staticmethod
    def perform_scan(scan: Scan) -> dict:
        """Effectue un scan avec Nikto sur un domaine ou une IP."""
        domain = scan.data_dict.get("domain")
        if not domain:
            print("Aucun domaine spécifié.")
            return None

        # Commande pour exécuter Nikto
        command = [
            "nikto",
            "-h",
            domain,
            "-o",
            "/tmp/nikto_report.txt",  # Chemin pour stocker le rapport temporaire
            "-Format",
            "txt"
        ]

        print(f"Commande exécutée : {' '.join(command)}")

        try:
            # Exécuter la commande
            subprocess.run(command, check=True, text=True)

            # Lire le contenu du rapport généré
            with open("/tmp/nikto_report.txt", "r") as report_file:
                report_content = report_file.read()
            print(report_content)
            return NiktoJob.parse_nikto_output(report_content)
        except subprocess.CalledProcessError as e:
            print(f"Nikto scan échoué pour le domaine {domain}\nErreur : {e}")
            return None
        except FileNotFoundError:
            print("L'outil Nikto n'est pas installé.")
            return None

    @staticmethod
    def parse_nikto_output(output: str) -> dict:
        """Analyse le rapport Nikto et extrait les informations utiles."""
        findings = []
        for line in output.splitlines():
            if line.startswith("+"):  # Les résultats importants de Nikto commencent par "+"
                findings.append(line.strip())

        return {"nikto_findings": findings}
