from celery import Celery
from elasticsearch import Elasticsearch

elastic = Elasticsearch(host="elasticsearch", port="9200")
celery = Celery()
