# # Backend Dockerfile for Flask
# FROM python:3.11-slim

# ENV PYTHONUNBUFFERED True
# ENV APP_HOME /app
# WORKDIR $APP_HOME
# COPY . ./

# RUN pip install --no-cache-dir -r requirements.txt

# # Cloud Run expects the application to listen on $PORT
# # We'll use Gunicorn to run the Flask app
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
