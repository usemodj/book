## Run App

$ source venv/bin/activate

To run the application under Gunicorn, use the following command:
(venv) $ gunicorn manage:app

---------------------

$ cd flasky

$ virtualenv venv

$ source venv/bin/activate

(venv) $ deactivate

## To install Flask into the virtual environment, use the following command:

(venv) $ pip install flask
OR
$ sudo pip install flask

## Command-Line Options with Flask-Script
Flask-script Install
(venv) $ pip install flask-script

## Flask-Bootstrap can be installed with pip:

(venv) $ pip install flask-bootstrap

hello.py: Flask-Bootstrap initialization
from flask.ext.bootstrap import Bootstrap
# ...
bootstrap = Bootstrap(app)

## Flask-Moment is installed
with pip:
(venv) $ pip install flask-moment

templates/base.html: 

	{% block scripts %}
	{{ super() }}
	{{ moment.include_moment() }}
	{{ moment.locale('ko') }}
	{% endblock %}

templates/index.html:

	{% extends "base.html" %}

	{% block title %}Flasky{% endblock %}

	{% block page_content %}
	<div class="page-header">
	    <h1>Hello World!</h1>
	</div>

	<p>The local date and time is {{ moment(current_time).format('LLL') }}.</p>
	<p>That was {{ moment(current_time).fromNow(refresh=True) }} </p>
	{% endblock %}


## Web Forms

Flask-WTF and its dependencies can be installed with pip:
(venv) $ pip install flask-wtf

hello.py: Flask-WTF configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

## Database

Flask-SQLAlchemy is installed with pip:
(venv) $ pip install flask-sqlalchemy
(venv) $ pip install  pymysql
### hello.py: Database configuration

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
'mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

### Creating the Tables
(venv) $ python hello.py shell
>>> from hello import db
>>> db.create_all()

To chage tables;
>>> db.drop_all()
>>> db.create_all()

### Creating a Migration Repository
(venv) $ pip install flask-migrate

hello.py: Flask-Migrate configuration:

	from flask.ext.migrate import Migrate, MigrateCommand
	# ...
	migrate = Migrate(app, db)
	manager.add_command('db', MigrateCommand)

to create a migration repository with the init subcommand:
(venv) $ python hello.py db init

creates an automatic migration script:
(venv) $ python hello.py db migrate -m "initial migration"

## Email Support with Flask-Mail
Flask-Mail is installed with pip:

(venv) $ pip install flask-mail

hello.py: Flask-Mail configuration for Gmail
	import os
	# ...
	app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
	app.config['MAIL_PORT'] = 587
	app.config['MAIL_USE_TLS'] = True
	app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
	app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

hello.py: Flask-Mail initialization
from flask.ext.mail import Mail
mail = Mail(app)

(venv) $ export MAIL_USERNAME=<Gmail username>
(venv) $ export MAIL_PASSWORD=<Gmail password>
For Microsoft Windows users, the environment variables are set as follows:
(venv) $ set MAIL_USERNAME=<Gmail username>
(venv) $ set MAIL_PASSWORD=<Gmail password>


## User Authentication with Flask-Login
(venv) $ pip install flask-login

## Requirements File
(venv) $ pip freeze >requirements.txt


## To Database migrate
to create a migration repository with the init subcommand:
(venv) $ python hello.py db init

creates an automatic migration script:
(venv) $ python hello.py db migrate -m "initial migration"

(venv) $ python manage.py db upgrade

to create user
(venv) $ python manage.py shell
>>> u = User(email='john@example.com', username='john', password='cat')
>>> db.session.add(u)
>>> db.session.commit()


To ensure that you have all the dependencies installed, also run 

pip install -r requirements.txt


## Creating Fake Blog Post Data
(venv) $ pip install forgerypy

## Rich-Text Posts with Markdown and Flask-PageDown
(venv) $ pip install flask-pagedown markdown bleach

• PageDown, a client-side Markdown-to-HTML converter implemented in Java‐
Script.
• Flask-PageDown, a PageDown wrapper for Flask that integrates PageDown with
Flask-WTF forms.
• Markdown, a server-side Markdown-to-HTML converter implemented in Python.
• Bleach, an HTML sanitizer implemented in Python.

## Flask-HTTPAuth is installed with pip:
(venv) $ pip install flask-httpauth

## Testing Web Services with HTTPie
(venv) $ pip install httpie

(venv) $ http --json --auth <email>:<password> GET http://127.0.0.1:5000/api/v1.0/posts/

add a new blog post:
(venv) $ http --auth <email>:<password> --json POST \
> http://127.0.0.1:5000/api/v1.0/posts/ \
> "body=I'm adding a post from the *command line*."

To use authentication tokens, a request to /api/v1.0/token is sent:
(venv) $ http --auth <email>:<password> --json GET http://127.0.0.1:5000/api/v1.0/token

## Obtaining Code Coverage Reports
(venv) $ pip install coverage

An example of the text-based report follows:
(venv) $ python manage.py test --coverage

## End-to-End Testing with Selenium
(venv) $ pip install selenium

## Running a production web server
(venv) $ pip install gunicorn

To run the application under Gunicorn, use the following command:
(venv) $ gunicorn manage:app

-----------------
## MultiCheckboxField

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RoomBookingForm(Form):
    #room_id = HiddenField('Room ID')
    booking = MultiCheckboxField('room')
    def __init__(self, data, *args, **kwargs):
        super(RoomBookingForm, self).__init__(*args, **kwargs)
        self.booking.choices = data;

views.py:
booking_form = RoomBookingForm([(room.id, room.number) for (room, book) in reservations])
        
       
## Flask-Social

pip install Flask-Social

Then install your provider API libraries.

Facebook:

$ pip install http://github.com/pythonforfacebook/facebook-sdk/tarball/master

Twitter:

$ pip install python-twitter

Google:

$ pip install oauth2client google-api-python-client


       