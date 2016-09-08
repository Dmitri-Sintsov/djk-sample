==========
djk-sample
==========

Sample Django project for django-jinja-knockout: https://github.com/Dmitri-Sintsov/django-jinja-knockout

Installation
------------

.. highlight:: shell

In Ubuntu 14.04 LTS::

    sudo apt-get install libxml2-dev libxslt-dev
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

In Windows:

* Make sure python.exe / pip3.exe are in your PATH.
* Download appropriate lxml wheel from http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
  (this example uses Python 3.4 for Windows 32 bit version of lxml).

Then issue the following commands::

    python -m venv djk_sample
    cd djk_sample
    Scripts\activate.bat
    git clone https://github.com/Dmitri-Sintsov/djk-sample.git
    pip3 install --use-wheel --no-index lxml-3.4.4-cp34-none-win32.whl
    cd djk-sample
    pip3 install -r requirements.txt
    mkdir "%VIRTUAL_ENV%\djk-sample\logs"
    python manage.py makemigrations club_app
    python manage.py migrate
    python manage.py runserver
