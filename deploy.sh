#!/bin/bash

# SupplySentinel - Google Cloud Run Deployment Script
# Usage: ./deploy.sh

set -e

# Configuration Variables
PROJECT_ID=gen-lang-client-0162519462
SERVICE_NAME="supplysentinel"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying SupplySentinel to Google Cloud Run..."
echo "Project: ${PROJECT_ID}"
echo "Service: ${SERVICE_NAME}"
echo "Region: ${REGION}"
echo ""

# Step 1: Build the container image
echo "📦 Building container image..."
gcloud builds submit --tag ${IMAGE_NAME} --project ${PROJECT_ID}

# Step 2: Deploy to Cloud Run
echo "☁️  Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --memory 512Mi \
  --timeout 300 \
  --project ${PROJECT_ID}

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your app is now live at:"
gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format 'value(status.url)' --project ${PROJECT_ID}
