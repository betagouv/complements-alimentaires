build:
	docker compose build

run:
	docker compose up

bash:
	docker compose run --user root server bash -rm

clean:
	docker image prune
	docker container prune
