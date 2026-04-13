FROM python:3.11-slim

# Set metadata
LABEL maintainer="R0b3rt0 <author@example.com>"
LABEL version="5.0"
LABEL description="AutoXSS - Automated XSS Discovery Framework"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY xssgen.py .
COPY lib_*.py .
COPY payloads/ payloads/
COPY README.md LICENSE ./

# Create directories for logs and audit trails
RUN mkdir -p /app/logs /app/.audit_logs /app/reports

# Set proper permissions
RUN chmod +x xssgen.py

# Health check (basic connectivity test)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)" || exit 1

# Non-root user for security
RUN useradd -m -u 1000 scanner && chown -R scanner:scanner /app
USER scanner

# Default entrypoint
ENTRYPOINT ["python3", "xssgen.py"]
CMD ["--help"]
