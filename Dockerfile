FROM ultrafunk/undetected-chromedriver:latest

RUN apt-get update

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV APP_HOME /
COPY . .
WORKDIR $APP_HOME
ENV PORT=8000

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app