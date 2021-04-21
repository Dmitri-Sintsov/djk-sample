==========
djk-sample
==========

.. _Bootstrap 3: https://github.com/Dmitri-Sintsov/djk-bootstrap3
.. _Bootstrap 4: https://github.com/Dmitri-Sintsov/djk-bootstrap4
.. _Chrome: https://www.google.com/chrome/
.. _ChromeDriver: https://sites.google.com/a/chromium.org/chromedriver/
.. _Firefox ESR: https://www.mozilla.org/en-US/firefox/organizations/
.. _fixtures_order: https://github.com/Dmitri-Sintsov/djk-sample/search?l=Python&q=fixtures_order&utf8=%E2%9C%93
.. _geckodriver: https://github.com/mozilla/geckodriver/releases
.. _dump_data: https://github.com/Dmitri-Sintsov/djk-sample/search?l=Python&q=dump_data&utf8=%E2%9C%93
.. _has_fixture: https://github.com/Dmitri-Sintsov/djk-sample/search?l=Python&q=has_fixture&utf8=%E2%9C%93
.. _djk_sample/tests.py: https://github.com/Dmitri-Sintsov/djk-sample/blob/master/djk_sample/tests.py


Sample Django project for django-jinja-knockout: https://github.com/Dmitri-Sintsov/django-jinja-knockout

.. image:: https://circleci.com/gh/Dmitri-Sintsov/djk-sample.svg?style=shield
    :target: https://circleci.com/gh/Dmitri-Sintsov/djk-sample

.. image:: https://img.shields.io/travis/Dmitri-Sintsov/djk-sample.svg?style=flat
    :target: https://travis-ci.org/Dmitri-Sintsov/djk-sample

.. image:: http://www.icoph.org/img/ic-youtube.png
    :alt: Watch selenium tests recorded videos.
    :target: https://www.youtube.com/channel/UCZTrByxVSXdyW0z3e3qjTsQ

Screenshot:

.. image:: https://raw.githubusercontent.com/wiki/Dmitri-Sintsov/djk-sample/djk_change_or_create_foreign_key_for_inline_form.png
   :width: 740px

Recorded video: https://www.youtube.com/watch?v=CJLdtFaXhKo

Installation
------------

Ubuntu
~~~~~~

.. highlight:: shell

Tested in Ubuntu 20.04 LTS::

    sudo apt-get install git
    python3 -m venv djk-sample
    cd djk-sample
    source bin/activate
    git clone https://github.com/Dmitri-Sintsov/djk-sample.git
    cd djk-sample
	python3 -m pip install -U -r requirements.txt

To use the current stable `Bootstrap 3`_ version of ``djk_ui``::

    python3 -m pip install -U -r requirements/bs3.txt

To use the current stable `Bootstrap 4`_ version of ``djk_ui``::

    python3 -m pip install -U -r requirements/bs4.txt

then::

    mkdir "$VIRTUAL_ENV/djk-sample/logs/"
    mkdir "$VIRTUAL_ENV/djk-sample/fixtures/"
    python3 manage.py makemigrations club_app event_app
    python3 manage.py migrate
    python3 manage.py runserver

Shell scripts ``3bs.sh`` and ``4bs.sh`` allow to switch the Bootstrap version on the fly, using the development
(not always stable) version of ``djk_ui``.

Install Deno (optional)::

    curl -fsSL https://deno.land/x/install/install.sh | sh
    export DENO_INSTALL=$HOME/.deno


Windows
~~~~~~~

Windows x64 (x86 is similar but needs 32-bit versions of Python package wheels).

* Download and install Python 3.6, 3.7, 3.8 or 3.9.
* Make sure ``python.exe`` / ``pip3.exe`` are in your `PATH`.

Then issue the following commands::

    python -m venv djk-sample
    cd djk-sample
    Scripts\activate.bat
	python -m pip install -U pip
    git clone https://github.com/Dmitri-Sintsov/djk-sample.git
    cd djk-sample
	python -m pip install -U -r requirements.txt

To use the current stable `Bootstrap 3`_ version of ``djk_ui``::

    python -m pip install -U -r requirements\bs3.txt

To use the current stable `Bootstrap 4`_ version of ``djk_ui``::

    python -m pip install -U -r requirements\bs4.txt

then::

    mkdir "%VIRTUAL_ENV%\djk-sample\logs"
    mkdir "%VIRTUAL_ENV%\djk-sample\fixtures"
    python manage.py makemigrations club_app event_app
    python manage.py migrate
    python manage.py runserver

