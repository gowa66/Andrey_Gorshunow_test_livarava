Test Task (Django)
======

Used python 2.7 and django 1.8.7

Installation start guide
-----------------

Clone project from GitHub

    $ git  clone git@github.com:gowa66/Django_test_LR.git
    $ cd Django_test_LR

Install virtualenv

	$ pip install virtualenv
	$ virtualenv .env
	$ source .env/bin/activate

Install requirements

	$ pip install -r requirements

Synch DB

	$ python manage.py migrate
	$ python manage.py createsuperuser
	$ python manage.py syncdb

Runserver

	$ python manage.py runserver