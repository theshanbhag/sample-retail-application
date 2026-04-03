

## Prerequsites

## Deploy from local

### setup env variables
use gcloud to setup the google project to deploy the cloud run function on.
```
# select the project to be used
gcloud init
```

### 1. set up virtualenv

```
virtualenv venv
source venv/bin/activate
```


### 2. Deploy both frontend and backend

```
# the script will load the data to MongoDB
./deploy.sh
```