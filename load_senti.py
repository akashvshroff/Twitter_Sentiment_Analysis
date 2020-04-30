# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:26:53 2020

@author: akush
"""

import sqlite3
import tweepy
from textblob import TextBlob
from config import *
import matplotlib.pyplot as plt

def load():
    keyword = input("Please enter keyword to be searched: \n")
    language = 'en'

    for result in tweepy.Cursor(api.search,q = keyword,lang = 'en').items(250):
        tweet = TextBlob(result.text)
        a = tweet.sentiment.polarity
        #print (a)
        if a > 0:
            sentiment = 'positive'
        elif a < 0:
            sentiment = 'negative'
        else :
            sentiment = 'neutral'
        #print (result.text,'sentiment',sentiment)

        cur.execute('SELECT id FROM Sentiments WHERE name = ? ', (sentiment, ))
        sentiment_id = cur.fetchone()[0]
        cur.execute('INSERT OR IGNORE INTO Tweets (username,tweet,sentiment_id) VALUES (?,?,?)',
            (result.user.screen_name, result.text, sentiment_id))

    conn.commit()

def analyse():
    cur.execute('''SELECT Tweets.username, Tweets.tweet, Sentiments.name FROM Tweets
                   JOIN Sentiments ON  Tweets.sentiment_id = Sentiments.id''')
    data = cur.fetchall()
    pcount = 0
    ncount = 0
    necount = 0
    total = 0
    for row in data:
        if row[2] == 'positive':
            pcount += 1
        elif row[2] == 'negative':
            ncount += 1
        else :
            necount += 1
        total += 1

    p = pcount/total * 100
    n = ncount/total * 100
    ne = necount/total * 100
    #print (p,n,ne)

    positive = float("{:.2f}".format(p))
    negative = float("{:.2f}".format(n))
    neutral = float("{:.2f}".format(ne))
    #g = float("{:.2f}".format(x))
    # print (positive,negative,neutral)
    show(positive,neutral,negative)
    conn.commit()

def show(p,ne,n):

    labels = 'Positive','Neutral','Negative'
    sizes = [p,ne,n]
    #print (sizes)
    explode = (0,0,0.1)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()


if __name__ == '__main__':
    conn = sqlite3.connect('tw_sen.sqlite')
    cur = conn.cursor()

    cur.executescript('''
    DROP TABLE IF EXISTS Tweets;
    DROP TABLE IF EXISTS Sentiments;
    CREATE TABLE Tweets (username TEXT UNIQUE, tweet TEXT,
    sentiment_id INTEGER);
    CREATE TABLE Sentiments (name TEXT UNIQUE, id INTEGER NOT NULL PRIMARY
    KEY AUTOINCREMENT UNIQUE)''')
    cur.execute('INSERT INTO Sentiments (name) VALUES (?)',('positive',))
    cur.execute('INSERT INTO Sentiments (name) VALUES (?)',('negative',))
    cur.execute('INSERT INTO Sentiments (name) VALUES (?)',('neutral' ,))

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    load()
    analyse()
