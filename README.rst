==========
djk-sample
==========

.. _Bootstrap 3: https://github.com/Dmitri-Sintsov/djk-bootstrap3
.. _Bootstrap 4: https://github.com/Dmitri-Sintsov/djk-bootstrap4
.. _Bootstrap 5: https://github.com/Dmitri-Sintsov/djk-bootstrap5
.. _Chrome: https://www.google.com/chrome/
.. _ChromeDriver: https://sites.google.com/a/chromium.org/chromedriver/
.. _cherry_django.sh: https://github.com/Dmitri-Sintsov/djk-sample/blob/master/cli/cherry_django.sh
.. _Firefox ESR: https://www.mozilla.org/en-US/firefox/organizations/
.. _fixtures_order: https://github.com/Dmitri-Sintsov/djk-sample/search?l=Python&q=fixtures_order&utf8=%E2%9C%93
.. _geckodriver: https://github.com/mozilla/geckodriver/releases
.. _django_deno: https://github.com/Dmitri-Sintsov/django-deno
.. _deno rollup: https://deno.land/x/drollup
.. _settings.py: https://github.com/Dmitri-Sintsov/djk-sample/blob/master/djk_sample/settings.py
.. _system.js: https://github.com/systemjs/systemjs
.. _dump_data: https://github.com/Dmitri-Sintsov/djk-sample/search?l=Python&q=dump_data&utf8=%E2%9C%93
.. _has_fixture: https://github.com/Dmitri-Sintsov/djk-sample/search?l=Python&q=has_fixture&utf8=%E2%9C%93
.. _djk_sample/tests.py: https://github.com/Dmitri-Sintsov/djk-sample/blob/master/djk_sample/tests.py
.. _terser: https://github.com/terser/terser


Sample Django project for django-jinja-knockout: https://github.com/Dmitri-Sintsov/django-jinja-knockout

.. image:: https://circleci.com/gh/Dmitri-Sintsov/djk-sample.svg?style=shield
    :target: https://circleci.com/gh/Dmitri-Sintsov/djk-sample
..
   https://iconarchive.com/show/android-lollipop-icons-by-dtafalonso/Youtube-icon.html
.. image:: https://icons.iconarchive.com/icons/dtafalonso/android-lollipop/24/Youtube-icon.png
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
    # Uncomment next line to use v2.2.0 instead of development version:
    # git checkout tags/v2.2.0
    python3 -m pip install -U -r requirements.txt

To use the current stable `Bootstrap 3`_ version of ``djk_ui``::

    python3 -m pip install -U -r requirements/bs3.txt

or::

    python3 -m pip install -U wheel/djk_bootstrap3-2.2.0-py2.py3-none-any.whl

To use the current stable `Bootstrap 4`_ version of ``djk_ui``::

    python3 -m pip install -U -r requirements/bs4.txt

or::

    python3 -m pip install -U wheel/djk_bootstrap4-2.2.0-py2.py3-none-any.whl

To use the development `Bootstrap 3`_ version::

    ./cli/3bs.sh

To use the development `Bootstrap 4`_ version::

    ./cli/4bs.sh

To use the development `Bootstrap 5`_ version::

    ./cli/5bs.sh

then::

    mkdir "$VIRTUAL_ENV/djk-sample/logs/"
    mkdir "$VIRTUAL_ENV/djk-sample/fixtures/"
    python3 manage.py makemigrations club_app event_app
    python3 manage.py migrate
    apt install gettext
    python3 manage.py compilemessages
    python3 manage.py runserver

Shell scripts ``cli/3bs.sh`` / ``cli/4bs.sh`` / ``cli/5bs.sh`` allow to switch the Bootstrap version on the fly, using the development
(not always stable) version of ``djk_ui``.

Install Deno (optional)::

    curl -fsSL https://deno.land/x/install/install.sh | sh
    export DENO_INSTALL=$HOME/.deno


Windows
~~~~~~~

Windows x64 (x86 is similar but needs 32-bit versions of Python package wheels).

* Download and install Python 3.9 / 3.10 / 3.11.
* Make sure ``python.exe`` / ``pip3.exe`` are in your `PATH`.

