# Lingo trainer created with connexion
![Alt text](openapi_server/test/coverage.svg)


## Overview
This lingo trainer is a school project created for the course 'backend programming'. 
With the use of connexion I created an flask project that uses OpenAPI. [OpenAPI-Spec](https://openapis.org) 
from a remote server, you can easily generate a server stub. This is an example of building a OpenAPI-enabled Flask server.

This example uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

## Requirements
Python 3.5.2+

## Usage
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

## Environment variables
To run the application properly you need to se the following environment variables
| ENV | Purpose | Example |
| :--- | :---: | ---: |
| DB_HOST | Database host | `127.0.0.1` |
| DB_NAME | Name of the database | `lingo_trainer` |
| DB_PASS | Password of the database | `password` |
| DB_PORT | Port on witch the database is running | `5432` |

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t openapi_server .

# starting up a container
docker run -p 5000:5000 openapi_server
```

## Extra options
Add new dictionaries, first put the new dictionary in ~/assets/unfiltered_dictionaries.
After run the following function:
```
python openapi_server/extentions/dictionary.py <DICTIONARY FILE NAME> <LANGUAGE NAME>

# Example
python openapi_server/extentions/dictionary.py "woorden" "NL"
```

## Testing
To test code quality before committing:
```
# Run pylint to check code
pylint --ignore-patterns=test_.*?py openapi_server
```

To test the application and see multiple analytics use the following functions:

```
pip install coverage

# Run PyTest
coverage run --omit 'venv/*' -m pytest openapi_server

# Show coverage
coverage report
```

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```
