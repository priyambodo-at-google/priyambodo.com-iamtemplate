export PROJECT_ID=$(gcloud config get project)
export PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
export SERVICE_ACCOUNT_NAME=$(gcloud compute project-info describe --format="value(defaultServiceAccount)")
export GOOGLE_CLOUD_PROJECT=$(gcloud config get project)
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_LOCATION="us-central1"

export GCP_REGION='us-central1'
export AR_REPO='priyambodocom-artifactregistry'  
export SERVICE_NAME='changeme-priyambodo-com'

echo $GCP_REGION
echo $AR_REPO
echo $SERVICE_NAME
