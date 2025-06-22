.PHONY: run build test

run:
	docker-compose up --build

build:
	docker-compose build

test-backend:
	docker-compose exec backend pytest -v

test-frontend:
	docker-compose exec frontend npm run test

migrate:
	docker-compose exec backend alembic upgrade head

init-db:
	docker-compose exec backend python scripts/init_db.py