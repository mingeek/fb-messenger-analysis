import simplejson
import os
import pandas as pd
import datetime
import numpy as np
import itertools

from bs4 import BeautifulSoup
from textblob import TextBlob
from dateutil import parser

#Input: Text to be removed and an optional list of words to remove
#Returns: Text with removed cursewords
def remove_word(text, remove = ['fuck','bitch','shit','retard','idiot', 'sick', 'lit']): #cursewords only used in derogatry manners not set by default
    for word in remove:
        text = text.replace(word, "")
    return text

#Requirement: The Facebook messages must be in {current_dir}/messages in the way they were downloaded
#Input: N/A 
#Returns: N/A
def fb_to_json():
    if not os.path.exists(os.getcwd() + '/json'):
        os.makedirs(os.getcwd() + '/json')    
    for root, dirs, files in os.walk('messages'): 
        for dir in dirs:
            curr_dir = os.getcwd() + '/messages/' + dir
            for file in os.listdir(curr_dir):
                if file.endswith(".html"):
                    with open(curr_dir + '/' + file, "rb") as fp:
                        soup = BeautifulSoup(fp, 'lxml')

                        conv_name = soup.find('div', {'class' : '_3b0d'}).text #The first word in message1.html is always the friend's name
                        messages = soup.findAll('div', {'class' : '_2let'})
                        message_list = []
                        friend = dir.split('_')[0]
                        for message in messages:

                            sender = message.previous_sibling.text
                            div = message.findChild()
                            if len(div.findChildren()) == 4:#otherwise it's an image or file or something
                                text = div.findChildren()[1].text
                                date = parser.parse(message.next_sibling.text).isoformat()
                                sent = False
                                if conv_name != sender:
                                    sent = True #Sent by you
                                message = {
                                    "friend": friend,
                                    "sent": sent,
                                    "text": text,   
                                    "date": date
                                }
                                message_list.append(message)
                        ###Do not fix duplicate names, because then you need to address it while scraping###
                        with open('json/' + friend + '.json', 'w') as json_file:  
                            simplejson.dump(message_list, json_file)
        return #only go to 2nd level of dirs

#Input: N/A
#Return: A list of strings containing all chat names
def get_chats_names():
    chat_names = []
    for file in os.listdir(os.getcwd() + '/json'):
        chat_names.append(file.split('.')[0])
    return chat_names

#Input: JSON of message
#Return: JSON holding sentiment analysis on a given message
def sentiment_analysis(message):
    return {
        "date": message['date'],
        "friend": message['friend'],
        "sent": message['sent'],
        "sentiment": TextBlob(remove_word(message['text'])).sentiment[0] 
    }

#Input: String input 
#Return: JSON of chatname
def get_json(name):
    with open('json/' + name + '.json', 'r') as json_file:
        return simplejson.load(json_file)

#Input: A list of JSON objects holding all the messages of a specific chat
#Return: A list holding JSON of sentiment analysis per message
def chat_sentiment_analysis(messages):
    analyzed_messages = [sentiment_analysis(message) for message in messages]
    return analyzed_messages

#Input: A list of JSON holding sentiment analysis
#Return: A tuple of lists of the average sentiment over a weekly basis (Used to be data frame, might change it back)
#Note: Changing the time is dependent on the resample library, in which the basis are 'D'ays, 'W'eeks, 'M'onths, etc.
def chat_sentiment_analysis_time(messages, time='W'): 
    df = pd.io.json.json_normalize(messages)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df.sentiment != 0]
    df = df.resample(time, on='date').mean()
    df = df.dropna()
    df = df.loc[datetime.date(year=2018,month=9,day=1):datetime.date(year=2019,month=5,day=5)] #Personal Use, ignore this line
    dates = df.index.tolist()
    sentiments = df['sentiment'].tolist()
    return {
        #These are lists
        "date": dates,
        "sentiment": sentiments
    }
    #return df

#Input: A list of JSON containing messages
#Return: A JSON counting (#sent, #received) messages
def message_count(messages):
    sent, received, = 0, 0
    friend = messages[0]['friend']
    for message in messages:
        if message['sent']:
            sent += 1
        else:
            received += 1
    return {
        "friend": friend,
        "sent": sent,
        "received": received
    }
    #Note: Maybe combine this with split_conversation? And maybe this should contain the friend name?

#Input: N/A
#Return: JSON of all messages amongst all conversations
def all_conversations():
    chats = get_chats_names()
    convs = [get_json(chat) for chat in chats]
    all_convs = list(itertools.chain.from_iterable(convs))
    return all_convs

#Input: A JSON of a conversation
#Return: A JSON of two lists (sent, received) of messages
def split_conversation(messages):
    sent, received = [], []
    for message in messages:
        sent.append(message) if message['sent'] else received.append(message)
    return {
        "sent": sent, 
        "received": received
    }

#Input: A JSON of a conversation
#Return: A JSON of the sentiments split by sent/recieved messages
def split_sentiment(messages):
    split = split_conversation(messages)
    sender = split['sent']
    recipient = split['received']
    sender = chat_sentiment_analysis(sender)
    recipient = chat_sentiment_analysis(recipient)
    sender_sentiments = chat_sentiment_analysis_time(sender)
    recipient_sentiments = chat_sentiment_analysis_time(recipient)
    return {
        "sender_sentiment": sender_sentiments,
        "recipient_sentiment": recipient_sentiments
    }