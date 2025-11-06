FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["bash", "-c", "python db_init_script.py && uvicorn app:app --host 0.0.0.0 --port 8000"]
