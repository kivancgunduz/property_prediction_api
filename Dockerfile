FROM python:3.8

RUN mkdir /app

COPY . /app

# Delete virtual env files
RUN rm -rf /app/env

WORKDIR /app

# Install necessery libs
RUN pip install -r requirements.txt

# Run app 
CMD python app.py
