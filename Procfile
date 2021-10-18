web: gunicorn EShop.wsgi --log-file -
worker: celery -A EShop.celery worker -B --loglevel=info