# SupplySentinel - Cloud Deployment Guide

## 🚀 Quick Start: Deploy to Google Cloud Run

### Prerequisites
1. Google Cloud account with billing enabled
2. `gcloud` CLI installed and configured
3. Docker installed locally (optional, for testing)

### Step-by-Step Deployment

#### 1. Configure Your Project
Edit `deploy.sh` and update these variables:
```bash
PROJECT_ID="your-gcp-project-id"  # Your GCP project ID
SERVICE_NAME="supplysentinel"      # Any name you want
REGION="us-central1"               # Choose your region
```

#### 2. Enable Required APIs
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

#### 3. Set Your API Key
The app will prompt for `GEMINI_API_KEY` in the UI. Alternatively, you can set it as an environment variable:

```bash
# During deployment (recommended for production)
gcloud run deploy supplysentinel \
  --set-env-vars GEMINI_API_KEY=your_key_here \
  ... other flags
```

#### 4. Deploy
```bash
# Make script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

The script will:
- Build your Docker container using Cloud Build
- Deploy to Cloud Run
- Provide you with a public URL

#### 5. Access Your App
After deployment completes, you'll see:
```
✅ Deployment complete!
🌐 Your app is now live at:
https://supplysentinel-xxxxx-uc.a.run.app
```

---

## 🧪 Local Testing (Before Deployment)

### Option 1: Run with Streamlit directly
```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
export GEMINI_API_KEY="your_key_here"

# Run the app
streamlit run app.py
```

### Option 2: Test with Docker locally
```bash
# Build the image
docker build -t supplysentinel .

# Run the container
docker run -p 8080:8080 \
  -e GEMINI_API_KEY="your_key_here" \
  supplysentinel
```

Visit `http://localhost:8080`

---

## 🔒 Security Best Practices

### For Production Deployment:

1. **Use Secret Manager** (instead of environment variables):
```bash
# Store API key in Secret Manager
gcloud secrets create gemini-api-key --data-file=-
# (paste your key and press Ctrl+D)

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding gemini-api-key \
  --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/secretmanager.secretAccessor

# Deploy with secret
gcloud run deploy supplysentinel \
  --image gcr.io/PROJECT_ID/supplysentinel \
  --set-secrets=GEMINI_API_KEY=gemini-api-key:latest
```

2. **Enable Authentication** (for internal use):
Remove `--allow-unauthenticated` from deploy.sh and add:
```bash
--no-allow-unauthenticated
```

---

## 📊 Monitoring & Logs

View logs:
```bash
gcloud run services logs read supplysentinel --region us-central1
```

View metrics in Cloud Console:
```
https://console.cloud.google.com/run/detail/{REGION}/supplysentinel
```

---

## 💰 Cost Estimation

**Cloud Run Pricing (as of 2025):**
- First 2 million requests/month: FREE
- CPU: ~$0.00002400/vCPU-second
- Memory: ~$0.00000250/GiB-second
- Requests: $0.40 per million

**Typical usage:** ~$5-20/month for moderate use

---

## 🔄 Update Deployment

After making code changes:
```bash
# Simply re-run the deployment script
./deploy.sh
```

Cloud Run will automatically roll out the new version with zero downtime.

---

## 🆘 Troubleshooting

### Issue: "Permission denied" on deploy.sh
```bash
chmod +x deploy.sh
```

### Issue: "API not enabled"
```bash
gcloud services enable cloudbuild.googleapis.com run.googleapis.com
```

### Issue: Container fails to start
Check logs:
```bash
gcloud run services logs read supplysentinel --region us-central1 --limit 50
```

### Issue: Out of memory
Increase memory in deploy.sh:
```bash
--memory 1Gi  # Instead of 512Mi
```

---

## 📚 Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Streamlit Cloud Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Google Cloud Build](https://cloud.google.com/build/docs)
