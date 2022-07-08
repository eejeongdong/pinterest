FROM python:3.9.0

WORKDIR /home/

RUN echo "testing123"

RUN git clone https://github.com/eejeongdong/pinterest.git

WORKDIR /home/pinterest/

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient

# RUN export DJANGO_SETTINGS_MODULE=pragmatic.settings

EXPOSE 8000

CMD ["bash", "-c","python manage.py collectstatic --noinput --settings=pragmatic.settings.deploy && python manage.py migrate --settings=pragmatic.settings.deploy && gunicorn pragmatic.wsgi --env DJANGO_SETTINGS_MODULE=pragmatic.settings.deploy --bind 0.0.0.0:8000"]