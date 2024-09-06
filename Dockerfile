FROM python:3.12.5-slim

WORKDIR /app/Dawn

ENV reLoginCount 60

COPY Utils /app/Dawn/Utils
COPY main.py /app/Dawn
COPY requirements.txt /app/Dawn
COPY .env /app/Dawn

RUN pip install -r requirements.txt --no-cache-dir


CMD ["python", "main.py"]
