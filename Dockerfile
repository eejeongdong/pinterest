FROM python:3.9.0

WORKDIR /home/

RUN git clone https://github.com/eejeongdong/pinterest.git

WORKDIR /home/pinterest/

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN echo "SECRET_KEY=django-insecure-w(e$$4t3z^&5$68q&9(j6sf&9ab#(vgwiwe_t$-==iht95+0*9" > .env

RUN python manage.py migrate

RUN python manage.py collectstatic

EXPOSE 8000

CMD ["gunicorn", "pragmatic.wsgi", "--bind", "0.0.0.0:8000"]