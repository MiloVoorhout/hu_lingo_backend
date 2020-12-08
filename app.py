#!/usr/bin/env python3
import connexion
import logging
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)
connexion_app = connexion.App(__name__)
CORS(connexion_app.app)
connexion_app.add_api('lingo/swagger/swagger.yaml')
app = connexion_app.app


if __name__ == '__main__':
    # run our standalone gevent server
    app.run(host='localhost', port=8080)
