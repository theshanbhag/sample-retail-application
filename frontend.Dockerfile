# # Frontend Dockerfile for Streamlit
# FROM python:3.11-slim

# ENV PYTHONUNBUFFERED True
# ENV APP_HOME /app
# WORKDIR $APP_HOME
# COPY . ./

# RUN pip install --no-cache-dir -r requirements.txt

# # Cloud Run expects the application to listen on $PORT
# # We'll run Streamlit and tell it to use the port provided by Cloud Run
# CMD streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0
