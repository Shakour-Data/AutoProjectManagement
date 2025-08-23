FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN groupadd -r apm && useradd -r -g apm apm

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    cron \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data /app/logs && \
    chown -R apm:apm /app

USER apm

# Setup cron for scheduled tasks
COPY docker/worker/crontab /etc/cron.d/apm-cron
RUN chmod 0644 /etc/cron.d/apm-cron && crontab /etc/cron.d/apm-cron

CMD ["python", "-m", "autoprojectmanagement.services.automation_services.auto_commit"]
