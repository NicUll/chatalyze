# Twitch Chatalyzer

## Contents
- [Introduction](#introduction)
    - [Modules Used](#modules)
    - [Unfinished](#unfinished)
- [How To Use](#how-to-use)

## Introduction

This repo is a collection of packages used for a Twitch chat analyzer.
The final data is accessed through a graphql-endpoint 

### Modules 

#### irc.py
A small irc client used to connect (but is not limited) to twitch.

#### dbhandler.py
Used to store message data temporarily to be analyzed.

#### messages.py
Controller of data between irc and db (db-handler).

#### analyzer.py
Supposed to work with data in messages so that main can fetch this

#### main.py
Holds all logic for graphql server and models being served

#### auth.py
Not implemented yet, added to keep from hardcoding authentication values in irc client

### Unfinished

The idea is that the data produced by Flask and stored in data.db (the channels table) 
can be accessed by several people at once but the underlying message data accessed by the analyzer
is only accessed by one client at a time. The field channel.active is then supposed to 
tell whether a thread calculating the message-data needs to be started or if there is already data 
called for by someone else. The active-flag should then be updated and set to false based on either if
the client that's making the data be created has changed channel, or if channel.upd_time is over a
certain amount of seconds old.

Upon querying for channel data the analyzer should call "messages" for data 
and calculate message-frequency as well as mood based on rules in the mood table.

Ideas for moods/feelings describing the channel-chat can be seen in mood-ideas.md
The mood was supposed to be calculated by the means of several parameters. 
The memes being sent.
If a raid is going on 
If people are joining, or parting from the channel
Various tags accessed with the CAP REQ commands.



## How To Use

Idea is that server should be started by means of main.py




