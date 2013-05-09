dropdb --user postgres membership
createdb --user postgres membership

./manage.py syncdb;
./manage.py load

git push heroku master

/usr/bin/heroku db:push --confirm wfolktest postgres://postgres:*@127.0.0.1:5432/membership