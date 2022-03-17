web: gunicorn eshop.wsgi --log-file -
worker: celery -A EShop.celery worker -B --loglevel=info