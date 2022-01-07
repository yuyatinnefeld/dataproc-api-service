# Dataproc API Service
This Project is built with FastAPI. You can manage the Dataproc Service in Swagger UI.

## Essential Pieces of the Software
- GCP Project (ex. yt-demo-dev)
- GCP Service Account Json Key (stored in conf/creds.json)
- Python 3.7 or older version
- Cloud SDK 
- Gitlab
- Docker

## Setup Environment Variables
```bash
vi settings.py
```

## Setup the Python Environment
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/conf/creds.json"
```

## Setup the GCP Environment
```bash
PROJECT_ID="yt-demo-dev"
REGION="europe-west1"
SERVICE_ACCOUNT_NAME="demo-dataproc"
GCP_SERVICE_ACCOUNT_KEY_DEV=${GOOGLE_APPLICATION_CREDENTIALS}

gcloud auth activate-service-account --key-file ${GCP_SERVICE_ACCOUNT_KEY_DEV}
gcloud config set project ${PROJECT_ID}

# create a service account for dataproc workflow template
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \
    --display-name="dataproc service account"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/dataproc.admin"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/dataproc.editor"

# upload a autoscaling cluster
POLICY_NAME="yt-demo-dev-autoscaling-policy"
FILE_NAME="resources/autoscaling_policy.yaml"

gcloud dataproc autoscaling-policies import ${POLICY_NAME} \
    --source=${FILE_NAME} \
    --region=${REGION}

# create 2 buckets for the dataproc cluster configuration
DATAPROC_TAMP_BUCKET="${PROJECT_ID}-dataproc-temp"
DATAPROC_STAGING_BUCKET="${PROJECT_ID}-dataproc-staging"
gsutil mb -c "STANDARD" -l ${REGION} gs://${DATAPROC_TAMP_BUCKET}
gsutil mb -c "STANDARD" -l ${REGION} gs://${DATAPROC_STAGING_BUCKET}

# upload few spark jobs in the temp bucket for the dataproc workflow template
gsutil cp spark/data_collection_job.py gs://${DATAPROC_TAMP_BUCKET}/src/data_collection_job.py
gsutil cp spark/data_processing_job.py gs://${DATAPROC_TAMP_BUCKET}/src/data_processing_job.py
gsutil cp spark/data_validation_job.py gs://${DATAPROC_TAMP_BUCKET}/src/data_validation_job.py

# create a workflow templates
DATA_COLLECTION_TEMP="data_collection_wf_temp"
DATA_PROCESSING_TEMP="data_processing_wf_temp"
DATA_VALIDATION_TEMP="data_validation_wf_temp"

gcloud dataproc workflow-templates import ${DATA_COLLECTION_TEMP} \
    --source=resources/${DATA_COLLECTION_TEMP}.yaml \
    --region=${REGION}

gcloud dataproc workflow-templates import ${DATA_PROCESSING_TEMP} \
    --source=resources/${DATA_PROCESSING_TEMP}.yaml \
    --region=${REGION}

gcloud dataproc workflow-templates import ${DATA_VALIDATION_TEMP} \
    --source=resources/${DATA_VALIDATION_TEMP}.yaml \
    --region=${REGION}
```
## Getting started

### Local Run
```bash
uvicorn app.main:app --reload
curl -i http://127.0.0.1:8000
# open the URL
http://127.0.0.1:8000/docs

```

## Dockerize Local Run

1. Open the Dockerfile 
2. Activate `COPY ./conf /code/conf` cmd

2. Docker run 
```bash
# test run
docker build -t fastapi-image .
docker run -it -p 8080:8080 -d fastapi-image
docker ps
# check and test the API
http://127.0.0.1:8080/docs
```

## Deploy to Cloud Run (NoOps)
1. Open Cloud Code Extenstion
2. Select Deploy to Cloud Run
3. Setup the environment
- service name: dataproc-api-service
- region: europe-west1
- url: gcr.io/yt-demo-dev/dataproc-api-service
