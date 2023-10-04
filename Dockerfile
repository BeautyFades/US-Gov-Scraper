FROM joyzoursky/python-chromedriver:3.9-selenium

RUN apt-get update

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENV APP_HOME /
COPY . .
WORKDIR $APP_HOME