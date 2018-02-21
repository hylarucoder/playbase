FROM base-ubuntu:0.1

# Sane defaults for pip
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PYTHONUNBUFFERED 1

RUN ln -s /usr/bin/pip3 /usr/bin/pip && ln -s /usr/bin/python3 /usr/bin/python
# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements

# --no-cache-dir
RUN pip install -r /requirements/local.txt -i https://pypi.doubanio.com/simple

COPY ./compose/django/celery/worker/start.sh /start-celeryworker.sh
RUN sed -i 's/\r//' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh

COPY ./compose/django/celery/beat/start.sh /start-celerybeat.sh
RUN sed -i 's/\r//' /start-celerybeat.sh
RUN chmod +x /start-celerybeat.sh

COPY ./compose/django/celery/flower/start.sh /start-celeryflower.sh
RUN sed -i 's/\r//' /start-celeryflower.sh
RUN chmod +x /start-celeryflower.sh

COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./compose/django/start-dev.sh /start-dev.sh
RUN sed -i 's/\r//' /start-dev.sh
RUN chmod +x /start-dev.sh

WORKDIR /webapp

ENTRYPOINT ["/entrypoint.sh"]
