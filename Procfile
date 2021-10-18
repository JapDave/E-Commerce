web: gunicorn EShop.wsgi --log-file -
worker: celery -A EShop worker -B --loglevel=info