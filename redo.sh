#dropdb --user postgres membership
#createdb --user postgres membership
rm membership.sqlite3
./manage.py syncdb
./manage.py load
# ./manage.py runserver
