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

                        conv_name = soup.find('div', {'class' : '_3b0d'}).text
                        messages = soup.findAll('div', {'class' : '_2let'})
                        message_list = []
                        friend = dir.split('_')[0]
                        for message in messages:
                            sender = message.previous_sibling.text

                            #do i make the 'friend' the same as the sender in terms of casing or no?
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

#Input: A JSON object holding all the messages of a specific chat
#Return: A list holding JSON of sentiment analysis per message
def chat_sentiment_analysis(messages):
    analyzed_messages = [sentiment_analysis(message) for message in messages]
    return analyzed_messages

#Input: A list of JSON holding sentiment analysis
#Return: A Data Frame of the average sentiment over a weekly basis
def chat_sentiment_analysis_time(messages):
    df = pd.io.json.json_normalize(messages)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df.sentiment != 0]
    df = df.resample('W', on='date').mean()
    df = df.dropna()
#   df = df.loc[datetime.date(year=2018,month=9,day=1):datetime.date(year=2019,month=5,day=1)]
    return df

#Input: A list of JSON containing messages
#Return: A dict counting (#sent, #received) messages
def message_count(messages):
    sent, received, = 0, 0
    for message in messages:
        if message['sent']:
            sent += 1
        else:
            received += 1
    return {
        "sent": sent,
        "received": received
    }

#Input: N/A
#Return: JSON of all messages amongst all conversations
def all_conversations():
    chats = get_chats_names()
    convs = [get_json(chat) for chat in chats]
    all_convs = list(itertools.chain.from_iterable(convs))
    return all_convs