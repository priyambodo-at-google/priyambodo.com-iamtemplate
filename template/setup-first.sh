source ~/.bashrc

# 1. Initialize the Google Cloud Environment

gcloud init
gcloud auth login
gcloud auth application-default login

export PROJECT_ID=work-mylab-machinelearning
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

gcloud config set project $PROJECT_ID
gcloud projects describe $PROJECT_ID --format="value(projectNumber)"
gcloud auth application-default set-quota-project $PROJECT_ID
gcloud config set billing/quota_project $PROJECT_ID
gcloud config list project
gcloud auth list

#gcloud services list --available

gcloud services enable bigquery.googleapis.com \
                       compute.googleapis.com \
                       cloudresourcemanager.googleapis.com \
                       servicenetworking.googleapis.com \
                       vpcaccess.googleapis.com \
                       aiplatform.googleapis.com

gcloud services enable run.googleapis.com \
                       cloudbuild.googleapis.com \
                       artifactregistry.googleapis.com \
                       iam.googleapis.com \
                       secretmanager.googleapis.com \
                       storage.googleapis.com \
                       pubsub.googleapis.com

# 2. Initialize the Google Cloud Variables

export GCP_REGION='us-central1'
export PROJECT_ID=$(gcloud config get project)
export PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
export SERVICE_ACCOUNT_NAME=$(gcloud compute project-info describe --format="value(defaultServiceAccount)")
export GOOGLE_CLOUD_PROJECT=$(gcloud config get project)
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_LOCATION=$GCP_REGION

export AR_REPO='priyambodocom-artifactregistry'  
export SERVICE_NAME='changeme-priyambodo-com'

echo $GCP_REGION
echo $PROJECT_ID
echo $AR_REPO
echo $SERVICE_NAME

# 3. Create Python Virtual Environment 

python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# 4. Deploy the application to Cloud Run (manually)

gcloud artifacts repositories create $AR_REPO \
    --repository-format=docker \
    --location=$GCP_REGION \
    --project=$PROJECT_ID \
    --description="Repository for my images created by Doddi Priyambodo"

gcloud builds submit src/backend/ --tag us-central1-docker.pkg.dev/$PROJECT_ID/$AR_REPO/$SERVICE_NAME

gcloud run deploy $SERVICE_NAME \
    --image $GCP_REGION-docker.pkg.dev/$PROJECT_ID/$AR_REPO/$SERVICE_NAME \
    --platform managed \
    --allow-unauthenticated \
    --region $GCP_REGION \
    --project $PROJECT_ID --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=$GCP_REGION,GOOGLE_GENAI_USE_VERTEXAI=TRUE"

# 5. Setup Git and Push

git config --global user.name "Doddi Priyambodo"
git config --global user.email "doddi@bicarait.com"

# Generate a dynamic commit message with the current timestamp
COMMIT_MESSAGE="Update by Doddi Priyambodo on $(date '+%A, %Y-%m-%d %H:%M:%S')"

# Stage all changes
git add .

# Commit with the dynamic message
git commit -m "$COMMIT_MESSAGE"

# Push to the main branch
git push origin main

# 6. Setup Awesome AGV
npx awesome-agv
