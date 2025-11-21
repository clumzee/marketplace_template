FROM python:3.10-slim
WORKDIR /app

# install system deps needed for psycopg and building wheels
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential gcc libpq-dev python3-dev ca-certificates \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Inline Python wait (no extra file), then run models script and start uvicorn
CMD ["sh", "-c", "(python - <<'PY'\nimport socket, time, sys\nhost='db'; port=5432\nstart=time.time()\nwhile time.time()-start < 60:\n    try:\n        s=socket.create_connection((host,port),2); s.close(); print('DB reachable'); sys.exit(0)\n    except Exception:\n        time.sleep(1)\nprint('DB wait timeout'); sys.exit(1)\nPY\n) && python models/models.py && uvicorn app:app --host 0.0.0.0 --port 8000"]
