install:
	pip install -r requirements.txt

migrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

db_load:
	python3 manage.py loaddata fixtures.json


setup:
	cp -n .env.example .env || true
	make install
	make db-start
	make migrations
	make migrate
	make db_load

db-start:
	docker-compose up -d --build --remove-orphans

db-stop:
	docker-compose stop

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) store_service.wsgi

stop:
	docker-compose down --volumes --remove-orphans

dev:
	poetry run python manage.py runserver 0.0.0.0:8080

check:
	poetry check

lint:
	poetry run flake8 store_service api

test:
	poetry run python3 manage.py test

deploy:
	git push

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev
