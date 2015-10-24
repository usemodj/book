from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.social import Social, SQLAlchemyConnectionDatastore, login_failed
from flask.ext.social.utils import get_connection_values_from_oauth_response

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
pagedown = PageDown()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    
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

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
    """
    from .models import User, Role, Connection
    security_ds = SQLAlchemyUserDatastore(db, User, Role)
    social_ds = SQLAlchemyConnectionDatastore(db, Connection)
    app.security = Security(app, security_ds)
    app.social = Social(app, social_ds)
    """
    return app

