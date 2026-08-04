# Dockerfile for Capacitismo Algorítmico Dataset
# Reproducible environment for validation, ETL, and development

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install test dependencies
RUN pip install --no-cache-dir pytest hypothesis

# Install linting tools
RUN pip install --no-cache-dir ruff yamllint

# Copy the entire project
COPY . .

# Make scripts executable
RUN chmod +x scripts/*.py

# Default command
CMD ["make", "validate-all"]