# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY config.json ./config.json

# Expose Gradio default port
EXPOSE 7860

# Set environment variables (can be overridden by docker-compose)
ENV PYTHONUNBUFFERED=1

# Entrypoint
CMD ["python", "src/ui.py"] 