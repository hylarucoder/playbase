from celery import Celery
from elasticsearch import Elasticsearch
from werkzeug.local import Local

elastic = Elasticsearch(host="elasticsearch", port="9200")
celery = Celery()
# g just like flask.g
g = Local()
