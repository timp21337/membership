membership
==========

A Woodcraft Folk Session System.


Requires https://github.com/holiture/heroku-buildpack-tex

Setup
-----
    apt-get install postgresql-server-dev-all
    apt-get install python-dev
    pip install -r /home/timp/git/membership/requirements.txt

Enables commands such as:

./manage.py summary attendees elfinCamp2013
./manage.py output attendees elfinCamp2013