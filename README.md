Test Task (Django)
======

Used python 2.7 and django 1.8.7

Installation start guide
-----------------

Clone project from GitHub

    $ git  clone git@github.com:gowa66/Andrey_Gorshunow_test_livarava.git
    $ cd Andrey_Gorshunow_test_livarava

Install virtualenv

    $ pip install virtualenv
    $ virtualenv .env
    $ source .env/bin/activate

Install requirements

    $ pip install -r requirements.txt

Synch DB

    $ python manage.py syncdb --noinput
    $ python manage.py migrate notelist

Runserver

    $ python manage.py runserver