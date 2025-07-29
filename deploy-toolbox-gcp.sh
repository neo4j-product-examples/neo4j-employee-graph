export PROJECT_ID="<your-project-id>"

#following 3 commands only need to be run once the first time
gcloud iam service-accounts create toolbox-identity

gcloud projects add-iam-policy-binding $PROJECT_ID \
   --member serviceAccount:toolbox-identity@$PROJECT_ID.iam.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor

gcloud secrets create employee-tools --data-file=tools.yaml

# for running a second time uncomment above 3 commands and run below instead
#gcloud secrets versions add employee-tools --data-file=tools.yaml
export IMAGE=us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest

gcloud run deploy employee-toolbox \
    --image $IMAGE \
    --service-account toolbox-identity \
    --region us-central1 \
    --set-secrets "/app/tools.yaml=employee-tools:latest" \
    --args="--tools-file=/app/tools.yaml","--address=0.0.0.0","--port=8080" \
    --allow-unauthenticated # https://cloud.google.com/run/docs/authenticating/public#gcloud



