FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN sudo apt-get update
RUN sudo apt-get install libpq-dev python3-dev
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["bash", "-c", "python models/models.py && fastapi dev app.py --host 0.0.0.0 --port 8000"]
