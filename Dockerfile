FROM node:12.18.0-alpine as build
COPY ./client/package.json ./
COPY ./client/package-lock.json ./
RUN npm ci
COPY ./client ./
RUN npm install --save-dev @types/styled-components-react-native
RUN npm run build

FROM nginx:1.23-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
RUN systemctl start nginx.service

FROM python:3.8-slim as run
ENV IN_DOCKER_CONTAINER Yes
COPY ./server/requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY ./server ./
COPY --from=build /build/ ./static/
CMD [ "gunicorn", "--config", "gunicorn_config.py", "app:gunicorn_app"]