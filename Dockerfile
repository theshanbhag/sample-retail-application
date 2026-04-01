# Use official lightweight Python image.
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Set work directory
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit uses port 8501 by default, but Cloud Run expects $PORT (usually 8080)
# We tell Streamlit to listen on the port provided by Cloud Run
CMD streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0
