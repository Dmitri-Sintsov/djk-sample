==========
djk-sample
==========

Sample Django project for django-jinja-knockout: https://github.com/Dmitri-Sintsov/django-jinja-knockout

Installation
------------

.. highlight:: shell

In Ubuntu 14.04 LTS::

    python3 -m venv djk_sample
    cd djk_sample
    source bin/activate
    git clone https://github.com/Dmitri-Sintsov/djk-sample.git
    cd djk-sample
    python3 -m pip install -U -r requirements.txt
    mkdir "$VIRTUAL_ENV/djk-sample/logs/"
    python manage.py makemigrations club_app
    python manage.py migrate
    python manage.py runserver

