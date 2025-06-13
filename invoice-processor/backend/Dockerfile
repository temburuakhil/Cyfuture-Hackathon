# Invoice Processor Backend Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads processed

EXPOSE 3000

CMD ["python", "main.py"]
