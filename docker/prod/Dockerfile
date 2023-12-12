###########
# BUILDER #
###########

# pull official base image
FROM python:3.11-bullseye as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# lint
RUN pip install --upgrade pip

# install dependencies
COPY ./docker/prod/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.11-bullseye

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -system app \
    && adduser -system app \
    && adduser app app

# create the appropriate directories
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME \
    && mkdir $APP_HOME/static \
    && mkdir $APP_HOME/media
WORKDIR $APP_HOME

# install dependencies
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy run_timecard.sh
COPY ./docker/prod/run_timecard.sh .
RUN chmod +x $APP_HOME/run_timecard.sh

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run migrate and start gunicorn when container starts
ENTRYPOINT ["/home/app/web/run_timecard.sh"]
