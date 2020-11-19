#!/usr/bin/env python3
import connexion
import logging

logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('lingo/swagger/swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w lingo
application = app.app

if __name__ == '__main__':
    # run our standalone gevent server
    app.run(host='localhost', port=8080, server='gevent')
