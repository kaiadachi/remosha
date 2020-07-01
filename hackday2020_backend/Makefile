all: \
	clean \
	build \
	run

build:
	docker build -t hackday2020_backend .

clean:
	docker container rm -f hackday2020_backend || echo "No container, skip remove"

run:
	docker container run -d -p 9000:9000 -it \
		--name hackday2020_backend hackday2020_backend:latest

bash:
	docker container exec -it hackday2020_backend /bin/bash