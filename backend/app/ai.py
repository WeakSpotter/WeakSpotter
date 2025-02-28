import requests

BASE_URL = "https://ai-cve.weakspotter.ozeliurs.com"
HEADERS = {
    "Authorization": "EaOkzu7Bmd9wV050o3-7A8LfjqbKEDcf1g2wpgP4EDQ"  # TODO: this is raciste, need to remove
}


def create_custom_vulnerability(description: str):
    """
    Envoie une requête POST à l'endpoint /vulnerabilities/custom pour créer ou retourner
    une vulnérabilité personnalisée basée sur la description fournie.

    Exemple d'utilisation :
      result = create_custom_vulnerability("Description de la vulnérabilité")
      print(json.dumps(result, indent=4, ensure_ascii=False))
    """
    url = f"{BASE_URL}/add_custom_vulnerability"
    payload = {"text": description}
    headers = {"Content-Type": "application/json", **HEADERS}
    print(f"Envoi de la requête POST à {url} avec le payload {payload}")
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return None
