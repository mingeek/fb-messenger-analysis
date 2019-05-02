import simplejson
import os
import pandas as pd
import datetime
import numpy as np
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
                        messages = soup.findAll('div', {'class' : '_2let'})
                        message_list = []
                        author = dir.split('_')[0]
                        for message in messages:
                            div = message.findChild()
                            if len(div.findChildren()) == 4:#otherwise it's an image or file or something
                                text = div.findChildren()[1].text
                                date = parser.parse(message.next_sibling.text).isoformat()
                                message = {
                                    "author": author,
                                    "text": text,   
                                    "date": date
                                }
                                message_list.append(message)
                        with open('json/' + author + '.json', 'w') as json_file:  
                            simplejson.dump(message_list, json_file)
        return #only go to 2nd level of dirs

#Input: N/A
#Return: A list of strings containing all chat names
def get_chats():
    chat_names = []
    for file in os.listdir(os.getcwd() + '/json'):
        chat_names.append(file.split('.')[0])
    return chat_names

#Input: JSON of message
#Return: JSON holding sentiment analysis on a given message
def sentiment_analysis(message):
    return {
        "date": message['date'],
        "author": message['author'],
        "sentiment": TextBlob(remove_word(message['text'])).sentiment[0] 
    }

#Input: String input 
#Return: JSON of chatname
def get_json(name):
    with open('json/' + name + '.json', 'r') as json_file:
        print (name + '\n')
        return simplejson.load(json_file)

#Input: A JSON object holding all the messages of a specific chat
#Return: A list holding JSONs of sentiment analysis per message
def chat_sentiment_analysis(messages):
    analyzed_messages = [sentiment_analysis(message) for message in messages]
    return analyzed_messages

#Input: A list of JSONs holding sentiment analysis
#Return: A Data Frame of the average sentiment over a weekly basis
def chat_sentiment_analysis_time(messages):
    df = pd.io.json.json_normalize(messages)
    df['date'] = pd.to_datetime(df['date'])
    df = df[df.sentiment != 0]
    df = df.resample('W', on='date').mean()
    df = df.dropna()
    return df

