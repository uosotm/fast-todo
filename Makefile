run:
	docker compose up
format:
	docker compose exec fast-todo poetry run black .
