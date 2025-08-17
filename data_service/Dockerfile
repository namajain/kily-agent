# Data Service Dockerfile (Hardcoded Mode)
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Data Service requirements and install dependencies
COPY data_service/pyproject.toml data_service/uv.lock ./
RUN pip install uv && uv sync --frozen

# Copy Data Service code
COPY data_service/ ./

# Expose port
EXPOSE 5002

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5002/health || exit 1

# Start the Data Service server
CMD ["uv", "run", "python3", "server.py"]
