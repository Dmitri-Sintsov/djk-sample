==========
djk-sample
==========

.. _Firefox ESR: https://www.mozilla.org/en-US/firefox/organizations/

Sample Django project for django-jinja-knockout: https://github.com/Dmitri-Sintsov/django-jinja-knockout

Installation
------------

.. highlight:: shell

Ubuntu
~~~~~~

This is example for Ubuntu 14.04 LTS::

    sudo apt-get install libxml2-dev libxslt-dev
    python3 -m venv djk_sample
    cd djk_sample
    source bin/activate
    git clone https://github.com/Dmitri-Sintsov/djk-sample.git
    cd djk-sample
    python3 -m pip install -U -r requirements.txt
    mkdir "$VIRTUAL_ENV/djk-sample/logs/"
    python manage.py makemigrations club_app event_app
    python manage.py migrate
    python manage.py runserver

Windows
~~~~~~~

Example for Windows 32 bit.

* Download and install Python 3.4 or 3.5 (download and install KB2999226 if Python 3.5 installation freezes).
* Make sure ``python.exe`` / ``pip3.exe`` are in your `PATH`.
* Download appropriate lxml wheel from http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml for example:

  * ``lxml-3.4.4-cp34-none-win32.whl`` for Python 3.4.3 32 bit
  * ``lxml-3.6.4-cp35-cp35m-win32.whl`` for Python 3.5.2 32 bit

Then issue the following commands::

    python -m venv djk_sample
    cd djk_sample
    Scripts\activate.bat
    git clone https://github.com/Dmitri-Sintsov/djk-sample.git
    pip3 install --use-wheel --no-index lxml-3.4.4-cp34-none-win32.whl
    cd djk-sample
    pip3 install -r requirements.txt
    mkdir "%VIRTUAL_ENV%\djk-sample\logs"
    python manage.py makemigrations club_app event_app
    python manage.py migrate
    python manage.py runserver

Mac OS X
~~~~~~~~

Use brew:

* Install Python3 from http://brew.sh/
* Follow Ubuntu instructions with the exception that ``libxml2-dev`` ``libxslt-dev`` are already installed.

Selenium tests
--------------

Inside project virtual environment install selenium::

    pip3 install selenium

Install latest `Firefox ESR`_. Then run the following command::

    python manage.py test

Close Firefox window when the tests are complete. It should print the following message in console::

    OK
    Destroying test database for alias 'default'...
