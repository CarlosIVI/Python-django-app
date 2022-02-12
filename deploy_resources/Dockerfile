FROM python:3.8-alpine

WORKDIR /home/app
COPY . /home/app/
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "./manage.py", "runserver"]