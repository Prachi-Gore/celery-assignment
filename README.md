# what steps i have taken
1 udate python version to  3.12.10 from 3.10 and set it as default version
2 create venv
3 install dependencies
4 config database (mysql)
5 add key for news api

# how to run
<!-- celery -A app.celery_app.celery worker --loglevel=info -->
celery -A app.celery_app.celery worker --loglevel=info --pool=solo
celery -A app.celery_app.celery beat --loglevel=info ## to run schedule task
sudo service redis-server start
fastapi dev app/main.py --host 0.0.0.0 --port 8000

# to check redis status 
sudo service redis-server status it should be active running

