   web: gunicorn eshop.wsgi --log-file -
   worker: celery -A eshop.celery worker -B --loglevel=info