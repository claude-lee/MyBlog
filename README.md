Blog

##########################################################

Blog in Python, with Django, social auth, south and Heroku

###########################################################

This is a simple blog that has posts, authors.

The blog

 - lists information
 - clicks through to a detailed page.

A user

 - is able to comment if logged in.
 - Django-social-auth for registering. (to be doone)
 - Python south is used for migrations.

The project is deployed to Heroku.


############################################################

First thing to do is to get all the required python packages.
Install them by running the following command.
Make sure you are in the project's root directory, the one with the file requirements.txt.

$ pip install -r requirements.txt

Then when you do some modifications on your app, do the following:

$ git add .

$ git commit -m "describing the update"

[$ heroku run ./manage.py syncdb # only first time, then use south]

###################################################################
$ ./manage.py schemamigration blog
$ git add blog/migrations/*
$ git commit -m 'adding new migrations for blog'
$ git push heroku master
$ heroku run ./manage.py migrate blog
#####################################################################
-> add 'south' to list of INSTALLED_APPS in settings.py

$ ./manage.py syncdb # Run syncdb locally:

$ ./manage.py convert_to_south django_app # Convert your project to use South:

-> modify models.py

$ ./manage.py schemamigration blog --auto # Set up the schema:

$ ./manage.py migrate blog # to perform the migration

$ add South==0.8.4 to requirements.txt

$ git add blog/migrations/* # tp add the blog/migrations directory to version control

$ git commit -m 'adding new migrations for blog' # to commit all changes

$ git push heroku master

$ heroku run python manage.py syncdb # to run syncdb on Heroku

$ heroku run python manage.py convert_to_south blog # to convert my Heroku instance of blog to use South


$ heroku run python manage.py migrate blog # to perform the migration

########################################################################

And what if I make further changes to myblog/blog/models.py?

$ python manage.py schemamigration blog --auto # to create the south migration file:

$ python manage.py migrate blog # to migrate locally

$ git add blog/migrations/* # tp add the blog/migrations directory to version control

$ git commit -m 'adding new migrations for blog' # to commit all changes

$ git push heroku master

$ heroku run python manage.py migrate blog # to migrate on Heroku


