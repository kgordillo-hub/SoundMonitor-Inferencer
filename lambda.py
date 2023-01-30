# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 13:24:43 2023

@author: milam
"""

import json
import boto3

from inferencer.adapa_task5 import DcaseAdapatask5
import soundfile as sf
import io
import time

s3 = boto3.client('s3')

def handler(event, context):
    
    start_time = time.time()
    print('Welcome to inferencer...')
    inferencer = DcaseAdapatask5()
    
    
    print("Lambda execution Completed...!")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }