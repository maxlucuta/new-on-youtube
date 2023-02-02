FROM python:3.8-slim

COPY . .
RUN python -m pip install --upgrade pip
WORKDIR "/server"
RUN pip3 install -r requirements.txt
CMD [ "gunicorn", "--config", "gunicorn_config.py", "app:gunicorn_app"]