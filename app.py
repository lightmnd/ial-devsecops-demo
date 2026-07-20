"""
Gestionale IAL – mini Flask app per la demo DevSecOps (Lezione 12).

Endpoint:
  GET /              → home page HTML
  GET /api/health    → health check JSON
  GET /api/studenti  → lista studenti (dati mock)
"""

import os
from flask import Flask, jsonify

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Dati mock – in produzione verrebbero da un DB
# ---------------------------------------------------------------------------
STUDENTI = [
    {"id": 1, "nome": "Giulia Rossi",   "corso": "Cloud Architecture"},
    {"id": 2, "nome": "Marco Bianchi",  "corso": "DevSecOps"},
    {"id": 3, "nome": "Sara Conti",     "corso": "FinOps & Sustainability"},
]


@app.route("/")
def home():
    return (
        "<h1>Gestionale IAL</h1>"
        "<p>Demo app per la lezione DevSecOps.</p>"
        "<ul>"
        "<li><a href='/api/health'>/api/health</a></li>"
        "<li><a href='/api/studenti'>/api/studenti</a></li>"
        "</ul>"
    ), 200


@app.route("/api/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "service": "gestionale-ial",
            "environment": os.environ.get("ENVIRONMENT", "local"),
            "version": os.environ.get("APP_VERSION", "1.0.0"),
        }
    ), 200


@app.route("/api/studenti")
def studenti():
    return jsonify({"studenti": STUDENTI, "totale": len(STUDENTI)}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
