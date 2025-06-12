export PYTHONDONTWRITEBYTECODE=1

docker rm -f $(docker ps -a -q)
docker volume rm $(docker volume ls -q)

docker compose up --build