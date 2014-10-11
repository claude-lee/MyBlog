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

> pip install -r requirements.txt

Then when you do some modifications on your app, do the following:

> git add .

> git commit -m "describing the update"

[> heroku run ./manage.py syncdb # only first time, then use south]

###################################################################
> ./manage.py schemamigration blog
> git add blog/migrations/*
> git commit -m 'adding new migrations for blog'
> git push heroku master
> heroku run ./manage.py migrate blog
#####################################################################
-> add 'south' to list of INSTALLED_APPS in settings.py

> ./manage.py syncdb # Run syncdb locally:

> ./manage.py convert_to_south django_app # Convert your project to use South:

-> modify models.py

> ./manage.py schemamigration blog --auto # Set up the schema:

> ./manage.py migrate blog # to perform the migration

> add South==0.8.4 to requirements.txt

> git add blog/migrations/* # tp add the blog/migrations directory to version control

> git commit -m 'adding new migrations for blog' # to commit all changes

> git push heroku master

> heroku run python manage.py syncdb # to run syncdb on Heroku

> heroku run python manage.py convert_to_south blog # to convert my Heroku instance of blog to use South


> heroku run python manage.py migrate blog # to perform the migration

########################################################################

And what if I make further changes to myblog/blog/models.py?

> python manage.py schemamigration blog --auto # to create the south migration file:

> python manage.py migrate blog # to migrate locally

> git add blog/migrations/* # tp add the blog/migrations directory to version control

> git commit -m 'adding new migrations for blog' # to commit all changes

> git push heroku master

> heroku run python manage.py migrate blog # to migrate on Heroku


#########################

to trouble shoot run

> heroku logs

#########################

1. > ./manage.py syncdb OR > ./manage.py migrate blog
-> File "/Users/claude/PycharmProjects/MyDjango/myblog/venv/lib/python2.7/site-packages/django/db/backends/dummy/base.py",
line 15, in complain
    raise ImproperlyConfigured("settings.DATABASES is improperly configured. "
django.core.exceptions.ImproperlyConfigured: settings.DATABASES is improperly configured.
Please supply the ENGINE value. Check settings documentation for more details.



#########################

2. heroku run python manage.py migrate blog/migrations/0003_auto__add_field_comment_tag.py
 File "/app/.heroku/python/lib/python2.7/site-packages/django/db/models/loading.py", line 190, in get_app
    raise ImproperlyConfigured("App with label %s could not be found" % app_label)
django.core.exceptions.ImproperlyConfigured: App with label py could not be found
SOLVED: run
> heroku run python manage.py migrate blog 0003
instead

#################################################
3. heroku run python manage.py migrate blog 0003
 - Soft matched migration 0003 to 0003_auto__add_field_comment_tag.
Running migrations for blog:
 - Migrating forwards to 0003_auto__add_field_comment_tag.
 > blog:0001_initial
FATAL ERROR - The following SQL query failed: CREATE TABLE "blog_entry" ("id" serial NOT NULL PRIMARY KEY, "title" varchar(500) NOT NULL, "author_id" integer NOT NULL, "body" text NOT NULL, "created_at" timestamp with time zone NOT NULL, "modified_at" timestamp with time zone NOT NULL)
The error was: relation "blog_entry" already exists
SOLVED??
> heroku run python manage.py migrate blog 0003 --fake

###################################################
4. heroku logs
OSError: [Errno 2] No such file or directory: '/app/myblog/static'
python ./manage.py collectstatic --noinput

django-blog-app::NAVY-> \d
                           List of relations
 Schema |               Name                |   Type   |     Owner
--------+-----------------------------------+----------+----------------
 public | auth_group                        | table    | bbkejnajxeggkb
 public | auth_group_id_seq                 | sequence | bbkejnajxeggkb
 public | auth_group_permissions            | table    | bbkejnajxeggkb
 public | auth_group_permissions_id_seq     | sequence | bbkejnajxeggkb
 public | auth_permission                   | table    | bbkejnajxeggkb
 public | auth_permission_id_seq            | sequence | bbkejnajxeggkb
 public | auth_user                         | table    | bbkejnajxeggkb
 public | auth_user_groups                  | table    | bbkejnajxeggkb
 public | auth_user_groups_id_seq           | sequence | bbkejnajxeggkb
 public | auth_user_id_seq                  | sequence | bbkejnajxeggkb
 public | auth_user_user_permissions        | table    | bbkejnajxeggkb
 public | auth_user_user_permissions_id_seq | sequence | bbkejnajxeggkb
 public | blog_comment                      | table    | bbkejnajxeggkb
 public | blog_comment_id_seq               | sequence | bbkejnajxeggkb
 public | blog_entry                        | table    | bbkejnajxeggkb
 public | blog_entry_id_seq                 | sequence | bbkejnajxeggkb
 public | django_admin_log                  | table    | bbkejnajxeggkb
 public | django_admin_log_id_seq           | sequence | bbkejnajxeggkb
 public | django_content_type               | table    | bbkejnajxeggkb
 public | django_content_type_id_seq        | sequence | bbkejnajxeggkb
 public | django_migrations                 | table    | bbkejnajxeggkb
 public | django_migrations_id_seq          | sequence | bbkejnajxeggkb
 public | django_session                    | table    | bbkejnajxeggkb
(23 rows)

################################################################################

heroku run python manage.py syncdb
Running `python manage.py syncdb` attached to terminal... up, run.8224
Syncing...
Creating tables ...
Creating table south_migrationhistory
Installing custom SQL ...
Installing indexes ...
Installed 0 object(s) from 0 fixture(s)

Synced:
 > django.contrib.admin
 > django.contrib.auth
 > django.contrib.contenttypes
 > django.contrib.sessions
 > django.contrib.messages
 > django.contrib.staticfiles
 > south

Not synced (use migrations):
 - blog
 - social_auth
(use ./manage.py migrate to migrate these)

###############################
heroku scale web=1