all: \
	clean \
	build \
	run

build:
	docker build -t hackday2020_frontend .

clean:
	docker container rm -f hackday2020_frontend || echo "No container, skip remove"

run:
	docker container run -d -p 443:8000 -it \
		--name hackday2020_frontend hackday2020_frontend:latest

sh:
	docker container exec -it hackday2020_frontend sh

log:
	docker container logs hackday2020_frontend -f
