gcloud run deploy tiebreak-demo-ui \
      --region=us-central1 \
      --source=. \
      --service-account=350195377988-compute@developer.gserviceaccount.com \
      --min-instances=1 \
      --min=1 \
      --memory=512Mi \
      --no-invoker-iam-check \
      --port=80