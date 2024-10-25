from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

def create_result(status, title, description):
    """Génère un objet de résultat avec le statut, le titre et la description donnés."""
    return {
        "status": status,
        "title": title,
        "description": description
    }

def check_connectivity(url):
    """Vérifie si le site est accessible."""
    try:
        curl_result = subprocess.run(['curl', '-Is', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if curl_result.returncode == 0:
            return create_result("correct", "Connectivité", f"{url} est accessible.")
        else:
            return create_result("critical", "Connectivité", f"{url} n'est pas accessible.")
    except Exception as e:
        return create_result("critical", "Erreur de Connectivité", str(e))

def check_https(url):
    """Vérifie si le site est accessible via HTTPS."""
    if not url.startswith("http://") and not url.startswith("https://"):
        # Ajouter https par défaut si aucun protocole n'est fourni
        https_url = f"https://{url}"
    elif url.startswith("http://"):
        # Convertir http en https
        https_url = url.replace("http://", "https://")
    else:
        https_url = url

    try:
        curl_result = subprocess.run(['curl', '-Is', https_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if curl_result.returncode == 0:
            return create_result("correct", "HTTPS", f"{https_url} est accessible via HTTPS.")
        else:
            return create_result("critical", "HTTPS", f"{https_url} n'est pas accessible via HTTPS. Veuillez activer HTTPS pour sécuriser la connexion.")
    except Exception as e:
        return create_result("critical", "Erreur HTTPS", str(e))

def perform_analysis(url):
    score = 100
    results = {
        "status": "success",
        "score": score,
        "details": []
    }
    
    # Analyse de la connectivité
    connectivity_result = check_connectivity(url)
    results["details"].append(connectivity_result)

    # Vérification de la disponibilité HTTPS
    https_result = check_https(url)
    results["details"].append(https_result)

    # Ajuster le score en fonction des résultats
    if connectivity_result["status"] == "critical":
        score = 0
        results["status"] = "failure"
    if https_result["status"] == "critical":
        score -= 50  # Réduction plus significative pour l'absence de HTTPS
        if score < 0: 
            score = 0

    results["score"] = score

    return results

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.json.get('url')
    if url:
        # Effectuer une série d'analyses sur l'URL
        analysis_results = perform_analysis(url)
        return jsonify(analysis_results)
    
    # Retourner une erreur si aucune URL n'est fournie
    return jsonify(create_result("failure", "Erreur d'entrée", "Aucune URL fournie.")), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
