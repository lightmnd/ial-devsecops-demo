# ---------------------------------------------------------------------------
# Stage 1: dipendenze
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------------------------------------------------------------------------
# Stage 2: immagine finale minimale
# ---------------------------------------------------------------------------
FROM python:3.12-slim

# Utente non-root (security best practice)
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Copia dipendenze dallo stage builder
COPY --from=builder /install /usr/local

# Copia sorgente
COPY app.py .

# Non eseguire come root
USER appuser

EXPOSE 8080

# Gunicorn come server WSGI di produzione
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "30", "app:app"]
