

## Prerequsites

## Deploy from local

### setup env variables
use gcloud to setup the google project to deploy the cloud run function on.
```
# select the project to be used
gcloud init
```

### Create the backend the application on cloud run

```

# deploy the docker image on cloud run
gcloud run deploy grocery-api --source .  --command="gunicorn,--bind,0.0.0.0:8080,--workers,1,--threads,8,--timeout,0,main:app"  --set-env-vars="MDB_MCP_CONNECTION_STRING=<<connection string>>" --region us-central1  --allow-unauthenticated

```

### Create the frontend for the application on cloud run

```
cloud run deploy grocery-frontend  --source .  --command="streamlit,run,streamlit_app.py,--server.port,8080,--server.address,0.0.0.0"  --set-env-vars="API_URL=<app url from backend command output>"  --region us-central1   --allow-unauthenticated
```
