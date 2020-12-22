# Lingo trainer created with connexion
![Alt text](openapi_server/test/coverage.svg)


## Overview
This lingo trainer is a school project created for the course 'backend programming'. 
With the use of connexion I created an flask project that uses OpenAPI. [OpenAPI-Spec](https://openapis.org) 
from a remote server, you can easily generate a server stub. This is an example of building a OpenAPI-enabled Flask server.

This project uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

The project runs on Heroku and is analysed by sonarcloud (my [Sonarcloud](https://sonarcloud.io/dashboard?id=MiloVoorhout_hu_lingo_backend))

## Requirements
Python 3.5.2+

## Usage
For creating the environment variables and database go to: [Preparation](#preparation)
To run the server, please execute the following from the root directory:

```
pip3 install -r requirements.txt
python3 -m openapi_server
```

and open your browser to here:

```
http://localhost:5000/api/ui/
```

Your OpenAPI definition lives here:

```
http://localhost:5000/api/openapi.json
```

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t openapi_server .

# starting up a container
docker run -p 5000:5000 openapi_server
```

## Preparation
#### Environment variables
To run the application properly you need to se the following environment variables
| ENV | Purpose | Example |
| :--- | :---: | ---: |
| DB_HOST | Database host | `127.0.0.1` |
| DB_NAME | Name of the database | `lingo_trainer` |
| DB_PASS | Password of the database | `password` |
| DB_PORT | Port on witch the database is running | `5432` |
| DB_USER | User name your login in with  | `milo` |
| JWT_ALGORITHM | Algorithm in which the jwt token is encoded  | `SHA256` |
| JWT_ISSUER | Name of company/person who issues the jwt token | `hu.milo.project` |
| JWT_LIFETIME_SECONDS | The lifetime of the jwt toke (in seconds) | `60` == 1 minute |
| JW_SECRET | The secret number of string for the jwt token | `4321` |

#### Database
You need to have an PostgreSQL database to use for the application. <br>
Go to `openapi_server/test/setup.sql` for the SQL file. Run this in your database query 
and you have created the required database tables. Get the `DB_HOST`, `DB_NAME`, `DB_PASS`,
`DB_PORT` and the `DB_USER` and set those as your environment variables.

## Extra options
Add new dictionaries: first put the new dictionary in `~/assets/unfiltered_dictionaries`.
After run the following function:
```
python openapi_server/extentions/dictionary.py <DICTIONARY FILE NAME> <LANGUAGE NAME>

# Example
python openapi_server/extentions/dictionary.py "woorden" "NL"
```

## Analyse
To analyse code writing quality before committing:
```
# Run linter to check code
pylint --ignore-patterns=test_.*?py openapi_server

pyflakes openapi_server

mypy openapi_server --ignore-missing-imports


# Strict scanner that includes mulitple linters
prospector openapi_server 


# Security analysis
bandit -r openapi_server/core
```
If you want to Analyse the performance do the following:
```
# Create a profile file in your directory
python -m cProfile -o profile -m pytest openapi_server

# Open the python console and run the following
p = pstats.Stats('profile')
p.strip_dirs()
p.sort_stats('cumtime')
p.print_stats(50)
```
This will print the 50 lines that have the longest cumulative duration. <br>
If you want more lines change the 50 to the requested amount.

## Testing
To test the application and see multiple analytics use the following functions:

```
pip install coverage

# Run PyTest
coverage run --omit 'venv/*' -m pytest openapi_server

# Show coverage
coverage report
```
Pytest runs every test written in `openapi_server/test`. <br>
This directory contains `end to end`, `integrations` and `unit` testing.

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```

To launch all unit tests, use the following function:
```
pytest openapi_server/test/unit/
```

## Extra Information
| Criteria | Solution  |
| --- | --- |
|  Static analysis tools  |  `pylint`, `pyflakes`, `mypy`, `prospector`, `bandit` and also `sonarcloud`  |
|  Logger  |  I use heroku's build in logger to see what happens when the application is running  |
|  Security control |  I use `bandit` for my security control and also `sonarcloud`  |
|  Performance analyses |  I use `cProfile` see [Analyse](#analyse) |
|  Code coverage |  For my coverage badge I use `coverage-badge`, this generates a badge. |
