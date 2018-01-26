#!/usr/bin/python

import sys
import json
import collections
import time

from flask import Flask, request
from engine import classify, load_resources
from werkzeug.wsgi import LimitedStream

reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)
app.config.from_object('config')

# Use this metod to create nested JSON
def tree():
    return collections.defaultdict(tree)

# Begin routing
@app.route('/classify', methods=['POST'])
def getarticle():

    # Get the item
    article_post = str(request.form['post'].lower())

    start_time = time.time()
    # Begin prediction
    label = classify(article_post)

    # Create the JSON from the returned prediction value
    data = tree()
    data['article'] = article_post
    data['label'] = label
    data['process_time'] = process_time(start_time)
    data = json.dumps(data)

    # Get item detail from Facetly
    returnValue = data

    # Return the value back to the web
    return(returnValue, 201)

def process_time(start_time):
    process = time.strftime('%H:%M:%S', time.gmtime((time.time() - start_time)))
    return process

class StreamConsumingMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        stream = LimitedStream(environ['wsgi.input'],
                               int(environ['CONTENT_LENGTH'] or 0))
        environ['wsgi.input'] = stream
        app_iter = self.app(environ, start_response)
        try:
            stream.exhaust()
            for event in app_iter:
                yield event
        finally:
            if hasattr(app_iter, 'close'):
                app_iter.close()

if __name__ == '__main__':


    app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)

    # Load pickle resources first
    load_resources()

    # app.run(host="127.0.0.1", port=1234, debug=True)
    app.run(host="0.0.0.0", port=5050, debug=True)


