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

gcloud services list --available

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
