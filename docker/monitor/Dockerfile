FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache \
    curl \
    docker-cli

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "autoprojectmanagement.services.status_service"]
