import subprocess

from app.jobs.job import Job
from app.models.scan import Scan
from pathlib import Path


class CMSmapJob(Job):
    def __init__(self):
        super().__init__("CMSmap", "cmsmap_scan", self.perform_scan)

    @staticmethod
    def perform_scan(scan: Scan) -> dict:
        """Scanne un site CMS avec CMSmap."""
        domain = scan.data_dict.get("domain")
        if not domain:
            print("Aucun domaine spécifié.")
            return None

        # Commande CMSmap
        command = ["cmsmap", domain]  # Correction ici


        print(f"Commande exécutée : {' '.join(command)}")

        try:
            result = subprocess.check_output(command, text=True)
            print(f"Résultat brut :\n{result}")
            return CMSmapJob.parse_cmsmap_output(result)
        except subprocess.CalledProcessError as e:
            print(f"CMSmap scan échoué pour le domaine {domain}\nErreur : {e}")
            return None
        except FileNotFoundError:
            print("L'outil CMSmap n'est pas installé.")
            return None

    @staticmethod
    def parse_cmsmap_output(output: str) -> dict:
        """Analyse la sortie de CMSmap."""
        findings = []
        for line in output.splitlines():
            if "[+]" in line:  # Les résultats importants commencent souvent par "[+]"
                findings.append(line.strip())

        return {"cmsmap_findings": findings}
