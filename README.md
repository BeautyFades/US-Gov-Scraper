# US Congressmen Webscraper

This project implements a Cloud-based framework for running Selenium, Chrome and Python in a containerized application. The application can also be hosted on a local machine for development or testing purposes.

# Local deploy commands
1. Ensure the Docker daemon is running on your machine
2. Build the container by ```cd```ing into this projects root folder (the one that contains the _Dockerfile_) and run the following command ```docker build -t scraper .```.
3. Run the container by executing the following command: ```docker run -p 8080:8080 scraper ipython app.py```. Note the port mappings map port 8080 on the host machine to the port 8080 on the container (the one configured in the _Dockerfile_ and also on ```entrypoint.py```'s ```app.run()``` statement)
4. You can now access the Flask routes by visiting [localhost:8080/<route_path>](), such as [localhost:8080/healthcheck]() or [localhost:8080/api/v1/scrape]().

# Google Cloud Run deploy commands
1. Make sure you have the GCP CLI tools properly installed (access to _gcloud_ commands in your command line). Also make sure you're connected to the correct project (```gcloud config set project <proj_name>```).
2. Build the container on Google Cloud Build by ```cd```ing into this projects root folder (the one that contains the _Dockerfile_) and running the following command ```gcloud builds submit --tag gcr.io/<project_name>/policheck-scraper .```.
3. Run the container on Google Cloud Run by executing: ```gcloud run deploy policheck-scraper --image gcr.io/<project_name>/policheck-scraper --region us-east1 --memory 1024Mi --platform managed --allow-unauthenticated --quiet --min-instances 0 --max-instances 1 --command ipython --args entrypoint.py```.
4. Once ready, the CLI will return a URL, something like [https://<project-name>-xxxxxxxxxx-xx.x.run.app](), from which you can use just like we used [localhost]() beforehand, i.e. [https://<project-name>-xxxxxxxxxx-xx.x.run.app/healthcheck](). We do not have to specify a __:8080__ port here since Cloud Run automatically listens on __$PORT__ which was defined on the _Dockerfile_ and maps all requests to it.

**CAUTION**: Note the ```--allow-unauthenticated``` flag when deploying to Cloud Run. When Cloud Run finishes up, it will spit that base service URL which will not check for authenticated API calls. Anyone with the link wil be able to trigger the scraper or visit any other routes. It is highly recommended to secure the endpoint for the project's next steps. More info on [Cloud Run Authentication Overview](https://cloud.google.com/run/docs/authenticating/overview).