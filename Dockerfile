FROM python:3.7
USER root

# install heroku cli
RUN curl https://cli-assets.heroku.com/install.sh | sh

# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN apt-get update && apt-get install -y \
	&& pip install --upgrade pip
RUN apt-get update && apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y

# change dir
WORKDIR /app

# install module
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

# flask setting
ENV FLASK_APP '/app/app.py'
ENV FLASK_DEBUG 1