FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if any (none required for basic tests)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt requirements_test.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements_test.txt

# Copy the rest of the code
COPY . .

# Ensure scripts are executable
RUN chmod +x scripts/*.sh

# Default command: run the check script
# We bypass the .venv check in the script by setting VENV_PYTHON
ENV VENV_PYTHON=python3
ENTRYPOINT ["/bin/bash", "./scripts/check.sh"]
