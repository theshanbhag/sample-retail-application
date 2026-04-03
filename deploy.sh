#!/bin/bash

# Configuration
# Replace with your GCP project ID or set as environment variable
PROJECT_ID=${GCP_PROJECT_ID:-$(gcloud config get-value project)}
REGION=${GCP_REGION:-"us-central1"}
BACKEND_SERVICE_NAME="catalog-backend"
FRONTEND_SERVICE_NAME="catalog-frontend"
REPOSITORY_NAME="catalog-repo"

# Check for required environment variables
if [ -z "$MDB_MCP_CONNECTION_STRING" ]; then
    echo "Error: MDB_MCP_CONNECTION_STRING environment variable is not set."
    echo "This is required to run the load_data.py script and for the backend."
    exit 1
fi

if [ -z "$PROJECT_ID" ]; then
  echo "Error: GCP_PROJECT_ID not set and could not be found in gcloud config."
  exit 1
fi

echo "Using Project ID: $PROJECT_ID"
echo "Using Region: $REGION"


# 1. Deploy Backend
echo "Deploying Backend to Cloud Run..."
gcloud run deploy $BACKEND_SERVICE_NAME --source . \
    --command="gunicorn,--bind,0.0.0.0:8080,--workers,1,--threads,8,--timeout,0,main:app" \
    --set-env-vars="MDB_MCP_CONNECTION_STRING=$MDB_MCP_CONNECTION_STRING" \
    --region us-central1  \
    --allow-unauthenticated

# 2.Get Backend URL
BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE_NAME --region $REGION --format 'value(status.url)')
echo "Backend is available at: $BACKEND_URL"

# 3. Deploy Frontend
echo "Deploying Frontend to Cloud Run..."
gcloud run deploy $FRONTEND_SERVICE_NAME \
    --source . \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars "API_URL=$BACKEND_URL" \
    --allow-unauthenticated

# 4.Get Frontend URL
FRONTEND_URL=$(gcloud run services describe $FRONTEND_SERVICE_NAME --region $REGION --format 'value(status.url)')

# 5. Run load_data.py
echo "Installing Python dependencies for local data loader..."
pip install --quiet -r requirements.txt

echo "Running load_data.py to populate MongoDB..."
python3 load_data.py

echo "--------------------------------------------------"
echo "Deployment Complete!"
echo "Backend URL: $BACKEND_URL"
echo "Frontend URL: $FRONTEND_URL"
echo "--------------------------------------------------"
