# pull official base image
FROM python:3.11-bullseye

# set work directory
ENV APP_HOME=/usr/src/app
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1  # prevents Python from buffering stdout and stderr

# update pip
RUN /usr/local/bin/python -m pip install --upgrade pip
# copy & install dev_reqs
COPY ./docker/dev/dev_reqs.txt .
# install dev_reqs.txt to container
RUN pip install -r dev_reqs.txt

# copy project
COPY . .

# run run_timecard_dev.sh on container start
ENTRYPOINT ["/usr/src/app/docker/dev/run_timecard_dev.sh"]
