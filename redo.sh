dropdb --user postgres membership
createdb --user postgres membership

./manage.py syncdb
./manage.py load
# ./manage.py runserver
