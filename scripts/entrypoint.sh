#!/bin/bash
/app/scripts/wait_for.sh ofd_agregator_redis:6379 -t 15 -- echo "Redis (ofd_agregator_redis) is up!"

python /app/manage.py buildapp --profile development

python /app/manage.py runserver 0.0.0.0:8000
