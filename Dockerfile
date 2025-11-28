FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install  -r requirements.txt

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

ENV SIGNAL_FILE=data/signals.jsonl
ENV APP_PORT=8000
ENV TARGET_DOMAIN=bellingcat.com

EXPOSE 8000

CMD ["python", "app.py"]