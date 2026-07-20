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


@app.after_request
def set_security_headers(response):
    """Add baseline browser protections so the DAST lab starts green."""
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response


# ---------------------------------------------------------------------------
# Dati mock – in produzione verrebbero da un DB
# ---------------------------------------------------------------------------
STUDENTI = [
    {"id": 1, "nome": "Giulia Rossi",   "corso": "Cloud Architecture"},
    {"id": 2, "nome": "Marco Bianchi",  "corso": "DevSecOps"},
    {"id": 3, "nome": "Sara Conti",     "corso": "FinOps & Sustainability"},
]


@app.route("/")  # root
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

@app.route("/api/studenti/<int:studente_id>")
def studente(studente_id):
    studente = next((s for s in STUDENTI if s["id"] == studente_id), None)
    if studente:
        return jsonify(studente), 200
    else:
        return jsonify({"error": "Studente non trovato"}), 404

@app.route("/api/studenti")
def studenti():
    return jsonify({"studenti": STUDENTI, "totale": len(STUDENTI)}), 200

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal Server Error"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