Then issue the following commands::

    python -m venv djk-sample
    cd djk-sample
    Scripts\activate.bat
    python -m pip install -U pip
    git clone https://github.com/Dmitri-Sintsov/djk-sample.git
    cd djk-sample
    rem Uncomment next line to use v2.2.0 instead of development version:
    rem git checkout tags/v2.2.0
    python -m pip install -U -r requirements.txt

To use the current stable `Bootstrap 3`_ version of ``djk_ui``::

    python -m pip install -U -r requirements\bs3.txt

To use the current stable `Bootstrap 4`_ version of ``djk_ui``::

    python -m pip install -U -r requirements\bs4.txt

To use the development `Bootstrap 3`_ version::

    cli\3bs.cmd

To use the development `Bootstrap 4`_ version::

    cli\4bs.cmd

To use the development `Bootstrap 5`_ version::

    cli\5bs.cmd

then::

    mkdir "%VIRTUAL_ENV%\djk-sample\logs"
    mkdir "%VIRTUAL_ENV%\djk-sample\fixtures"
    python manage.py makemigrations club_app event_app
    python manage.py migrate
    python manage.py compilemessages
    python manage.py runserver

Shell scripts ``cli\3bs.cmd`` / ``cli\4bs.cmd`` / ``cli\5bs.cmd`` allow to switch the Bootstrap version on the fly, using the development
(not always stable) version of ``djk_ui``.

Install Deno (optional)

Run PowerShell then invoke::

    irm https://deno.land/install.ps1 | iex

    set DENO_INSTALL=%userprofile%\.deno

set the environment variable.

Mac OS X
~~~~~~~~

Use brew:

* Install Python3 from https://brew.sh/
* Follow Ubuntu instructions.

Install Deno (optional)::

    brew install deno

deno rollup bundle
------------------
Since django-jinja-knockout v2, `django_deno`_ could be used to generate / run Javascript bundle.

`django_deno`_ dependence is optional and is required only to run with old browsers (eg. IE11)
or to create minimized production mode bundle.

`deno rollup`_ and `system.js`_ are used internally to create / load the production mode bundle.

* Use ``manage.py runrollup`` command to debug with old browsers (eg. IE11)
* Use ``manage.py collectrollup`` command to create minimized bundle, compatible to old browsers
* Use ``cli/cherry_django.sh`` to test generated bundle locally (emulation of production).

It's also possible to generate es6 minimized bundle to use with modern browsers (no IE11), with the following
``DENO_OUTPUT_MODULE_TYPE`` value in `settings.py`_::

    DENO_OUTPUT_MODULE_TYPE = 'module'

To automatically create the production Javascript bundle::

    ./cli/collectrollup.sh

To run test server after the bundle has been created::

    ./cli/cherry_django.sh

`terser`_ is used to minimize the bundle. To create non-minimized bundle, one may turn off terser in `settings.py`_::

    DENO_ROLLUP_COLLECT_OPTIONS = {
        'terser': False,
    }

``DJANGO_DEBUG`` and ``CHERRYPY_STATIC`` environment variables are used by `settings.py`_ to select the debug /
production version of Javascript code, for example in the deno production script `cherry_django.sh`_::

    DJANGO_DEBUG='False'
    CHERRYPY_STATIC='True'

Unit tests
----------

Selenium tests
~~~~~~~~~~~~~~

Inside project virtual environment install selenium 3.4 or newer::

    pip3 install -r ./requirements/test.txt

To use `Bootstrap 3`_ version::

    ./cli/3bs.sh

To use `Bootstrap 4`_ version::

    ./cli/4bs.sh

To use `Bootstrap 5`_ version::

    ./cli/5bs.sh

``django-jinja-knockout`` version 2.2.0 release tests were performed with:

* Linux fv-az247-370 5.15.0-1035-azure #42-Ubuntu SMP Tue Feb 28 19:41:23 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
* Ubuntu 22.04.2 LTS
* Python 3.11.3
* Google Chrome 112.0.5615.121
* ChromeDriver 112.0.5615.49 (bd2a7bcb881c11e8cfe3078709382934e3916914-refs/branch-heads/5615@{#936})

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
