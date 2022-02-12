FROM python:3.8-alpine

WORKDIR /home/app
COPY . /home/app/
RUN pip install django
RUN python manage.py migrate

ENTRYPOINT ["python", "./manage.py", "runserver"]
