FROM python:3.8-slim

COPY . .
RUN pip3 install -r requirements.txt
CMD [ "gunicorn", "--config", "gunicorn_config.py", "app:gunicorn_app"]