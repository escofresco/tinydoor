release: python manage.py migrate
<<<<<<< HEAD
web: gunicorn config.wsgi:application
worker: celery worker --app=config.celery_app --loglevel=info
=======
web: gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
worker: celery worker --app=config.celery_app --loglevel=info
beat: celery beat --app=config.celery_app --loglevel=info
>>>>>>> dd4fd56341cdf9156f4b0a7016225b2ebdc82048
