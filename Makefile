install:
	poetry install

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

setup:
	cp -n .env.example .env || true
	make install
	make migrations
	make migrate

db-start:
	docker-compose up -d --build --remove-orphans

db-stop:
	docker-compose stop

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

dev:
	poetry run python manage.py runserver 0.0.0.0:8080

check:
	poetry check

lint:
	poetry run flake8 task_manager users tasks labels statuses

test:
	poetry run python3 manage.py test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m --omit='*/python-project-83/*'
	poetry run coverage xml --omit='*/python-project-83/*'

deploy:
	git push

requirements:
	poetry export -f requirements.txt --output requirements.txt
