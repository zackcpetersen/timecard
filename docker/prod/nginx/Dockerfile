FROM nginx:1.24-bullseye

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/prod/nginx/nginx.conf /etc/nginx/conf.d
