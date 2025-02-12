# Build stage
FROM python:3.8-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Nginx stage
FROM nginx:alpine

# Install Python and dependencies
RUN apk add --no-cache python3 py3-pip

# Copy Python environment from builder
COPY --from=builder /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/

# Copy application code
COPY . /app
WORKDIR /app

# Configure Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 8080

# Start Nginx and FastAPI
CMD nginx && uvicorn main:app --host 0.0.0.0 --port 8000

