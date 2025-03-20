# Frontend build stage
FROM node:18 AS frontend-build

WORKDIR /frontend

# Copy only package files first to leverage Docker cache
COPY frontend/package.json frontend/package-lock.json ./ 
RUN npm ci

# Copy the entire frontend directory
COPY frontend/ ./ 

# Build the frontend (React app)
RUN npm install react-router-dom && npm install axios && npm run build

# Backend build stage
FROM python:3.9 AS backend-build

WORKDIR /backend

# Copy only requirements file first (cache optimization)
COPY backend/requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY backend/ ./ 

# Copy secrets.txt into the container (ensure this file is in the backend folder)
#COPY backend/secrets.txt ./secrets.txt

# Final stage: Using a smaller, more secure image
FROM python:3.9-slim AS final

WORKDIR /backend

# Use a non-root user for security
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy backend from backend-build stage
COPY --from=backend-build /backend /backend

# Copy frontend build from frontend-build stage
COPY --from=frontend-build /frontend/build /backend/frontend/build

# Copy installed dependencies
COPY --from=backend-build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=backend-build /usr/local/bin /usr/local/bin

# Expose port 8080 (Google Cloud Run default)
EXPOSE 8080

# Set user for better security
USER appuser

# Command to run the application with Gunicorn
CMD ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-b", "0.0.0.0:8080", "main:app"]