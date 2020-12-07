FROM python:3.7
WORKDIR /app
RUN apt-get update -y && apt-get install -y libopencv-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY ./server/requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn
COPY ./server .
CMD gunicorn --bind 0.0.0.0:$PORT app