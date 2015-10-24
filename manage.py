#!/usr/bin/env python 
import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app, db
from app.models import User, Role, Post, Permission
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
import app

app = create_app(os.getenv('BOOK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

app.config['SECURITY_POST_LOGIN'] = '/profile'
#Twitter:
app.config['SOCIAL_TWITTER'] = {
    'consumer_key': 'twitter consumer key',
    'consumer_secret': 'twitter consumer secret'
}
#Facebook:
app.config['SOCIAL_FACEBOOK'] = {
    'consumer_key': '1120806077947103',
    'consumer_secret': '4bf6c5476a4f3617dd1d67c7ff83072e'
}
#Google:
app.config['SOCIAL_GOOGLE'] = {
    'consumer_key': 'xxxx',
    'consumer_secret': 'xxxx'
}

@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML verion: file://%s/index.html' % covdir)
        COV.erase()

@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run()

@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    from app.models import Role, User
    
    #migrate database to latest revision
    upgrade()
    
    #create user roles
    Role.insert_roles()
    
    #create self-follows for all users
    User.add_self_follows()
                
    
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Permission=Permission)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    
    
"""
    ## Requirements File
    (venv) $ pip freeze >requirements.txt

    To ensure that you have all the dependencies installed, also run 
    (venv) $ pip install -r requirements/prod.txt

    Migration:
    (venv) $ python manage.py db migrate
    
    Deploy command:
    $ source venv/bin/activate
    (venv) $ python manage.py deploy
    
    Run production mode:
    (venv) $ export BOOK_CONFIG=production
    (venv) $ gunicorn manage:app
    
   The unit tests can be executed as follows: 
   (venv) $ python manage.py test
   
   When working with Flask-Migrate to keep track of migrations, database
    tables can be created or upgraded to the latest revision with a single command:
    (venv) $ python manage.py db upgrade
"""   