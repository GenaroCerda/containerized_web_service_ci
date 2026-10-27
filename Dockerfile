# ---- Etapa 1: builder (instala dependencias) ----
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Etapa 2: imagen final ----
FROM python:3.12-slim
RUN useradd --create-home --uid 1000 appuser
WORKDIR /app
COPY --from=builder /install /usr/local
COPY app/ ./app/
USER appuser
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.main:app"]