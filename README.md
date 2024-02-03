# Zelf Hackathon Backend


## Commands
Run Docker Services
```
docker compose up -d
```

Run Server
```
python manage.py runserver
```

Run Celery Worker
```
celery -A core.celery flower --port=5555
```

Run Celery Beat Worker
```
celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```