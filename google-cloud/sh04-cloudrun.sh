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
