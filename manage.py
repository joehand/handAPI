# manage.py
from flask.ext.script import Manager, Shell
from flask.ext.security import MongoEngineUserDatastore

from hand_api import create_app
from hand_api.extensions import db
from hand_api.user import User, Role


app = create_app()
manager = Manager(app)


@manager.command
def initdb():
    """Init/reset database."""
    user_datastore = MongoEngineUserDatastore(db, User, Role)
    user_datastore.create_user(email='joe.a.hand@gmail.com', password='password')


def shell_context():
    return dict(app=app)   
from flask.ext.script import Manager


#runs the app
if __name__ == '__main__':
    manager.add_command('shell', Shell(make_context=shell_context))
    manager.run()