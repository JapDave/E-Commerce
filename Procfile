web: gunicorn EShop.wsgi --log-file -
worker: celery -A EShop worker -l info -c 4