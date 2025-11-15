# Celery Assignment 📚 ****[Demo](https://youtu.be/2a4Zi53JkBY)****
## what steps i have taken
1 udate python version to  3.12.10 from 3.10 and set it as default version <br>
2 create  <br>
3 install dependencies <br>
4 config database (mysql) <br>
5 add key for news api <br>

## how to run
<!-- celery -A app.celery_app.celery worker --loglevel=info -->
celery -A app.celery_app.celery worker --loglevel=info --pool=solo <br>
celery -A app.celery_app.celery beat --loglevel=info ## to run schedule task <br>
sudo service redis-server start <br>
fastapi dev app/main.py --host 0.0.0.0 --port 8000 <br>

## to check redis status 
sudo service redis-server status it should be active running <br>

