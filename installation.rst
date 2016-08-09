.. highlight:: shell

Installation for Ubuntu 14.04 LTS::

    python3 -m venv djk_sample
    cd djk_sample
    source bin/activate
    git clone https://github.com/Dmitri-Sintsov/djk-sample.git
    cd djk-sample
    python3 -m pip install -U -r requirements.txt
    python manage.py makemigrations club_app
    python manage.py migrate
    python manage.py runserver
