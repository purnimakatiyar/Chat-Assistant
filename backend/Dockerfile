FROM python:3.12-slim AS deps

WORKDIR /deps

# System packages needed to compile any C-extension wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install into a separate prefix so we can copy just this layer later
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim AS runtime


RUN groupadd --system appgroup && \
    useradd  --system --gid appgroup --home /app --shell /bin/false appuser

WORKDIR /app

# Copy installed packages from the deps stage
COPY --from=deps /install /usr/local


COPY app/     ./app/
COPY main.py  ./main.py

RUN mkdir -p /app/logs && chown -R appuser:appgroup /app

USER appuser

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LOG_LEVEL=INFO \
    LOG_TO_FILE=false \
    PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c \
        "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"


CMD ["sh", "-c", \
     "uvicorn main:app \
        --host 0.0.0.0 \
        --port ${PORT} \
        --workers ${WORKERS:-2} \
        --proxy-headers \
        --no-access-log"]
