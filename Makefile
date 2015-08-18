all: staticdata db app nginx

db:
	docker run --name postgres -e POSTGRES_PASSWORD=qwerty -e POSTGRES_USER=root -d postgres
	sleep 10
	docker exec postgres psql -c "CREATE DATABASE hrportal"

app:
	docker build -t hruaprom docker/hrportal
	docker run --name hrportal --volumes-from staticdata --link postgres:postgres -d hruaprom
	docker exec hrportal python3 manage.py dbutils init -p

staticdata:
	docker create -v /staticdata --name staticdata ubuntu /bin/true

nginx:
	docker build -t nginx docker/nginx/
	docker run --name nginx --link hrportal:hrportal --volumes-from staticdata -p 80:80 -d nginx