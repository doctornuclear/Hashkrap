from flask import Flask
from datetime import timedelta
import sqlite3
from flask import g
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.permanent_session_lifetime = timedelta(hours=6)

DATABASE = '/path/to/db'

app.config['SECRET_KEY'] = 'secret key'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("scraped_hashtags.db", check_same_thread=False, isolation_level=None)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


from hashkrap import routes