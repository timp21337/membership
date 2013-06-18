dropdb --user postgres membership
createdb --user postgres membership

./manage.py syncdb;
git push heroku_test master
heroku db:push --confirm wfolktest postgres://postgres:*@127.0.0.1:5432/membership

./manage.py load

git push heroku master

heroku db:push --confirm ifwfe postgres://postgres:*@127.0.0.1:5432/membership