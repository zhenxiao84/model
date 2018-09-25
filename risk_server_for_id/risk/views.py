# Create your views here.
import gzip
import json
import logging
import os
import zlib
import uuid
import datetime
import requests
from .feat import Feat
from . import v1
from risk.models import Request, ExecInfo
from risk.response.response import get_response
from django.http import HttpResponse
import datetime

import traceback

system_logger = logging.getLogger('system_log')
business_logger = logging.getLogger('business_log')

request_files_path = "request_files"

def risk_for_gzip(request):
    try:
        body = gzip.decompress(request.body).decode('utf-8')
    except:
        system_logger.exception('gzip decompress error!')
        return HttpResponse(get_response(-1, 'gzip decompress error', None, None, None).to_str())

    return risk_calc(request.method, body)

def risk(request):
    body = request.body.decode('utf-8')
    return risk_calc(request.method, body)

def risk_calc(method, body):
    if method != 'POST':
        return HttpResponse(get_response(-1, 'request method is not post', None, None, None).to_str())
    try:
        json_body = json.loads(body)
    except:
        system_logger.exception('request body json loads error!')
        return HttpResponse(get_response(-1, 'request body json loads error', None, None, None).to_str())
    
    request_id = '%s-%s' % (datetime.datetime.now().strftime('%Y%m%d%H%M%S'), str(uuid.uuid1()))

    if 'model_name' not in json_body:
        system_logger.error('request body model_name is missing!')
        return HttpResponse(get_reponse(-1, 'request body model_name is missing', None, None, None).to_str())
    model_name = json_body['model_name']
   
    if 'customer_id' not in json_body:
        system_logger.error('request body customer_id is missing!')
        return HttpResponse(get_response(-1, 'request body customer_id is missing', None, None, None).to_str()) 
    customer_id = json_body['customer_id']

    request_file_save(request_id, body)
    business_logger.info('[Request] request_id:%s, model_name:%s, customer_id:%s', request_id, model_name, customer_id)
    request_save(request_id, model_name, customer_id) 
    return risk_router(request_id, model_name, customer_id)

def request_save(request_id, model_name, customer_id):
    request = Request(request_id=request_id, model_name=model_name, customer_id=customer_id)
    request.save()

def request_file_save(request_id, body):
    request_file_name = '%s.gz' % (request_id, )
    with gzip.open(os.path.join(request_files_path, request_file_name), 'wt', encoding='utf-8') as fp:
        fp.write(body)

def risk_router(request_id, model_name, customer_id, json_body):
    if model_name == 'v1':
        response = v1.execute(request_id, json_body)
    else:
        repsonse = get_response('model_name is not valid', None, None, None)

    business_logger.info('[Result] request_id:%s, model_name:%s, customer_id:%s, response:%s', request_id, model_name, customer_id, response.to_str())
    return HttpResponse(response.to_str())
