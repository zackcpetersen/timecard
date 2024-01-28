# Timecard app

## Local Settings
### This app runs on Python 3.11 and Django 3.2.22  
`docker compose up -d` - to run db and background images

`export DJANGO_SETTINGS_MODULE=timecard.settings.dev` - use dev settings
`export DJANGO_SETTINGS_MODULE=timecard.settings.base` - use base settings

`python manage.py`
- `makemigrations`
- `migrate`
- `collectstatic`
- `createsuperuser`


- `runserver`


- `flush`
- `test -v 2`

## Updating requirements.txt
`pipenv requirements > ./docker/prod/requirements.txt && pipenv requirements --dev > ./docker/dev/dev_reqs.txt`

## Virtual Environment
This project uses pipenv to manage virtual environment and dependencies.  
- Run any commands outside of the virtual environment with `pipenv run <command>`.  
- To create a new virtual environment, run `pipenv install` in the project root directory.  
- To activate the virtual environment, run `pipenv shell` in the project root directory.  
- To delete the virtual environment, run `pipenv --rm` in the project root directory.  


# Migrating to a new AWS Account
- create the new account under the castle rock org
  - create terraform user with custom admin access
- terraform apply the backend (use access creds from terraform user)
  - may need to swap domain names in modules/route53
- copyS3 data for project and profile images
- make sure frontend is pointing to correct backend api domain
- deploy frontend
- swap `www` and `backend` subdomains to point at loadbalancer and cloudfront distro (both outputs of backend apply)
- ???
- profit
