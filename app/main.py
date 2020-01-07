"""
Written by Nic Ullman

App to connect to and analyze twitch-chat channels.
Part of setup in main.py credit Sergio Lucero: https://gist.github.com/sergiolucero/1a1aab28f802491a4a03ac86f71b167f
"""

# Imports
import datetime
import os

import graphene
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Channel(db.Model):
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)
    active = db.Column(db.Boolean, nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.now)
    mood = db.Column(db.Integer, db.ForeignKey('mood.id'))
    messages_per_min = db.Column(db.Integer, default=0)
    messages_per_sec = db.Column(db.Integer, default=0)

    def __repr__(self):
        return 'Channel #%s' % self.name


class Mood(db.Model):
    __tablename__ = 'mood'

    id = db.column(db.Integer, primary_key=True)
    name = db.column(db.String, unique=True)
    rules = db.column(db.String)

    def __repr__(self):
        return 'Mood %i = %s' % (self.id, self.name)


# Schema
class ChannelObject(SQLAlchemyObjectType):
    class Meta:
        model = Channel
        interfaces = (graphene.relay.Node,)


class MoodObject(SQLAlchemyObjectType):
    class Meta:
        model = Mood
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_channels = SQLAlchemyConnectionField(ChannelObject)
    all_moods = SQLAlchemyConnectionField(MoodObject)
    
class AddChannel(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        active = graphene.Boolean(required=True)
        mood_id = graphene.Integer(required=False)
        
    channel = graphene.Field(lambda: ChannelObject)
    
    def mutate(self, info, name, active, mood_id):
        mood = Mood.query.filter_by(id=mood_id).first()
        channel = Channel(name=name, active=active)

        if mood is not None:
            channel.mood = mood

        db.session.add(channel)
        db.session.commit()

        return AddChannel(channel=channel)

        