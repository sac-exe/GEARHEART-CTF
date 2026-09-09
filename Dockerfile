FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY flag.txt .
COPY private.pem .
COPY templates/ ./templates/

EXPOSE 5050

CMD ["python", "app.py"]
