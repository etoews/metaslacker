import logging
import os

from flask import Flask, request
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash


logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.debug("Welcome to MetaSlacker")


SQLALCHEMY_DATABASE_URI = \
    '{engine}://{username}:{password}@{hostname}/{database}'.format(
        engine='mysql+pymysql',
        username=os.getenv('DB_ENV_MYSQL_USER'),
        password=os.getenv('DB_ENV_MYSQL_PASSWORD'),
        hostname=os.getenv('DB_PORT_3306_TCP_ADDR'),
        database=os.getenv('DB_ENV_MYSQL_DATABASE'))


api = Flask(__name__)
api.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
api.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(api)
db = SQLAlchemy(api)

@api.route('/', methods=['GET', 'POST'])
def index():
    # TODO: verify token!
    if request.method == 'GET':
        print(request.args)
        return 'GET Welcome to MetaSlacker'
    elif request.method == 'POST':
        print(request.headers)
        return 'POST Welcome to MetaSlacker'

@api.route('/create', methods=['POST'])
def register():
    print(request.headers)

    username = request.headers['username']
    api_key = request.headers['text']

    user = User(username=username, api_key=api_key)
    db.session.add(user)
    db.session.commit()

    return 'User {} created!'.format(username)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    api_key_hash = db.Column(db.String(128))

    @property
    def api_key(self):
        raise AttributeError('api_key is not a readable attribute')

    @api_key.setter
    def api_key(self, api_key):
        self.api_key_hash = generate_password_hash(api_key)

    def verify_api_key(self, api_key):
        return check_password_hash(self.api_key_hash, api_key)

    def __repr__(self):
        return "[User: id={}, username={}]".format(self.id, self.username)


@manager.command
def create_db():
    logger.debug("create_db")
    logger.debug(SQLALCHEMY_DATABASE_URI)
    api.config['SQLALCHEMY_ECHO'] = True
    db.create_all()

@manager.command
def create_dummy_data():
    logger.debug("create_test_data")
    api.config['SQLALCHEMY_ECHO'] = True
    user = User(username='Steve')
    db.session.add(user)
    db.session.commit()

@manager.command
def drop_db():
    logger.debug("drop_db")
    api.config['SQLALCHEMY_ECHO'] = True
    db.drop_all()


if __name__ == '__main__':
    manager.run()
