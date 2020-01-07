"""
Written by Nic Ullman

App to connect to and analyze twitch-chat channels.
Part of setup in main.py credit Sergio Lucero: https://gist.github.com/sergiolucero/1a1aab28f802491a4a03ac86f71b167f
"""

# Imports
import datetime
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Channels(db.Model):
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)
    active = db.Column(db.Boolean, nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.now)
    mood = db.Column(db.Integer, db.ForeignKey('mood.id'))
    messages_per_min = db.Column(db.Integer)
    messages_per_sec = db.Column(db.Integer)

    def __repr__(self):
        return 'Channel #%s' % self.name


class Mood(db.Model):
    __tablename__ = 'mood'

    id = db.column(db.Integer, primary_key=True)
    desc = db.column(db.String, unique=True)
    rules = db.column(db.String)

    def __repr__(self):
        return 'Mood %i = %s' % (self.id, self.desc)
