# metaslacker

## Docker Docker Docker

1. [Docker](https://docs.docker.com/installation/) 1.8.1
1. [Docker Machine](https://docs.docker.com/machine/#installation) 0.4.0
1. [Docker Compose](https://docs.docker.com/compose/install/) 1.4.0

# Local

## Initialize the Environment

```
docker-machine create --driver virtualbox metaslacker-dev
eval "$(docker-machine env metaslacker-dev)"
docker-compose up
```

## Initialize the Database

```
docker-compose run --rm --no-deps api python api.py create_db
```

# Remote

## Initialize the Environment

```
export OS_USERNAME=your-rackspace-username
export OS_API_KEY=your-rackspace-api-key
export OS_REGION_NAME=IAD
```

```
docker-machine create --driver rackspace metaslacker
eval "$(docker-machine env metaslacker)"
docker-compose --file docker-compose-prod.yml build
docker-compose --file docker-compose-prod.yml up -d
```

## Initialize the Database

```
export MYSQL_USER=metaslacker-admin
export MYSQL_PASSWORD=$(hexdump -v -e '1/1 "%.2x"' -n 32 /dev/random)
export MYSQL_ROOT_PASSWORD=$(hexdump -v -e '1/1 "%.2x"' -n 32 /dev/random)

docker-compose --file docker-compose-prod.yml run --rm --no-deps api python api.py create_db
```

## Secure the Environment

```
docker-machine ssh metaslacker "apt-get update"
docker-machine ssh metaslacker "apt-get -y install fail2ban"
docker-machine ssh metaslacker "ufw default deny"
docker-machine ssh metaslacker "ufw allow ssh"
docker-machine ssh metaslacker "ufw allow http"
docker-machine ssh metaslacker "ufw allow 2376" # Docker
docker-machine ssh metaslacker "ufw --force enable"
```

## Deploy Changes to Remote

```
docker-compose --file docker-compose-prod.yml build
docker-compose --file docker-compose-prod.yml up -d --x-smart-recreate
```

## Work with the Database

```
docker run --rm --link metaslacker_db_1:db mysql:5.7 sh -c \
  'exec mysql \
  --host=$DB_PORT_3306_TCP_ADDR \
  --user=root \
  --password=$DB_ENV_MYSQL_ROOT_PASSWORD \
  --database=$DB_ENV_MYSQL_DATABASE \
  --execute="show tables;" \
  --table'

docker run --rm --link metaslacker_db_1:db mysql:5.7 sh -c \
  'exec mysqldump \
  --host=$DB_PORT_3306_TCP_ADDR \
  --user=root \
  --password=$DB_ENV_MYSQL_ROOT_PASSWORD \ 
  --databases $DB_ENV_MYSQL_DATABASE \
  --single-transaction \
  --add-drop-database' > $DB_ENV_MYSQL_DATABASE.sql
```

## Alias

```
alias de='env | grep DOCKER_'
```