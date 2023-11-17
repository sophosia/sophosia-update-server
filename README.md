# Sophosis update server

When the Sophosia app checks for update, it request this server using the endpoint
```
https://sophosia-update-server.uc.r.appspot.com/<target>/<current_version>
```
This server grabs the latest release in sophosia repo and determine if the new release has different version number than the `current_version` of the app. If version number is different, this server returns a list of update files for different platforms together with their download urls and signitures. Tauri will update itself according to the server response.

# Deployment
## Prepare Project
1. Prepare the flask project.
2. In `app.yaml`, add a line `runtime: python310` to specify the python runtime.
3. Add `requirements.txt` and add necessary dependencies, `gunicorn` is needed to manage entry point.
4. In `main.py`, expose the app on host 0.0.0.0 and port 5000.

## Create Google Cloud Project
1. Create a project on [Google Cloud Platform](https://console.cloud.google.com/welcome).
2. Add Cloud Build API.

## Google Cloud SDK
1. Download and install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install-sdk).
2. Initialize SDK and set our default project by doing
```
gcloud init
```

## Deploy to GCP
1. Add AppEngine to GCP
```
gcloud components install app-engine-python
```
2. Deploy
```
gcloud app deploy
```
3. Browse app
```
gcloud app browse
```

## Update
After finish updating the app, to redeploy the app we simply do deploy it again,
```
gcloud app deploy
```