Shell scripts ``3bs.cmd`` and ``4bs.cmd`` allow to switch the Bootstrap version on the fly, using the development
(not always stable) version of ``djk_ui``.

Install Deno (optional)

Run PowerShell then invoke::

    iwr https://deno.land/x/install/install.ps1 -useb | iex

    set DENO_INSTALL=%userprofile%\.deno

environment variable.

Mac OS X
~~~~~~~~

Use brew:

* Install Python3 from https://brew.sh/
* Follow Ubuntu instructions.

Install Deno (optional)::

    brew install deno

Unit tests
----------

Selenium tests
~~~~~~~~~~~~~~

Inside project virtual environment install selenium 3.4 or newer::

    pip3 install -r dev-requirements.txt

To use `Bootstrap 3`_ version::

    ./3bs.sh

To use `Bootstrap 4`_ version::

    ./4bs.sh

django-jinja-knockout version 1.0.0 release tests were performed with:

* Python 3.8.2
* Ubuntu Linux 20.04LTS 64bit
* Selenium 3.141.0
* Chrome 81.0.4044.138 (Official Build) (64-bit)
* ChromeDriver 81.0.4044.138 (8c6c7ba89cc9453625af54f11fd83179e23450fa-refs/branch-heads/4044@{#999})
* Firefox 76.0.1 (64-bit)
* geckodriver 0.26.0 (e9783a644016 2019-10-10 13:38 +0000)

Selenium tests (Chrome, interactive)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Preferable method of interactive running Selenium tests is to use recent version of `Chrome`_ with compatible version of
`ChromeDriver`_. `ChromeDriver`_ binary should be extracted to one of the ``PATH`` directories or into
``$VIRTUAL_ENV/bin`` directory.

Install latest versions of `Chrome`_ / `ChromeDriver`_. Then run the following command::

    DJK_WEBDRIVER='selenium.webdriver.chrome.webdriver' python3 manage.py test

or, simply (will use default Selenium webdriver)::

    python3 manage.py test

Close ``Chrome`` window when the tests are complete. It should print the following message in the console::

    OK
    Destroying test database for alias 'default'...

Selenium tests (Firefox, interactive)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Not every version of `Firefox ESR`_ runs Selenium tests successfully due to bugs / incompatibilities of `geckodriver`_,
so it's not an recommended method to run interactive tests anymore, but one may try.

Selenium 3.0 or newer requires `geckodriver`_ to run with Firefox, which should be extracted to one of the ``PATH``
directories or into ``$VIRTUAL_ENV/bin`` directory.

Run the tests with the following command::

    DJK_WEBDRIVER='selenium.webdriver.firefox.webdriver' python3 manage.py test

Selenium tests (Chrome, remote shell)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using remote shell, one may install Xvfb::

    apt-get instal xvfb

to run tests in console this way::

    Xvfb :99 &
    export DISPLAY=:99
    python3 manage.py test

or this way::

    apt-get instal xvfb
    export DJK_WEBDRIVER='selenium.webdriver.chrome.webdriver'
    xvfb-run python3 manage.py test

See also:

* http://stackoverflow.com/questions/6183276/how-do-i-run-selenium-in-xvfb
* https://gist.github.com/alonisser/11192482

Selenium tests (headless Chrome)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Easiest way to run Selenium tests remotely is to use built-in headless Chrome driver. Headless mode is supported by
recent versions of Chrome browser::

    DJK_WEBDRIVER='django_jinja_knockout.webdriver.headless_chrome.webdriver' python3 manage.py test

Selenium test (Linux Chromium)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Linux Chromium usually is updated less often, providing more stable version of browser::

    DJK_WEBDRIVER='django_jinja_knockout.webdriver.chromium.webdriver' python3 manage.py test

Tox tests
~~~~~~~~~

Testing other Python versions with tox.

Note that python 3.5 tests requires tox 2.3.1 or newer version, while Ubuntu 14.04 LTS has older 1.6 version.
In such case install newer version of tox in the project virtual environment::

    pip3 install -U tox pip wheel setuptools

To run the test::

    tox -r -e py36-django-111-bs3

Tips
~~~~

To skip all or part of already executed tests uncomment one of ``# fixtures =`` definitions located before
`fixtures_order`_ list in `djk_sample/tests.py`_.

Newly introduced fixtures saved with `dump_data`_ Selenium command should be added in the proper place of
`fixtures_order`_ list to retain proper loading / checking order of the `has_fixture`_ method.
