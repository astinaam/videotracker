
### Setup environment variables


### Project setup
docker-compose up -d --build
docker-compose exec web python manage.py createsuperuser

### See logs
docker-compose logs 'db'
docker-compose logs 'web'
docker-compose logs 'celery'
docker-compose logs 'celery-beat'
docker-compose logs 'redis'
docker-compose logs 'dashboard'

### Monitor the background task
Visit http://localhost:5555

### Add more workers to the background task
docker-compose up -d --build --scale celery=3

### Super user
ytapp
ytapp@ytapp.com
123456
