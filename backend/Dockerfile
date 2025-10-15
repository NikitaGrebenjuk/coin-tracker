# coin-tracker/backend/Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements if present
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONPATH=/

# Copy application code
# COPY ./app ./app

# Expose port (change if needed)
EXPOSE 8000

# Default command (change app.py if needed)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]