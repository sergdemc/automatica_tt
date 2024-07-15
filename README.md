# Automatica: test task
A simple API that allows workers to visit stores and write visits to DB. The API is written in Python using the Django REST framework. 

## Installation

### Prerequisites

#### Python

Before installing the package make sure you have Python version 3.10 or higher installed:

```bash
>> python --version
Python 3.10+
```

#### Docker

The project uses Docker to run the database. To install Docker use its [official instruction](https://docs.docker.com/get-docker/).

### Application

To use the application, you need to clone the repository to your computer. This is done using the `git clone` command. Clone the project:

```bash
git clone git@github.com:sergdemc/automatica_tt.git && cd automatica_tt
```

Then you have to install all necessary dependencies in your virtual environment:

```bash
make install
```

## Usage

For start the application you need to create `.env` file in the root directory of the project. You can use `.env.example` as a template.

Start PostgreSQL database in the Docker containers and load fixtures by running:
```bash
make setup
```
_By default, the server will be available at http://127.0.0.1:8000._

Start services by running:
```bash
make start
```

Stop the application by running
```bash
make stop
```

## Tests

To run tests, use the command:
```bash
make test
```

For more commands, see the `Makefile`.