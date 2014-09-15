membership
==========

A Woodcraft Folk Session System.


Requires https://github.com/holiture/heroku-buildpack-tex

Setup
-----
    sudo apt-get install postgresql-server-dev-9.3
    sudo apt-get install python-dev
    sudo pip install -r /home/timp/git/membership/requirements.txt
    sudo ln -s ~/Dropbox/git/membership/load.py members/management/commands/


Enables commands such as:

    ./manage.py summary attendees elfinCamp2013
    ./manage.py output attendees elfinCamp2013