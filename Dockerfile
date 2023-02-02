FROM python:3.8-slim

COPY . .
RUN pip3 install -r server/requirements.txt
CMD [ "gunicorn", "--config", "server/gunicorn_config.py", "server/app:gunicorn_app"]