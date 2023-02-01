# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 13:24:43 2023

@author: kgordillo
"""

import json
#import boto3
import logging


from inferencer.adapa_task5 import DcaseAdapatask5
import soundfile as sf
import io
import time


import flask
from flask import Response, request


application = flask.Flask(__name__)
application.config.from_object("default_config")
application.debug = application.config["FLASK_DEBUG"] in ["true", "True"]

#s3 = boto3.client('s3')

@application.route("/identifySound", methods=["POST"])
def identify_sound():
    
    start_time = time.time()
    print('Welcome to inferencer...')
    
    response = None
    
    if request.json is None:
        # Expect application/json request
        response = Response("Empty request", status=415)
    else:
        request_content = json.loads(request.data)
        message = dict()
        try:
            message = request_content
            inferencer = DcaseAdapatask5()
            print('Inferenciador iniciado...')
            response = Response("", status=200)
        except Exception as ex:
            logging.exception("Error processing message: %s" % request.json)
            print('"Error processing message: %s" % request.json')
            response = Response(ex.message, status=500)
    
    return response

@application.route("/")
def print_hello():
    response = Response("Hello", status=200)
    return response

if __name__ == "__main__":
    application.run(host="0.0.0.0")