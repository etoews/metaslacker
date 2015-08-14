import logging
import os

from flask import Flask
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy


logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.debug("Welcome to Propeller")


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


@api.route('/')
def index():
    return 'Welcome to Propeller'


class Guest(db.Model):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return "[Guest: id={}, name={}]".format(self.id, self.name)


@manager.command
def create_db():
    logger.debug("create_db")
    api.config['SQLALCHEMY_ECHO'] = True
    db.create_all()

@manager.command
def create_dummy_data():
    logger.debug("create_test_data")
    api.config['SQLALCHEMY_ECHO'] = True
    guest = Guest(name='Steve')
    db.session.add(guest)
    db.session.commit()

@manager.command
def drop_db():
    logger.debug("drop_db")
    api.config['SQLALCHEMY_ECHO'] = True
    db.drop_all()


if __name__ == '__main__':
    manager.run()
