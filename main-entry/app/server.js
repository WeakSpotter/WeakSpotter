const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Servir les fichiers statiques
app.use(express.static(path.join(__dirname, 'public')));

// Route pour afficher la page principale
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Route pour afficher la page d'analyse
app.get('/analyze', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'analyze.html'));
});

// Route pour analyser l'URL
app.post('/analyze', async (req, res) => {
    const url = req.body.url;
    console.log("URL reçue pour analyse :", url);  // Log de l'URL reçue
    try {
        const response = await axios.post('http://web-analyzer:5000/analyze', { url });
        const result = response.data; // Récupère le JSON complet de la réponse
        res.json(result); // Renvoyer le JSON complet
    } catch (error) {
        console.error("Erreur pendant l'analyse :", error.message);
        res.json({ status: "error", result: "Failed to analyze URL. Please try again later." });
    }
});

app.listen(80, () => {
    console.log('Main Entry running on port 80');
});
