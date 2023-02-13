# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 13:24:43 2023

@author: kgordillo
"""

import json
import boto3
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

s3 = boto3.client("s3")

application.logger.setLevel(logging.DEBUG)

@application.route("/identifySound", methods=["POST"])
def identify_sound():
    
    start_time = time.time()
    logging.debug('Inferenciador iniciado...')
    
    response = None
    
    if request.json is None:
        # Expect application/json request
        response = Response("Empty request", status=415)
    else:
        request_content = json.loads(request.data)
        message = dict()
        try:
            content_json = json.loads(request_content["Message"])

            if request_content["TopicArn"] and request_content["Message"]:
                message = content_json["Records"][0]["s3"]
            else:
                message = request_content
                
            bucket = message["bucket"]["name"]
            archivo = message["object"]["key"]
            
            tmp_prnt = "Descargar el archivo: "+ archivo + " del bucket: " + bucket
            
            out_file_path='/tmp/'+str(archivo)
            logging.warn(tmp_prnt)

            s3.download_file(Bucket = bucket, Key = archivo, Filename = out_file_path)
            
            logging.warn("Inicializa el inferenciador")
               
            inferencer = DcaseAdapatask5()
            
            
            with open(out_file_path, 'rb') as audio:
                data, samplerate = sf.read(io.BytesIO(audio.read()))
            
            result = inferencer.run_inferencer(archivo, data, samplerate)
            result_json = result.to_json()
            logging.warn(result_json)
            logging.warn("Finaliza el inferenciador")
            
            
            sns_client = boto3.client("sns", region_name='us-east-1')
            
            processing_time = (time.time() - start_time)
            
            service_response = {'ProcessingTime_seconds' : processing_time, 'Inferencer_result' : result_json}
            
            logging.warn("Service response to send SNS....")
            logging.warn(service_response)
            
            response = sns_client.publish(
            TopicArn = "arn:aws:sns:us-east-1:703106094997:audio_result_event",
            Message = json.dumps({'statusCode': 200, 'body': service_response})
            )
            
            logging.warn("Response from SNS")
            logging.warn(response)
            #response = Response("", status=200)
        except Exception as ex:
            sns_client = boto3.client("sns", region_name='us-east-1')
            response = sns_client.publish(
               TopicArn = "arn:aws:sns:us-east-1:703106094997:audio_error_topic",
               Message = json.dumps({'statusCode': 500, 'error_processing': request.json})
            )
            logging.exception("Error processing message: %s" % request.json)
            logging.exception(ex)
            #response = Response(ex.message, status=500)
    
    return response

@application.route("/")
def print_hello():
    response = Response("Hello", status=200)
    return response

if __name__ == "__main__":
    application.run(host="0.0.0.0")