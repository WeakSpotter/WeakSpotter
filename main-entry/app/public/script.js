// Gérer la soumission du formulaire sur la page d'accueil
document.getElementById("auditForm")?.addEventListener("submit", function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const url = formData.get("url");

    // Masquer le message d'erreur au cas où il est visible
    document.getElementById("errorMessage").classList.add("hidden");
    document.getElementById("loading").style.display = "block";
    document.getElementById("auditForm").classList.add("hidden");

    console.log("Envoi de la requête d'analyse pour l'URL :", url);

    fetch("/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
    })
    .then(response => {
        console.log("Statut de la réponse :", response.status);
        return response.json();
    })
    .then(data => {
        console.log("Données reçues :", data);

        // Si l'URL est atteignable, rediriger vers la page de résultats
        if (data.status === "success") {
            localStorage.setItem("analysisResult", JSON.stringify(data));
            window.location.href = "/analyze";
        } else {
            // Afficher un message d'erreur si l'URL n'est pas accessible
            document.getElementById("loading").style.display = "none";
            document.getElementById("auditForm").classList.remove("hidden");
            document.getElementById("errorMessage").classList.remove("hidden");
        }
    })
    .catch(error => {
        console.error("Erreur lors de l'envoi de la requête :", error);
        // Réafficher le formulaire et cacher l'animation en cas d'erreur
        document.getElementById("loading").style.display = "none";
        document.getElementById("auditForm").classList.remove("hidden");
        document.getElementById("errorMessage").classList.remove("hidden");
    });
});




// Afficher le résultat sur la page d'analyse
if (window.location.pathname === "/analyze") {
    const resultContainer = document.getElementById("detailed-results");

    try {
        // Récupérer le résultat stocké précédemment
        const result = JSON.parse(localStorage.getItem("analysisResult"));
        console.log(result);

        // Mise à jour du score de sécurité avec le graphique
        if (result && result.score !== undefined) {
            const ctx = document.getElementById('score-chart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Score', ''],
                    datasets: [{
                        data: [result.score, 100 - result.score],
                        backgroundColor: ['#4CAF50', '#f4f4f4'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    cutout: '80%',
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            enabled: false
                        }
                    }
                }
            });
        }

        // Nettoyer le conteneur des résultats
        resultContainer.innerHTML = "";

        if (result && result.details) {
            const correctCount = result.details.filter(item => item.status === 'correct').length;
            const improveCount = result.details.filter(item => item.status === 'improve').length;
            const errorCount = result.details.filter(item => item.status === 'critical').length;

            document.querySelector(".summary-item.correct p").textContent = `${correctCount} éléments`;
            document.querySelector(".summary-item.improve p").textContent = `${improveCount} éléments`;
            document.querySelector(".summary-item.critical p").textContent = `${errorCount} éléments`;

            result.details.forEach(item => {
                const card = document.createElement("div");
                card.classList.add("detail-card", item.status);
                card.innerHTML = `<h3>${item.title}</h3><p>${item.description}</p>`;
                resultContainer.appendChild(card);
            });
        } else {
            resultContainer.innerHTML = `<p>Pas de résultats détaillés disponibles. Veuillez réessayer.</p>`;
        }
    } catch (e) {
        console.error("Erreur lors de l'analyse JSON:", e);
        resultContainer.innerHTML = `<p>Échec du chargement des résultats. Veuillez réessayer.</p>`;
    }
}
