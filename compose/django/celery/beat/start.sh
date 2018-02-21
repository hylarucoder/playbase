#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

sleep 3

rm -f './celerybeat.pid'
celery -A yadjangoblog.yataskapp beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
