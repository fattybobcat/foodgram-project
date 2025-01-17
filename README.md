# foodgram-project
foodgram-project

Foodgram-project running across multiple Docker containers. Foodgram allows you to leave recipes, follow to another users, add favorites recipes, download shoping list of ingredients, follow to another users.

workflow yamdb_final

This project will allow you to deploy to your "empty" server - foodgram-project project

[![Foodgram](https://github.com/fattybobcat/foodgram-project/actions/workflows/main.yml/badge.svg)](https://github.com/fattybobcat/foodgram-project/actions/workflows/main.yml)

## Getting Started

These instructions will get you a copy of the project up and running on your work-machine.
See deployment for notes on how to deploy the project on a live system. 

### Containers

The stack uses Python, Postgres for storage and Nginx.

## INSTALLATION

- Copy this repository to your local machine;
- Create Actions secrets in Github:
  ```
    Name                    Value                           Comments
    DB_ENGINE           =   django.db.backends.postgresql  # indicate that we are working with postgresql
    DB_NAME             =   postgres                       # database name
    POSTGRES_USER       =   login                          # login to connect to the database
    POSTGRES_PASSWORD   =   password                       # password to connect to the database (set your own)
    DB_HOST             =   db                             # service (container) name
    DB_PORT             =   5432                           # port for connecting to the database
    HOST_YC             =   xxx.xxx.xxx.xxx                # ip adress your server
    USER_YC             =                                  # username to connect to the server 
    SSH_KEY_PR          =   ---begin---                    # private key from a computer that has access to the production server (cat ~/.ssh/id_rsa) 
    PASSPHRASE          =                                  # If you used a passphrase when creating the ssh key, then add the variable 
    TELEGRAM_TO         =   your id telegram               # id your Telegram accaunt to which the message will be sent, about the status of the worlkflow assembly (you can ask @userinfobot)  
    TELEGRAM_TOKEN      =   Token                          # token your telegram-bot (you can ask  @BotFather)
    DOCKER_USERNAME     =                                  # your docker name
    DOCKER_PASSWORD     =                                  # your docker password 
  ```
- Push your projects to your Git repo;
- Wait workflow result; If not error - Great! Server is running on your server! Now you can rebild base, create superuser!

## Settings

There is no data in our database now. Need to install migrations and write test database

1. Open a new terminal and connect to your server:
```
  ssh your_login@yor.up.adr.ess
```
2. Run:
```
  docker container ls
```
  You will see next (example):
```
5652f89da934   nginx:1.19.6                         "/docker-entrypoint.…"   23 hours ago   Up 23 hours   0.0.0.0:80->80/tcp   code_nginx_1
5ed74b986dda   fattybobcat/foodgram-project:v1.21   "/bin/sh -c 'gunicor…"   23 hours ago   Up 23 hours                        code_web_1
2622b38c26ce   postgres:12.4                        "docker-entrypoint.s…"   23 hours ago   Up 23 hours   5432/tcp             code_db_1
```
2. Go to the directory where the given project is stored and run the following command to copy the database dump fixture.json to the project need app:
  ```
  docker cp  fixtures.json <CONTAINER ID>
  ```
3. To enter the web container (fattybobcat/foodgram:v1.21): run `docker exec -it <CONTAINER ID> bash`
4. Make migrate `python manage.py migrate`
5. To load the database run the commands:
```
  python3 manage.py shell
# execute in the opened terminal:
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().Delete()
>>> quit()

python manage.py loaddata fixtures.json
```

### Create superuser:

1. To enter the web container (fattybobcat/foodgram-project:v1.21): run `docker exec -it <CONTAINER ID> bash`
2. Run the commands: `python manage.py createsuperuser`

## User for test
username: admin
password: admin

## Site
[site](http://84.201.177.113)
http://84.201.177.113/

## Authors
Petruk Aleksandr - Python Developer

## License
This project is licensed under the MIT License
