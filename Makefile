run:
	docker compose up

bash:
	docker compose run server bash -rm --user root

clean:
	docker image prune
	docker container prune
