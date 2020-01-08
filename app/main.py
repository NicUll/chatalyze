"""
Written by Nic Ullman

App to connect to and analyze twitch-chat channels.
Part of setup in main.py credit Sergio Lucero: https://gist.github.com/sergiolucero/1a1aab28f802491a4a03ac86f71b167f
"""

import os
from datetime import datetime

import graphene
from flask import Flask
from flask_graphql import GraphQLView
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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    rules = db.Column(db.String)

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
        mood_id = graphene.Int()

    channel = graphene.Field(lambda: ChannelObject)

    def mutate(self, info, name, active, mood_id=None):
        mood = Mood.query.filter_by(id=mood_id).first() if mood_id else None
        channel = Channel(name=name, active=active)

        if mood is not None:
            channel.mood = mood

        db.session.add(channel)
        db.session.commit()

        return AddChannel(channel=channel)


class Mutation(graphene.ObjectType):
    add_channel = AddChannel.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
db.create_all()
db.session.commit()
# Routes

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)


@app.route('/')
def chatalyze():
    return '<a href="/graphql"><h1>Chatalyzer</h1></a>'


if __name__ == '__main__':
    app.run()
