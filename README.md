membership
==========

A Woodcraft Folk Session System.


Requires https://github.com/holiture/heroku-buildpack-tex

Ubuntu Setup
------------
    apt-get install postgresql-server-dev-all
    apt-get install python-dev
    pip install virtualenv
    virtualenv venv
    source venv/bin/activate
    pip install -r /home/timp/git/membership/requirements.txt
    ln -s ~/Dropbox/git/membership/load.py members/management/commands/
    ./redo.sh

Enables commands such as:

    ./manage.py output elfins
    ./manage.py summary elfins
    ./manage.py summary waiters
    ./manage.py summary attendees elfinCamp2013
    ./manage.py output attendees elfinCamp2013
    ./manage.py csv elfins > elfins.csv



Docker
------
     sudo usermod -a -G docker username
     docker build -t members .
     docker run -v /home/timp/git/membership/rerts:/membership/reports -it -p 8000:8000 members  ./manage.py runserver
     docker run -v ${PWD}/reports:/membership/reports -it -p 8000:8000 members  ./manage.py runserver 0.0.0.0:8000
 

