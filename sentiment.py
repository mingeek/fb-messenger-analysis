import os
import json
import pandas as pd
import datetime
import numpy as np
import itertools
from pprint import pprint
from tqdm import tqdm as pbar
from textblob import TextBlob
pd.plotting.register_matplotlib_converters()

#Input: N/A
#Return: A list of strings containing all chat names
def get_chats_names():
    chat_names = []
    for file in os.listdir(os.getcwd() + '/json'):
        chat_names.append(file.split('.')[0])
    return chat_names

#Input: String input 
#Return: JSON of chatname
def get_json(name):
      with open('json/' + name + '.json', 'r') as json_file:
        return json.load(json_file)
    

#Input: A list of JSON objects holding all the messages of a specific chat
#Return: A list holding JSON of sentiment analysis per message
def get_chat_sentiment(messages):
    analyzed_messages = [{"sentiment": message['sentiment'], "date": message['date']} for message in messages ]
    return analyzed_messages

#Input: A list of JSON holding sentiment analysis
#Return: A JSON of lists of the average sentiment over a weekly basis (Used to be data frame, might change it back)
#Note: Changing the time is dependent on the resample library, in which the basis are 'D'ays, 'W'eeks, 'M'onths, etc.
def sentiment_over_time(messages, time='W'): 
    df = pd.io.json.json_normalize(messages)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df.sentiment != 0]
    df = df.resample(time, on='date').mean()
    df = df.dropna()
#    df = df.loc[datetime.date(year=2019,month=3,day=1):datetime.date(year=2019,month=5,day=5)] #Personal Use, ignore this line
    dates = df.index.tolist()
    sentiments = df['sentiment'].tolist()
    return {
        #These are lists
        "date": dates,
        "sentiment": sentiments
    }

#Input: A list of JSON containing messages
#Return: A JSON counting the amount of messages
def message_count(messages):
    sent, received, = 0, 0
    chatname = messages[0]['chatname']
    for message in messages:
        if message['sent']:
            sent += 1
        else:
            received += 1
    return {
        "chatname": chatname,
        "sent": sent,
        "received": received
    }
    #Note: Maybe combine this with split_conversation? And maybe this should contain the friend name?

#Input: N/A
#Return: JSON of all messages amongst all conversations
def all_conversations():
    chats = get_chats_names()
    convs = [get_json(chat)['messages'] for chat in chats]
    all_convs = list(itertools.chain.from_iterable(convs))
    return all_convs

#Input: A JSON of a conversation
#Return: A JSON of the conversation, divided by sender
def split_conversation(messages):
    split_messages = {}
    for message in messages:
        if message['sender'] in split_messages:
            split_messages[message['sender']].append(message)
        else:
            split_messages[message['sender']] = []

    return [{"name": conversation[0], "messages": conversation[1]} for conversation in split_messages.items()]

#Input: A JSON of a conversation
#Return: A list of JSONs of the sentiments split by person over time
def split_sentiment(messages):
    conversations = split_conversation(messages)
    sentiments = []
    for conversation in conversations:
        sentiment = sentiment_over_time(get_chat_sentiment(conversation['messages']))
        sentiment['name'] = conversation['name']
        sentiments.append(sentiment)
    return sentiments

#Input: A JSON of a conversation
#Return: A JSON of a list of Dates and Message Counts. 
#This could use reworking because I literally just count the rows, no restructuring.
def message_count_over_time(messages, time='W'):
    df = pd.io.json.json_normalize(messages)
    df['date'] = pd.to_datetime(df['date'])
    df = df.resample(time, on='date')['text'].agg('count')
#    df = df.loc[datetime.date(year=2019,month=3,day=25):datetime.date(year=2019,month=5,day=5)] #Personal Use, ignore this line
    dates = df.index.tolist()
    message_count = df.values.tolist()
    return {
        #These are lists
        "date": dates,
        "message_count": message_count
    }


#Input: A JSON of a conversation
#Return: Returns the sentiment sorted by time instead of date
# def sentiment_by_time(messages):
