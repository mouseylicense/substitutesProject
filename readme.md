
# Substitutes Project (Still looking for a name 😐)

This is a school project (not homework!) to help school manage teacher substitutions,
A teacher (super teacher) enters all classes, and when teachers report Absences classes are marked that they need a Substitution,The super teacher then can mark who Substitutes that class.

This project is done for now, but will likely have more development in the future

some environment variables need to be defined in an .env file:

| Key                 | Description                                                         |  
|---------------------|---------------------------------------------------------------------|
| EMAIL_HOST          | The host for the SMTP server                                        |
| EMAIL_USE_TLS       | Choose if SMTP should use TLS                                       |
| EMAIL_PORT          | SMTP Port                                                           |
| EMAIL_HOST_USER     | ------                                                              |
| EMAIL_HOST_PASSWORD | ------                                                              |
| DEFAULT_FROM_EMAIL  | Email Sender                                                        |
| DB_USER             | Database Username                                                   |
| DB_PASSWORD         | Database password                                                   |
| DB_HOST             | Database Host IP                                                    |
| DB_PORT             | Database Host Port, Also needs to be changed in docker-compose.yaml |
| DB_ROOT_PASSWORD    | Database Root Password                                              |
| DJANGO_SECRET_KEY   | The Django Secret Key (optional)                                    |
| DJANGO_DEBUG        | True or False, Choose if django should run in debug mode (optional) |
After Running the containers, this command should be run to create a super user:
``` shell
~$ docker exec -it Substitutes_backend python manage.py createsuperuser
```
docker-compose.yaml:

```yaml
version: '3.8'
services:
  db:
    image: mysql:9.0.0
    container_name: Substitutes_DB
    restart: unless-stopped
    volumes:
      - ./data/conf.d:/etc/mysql/conf.d
      - ./data/logs:/logs
      - /usr/local/var/mysql:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: subs
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
    ports:
      - "3303:3306"
    healthcheck:
      test: ["CMD", "mysql", "-h", "localhost", "-u", "root", "-p${DB_ROOT_PASSWORD}", "-e", "SELECT 1"]
      timeout: 20s
      retries: 10
  backend:
    image: mouseylicense/substitutes:latest
    container_name: Substitutes_backend
    restart: unless-stopped
    ports:
      - "5858:5858"
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
volumes:
  data:
```

