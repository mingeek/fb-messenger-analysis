import os
import json
import datetime
from sentiment import *
from plot import *


def get_sentiment_graph(name):
    conv = get_json(name)['messages']
    chats = split_sentiment(conv)
    sentiment_graph = []
    for chat in chats:
        graph = {
            "x": chat['date'],
            "y": chat['sentiment'],
            "label": chat['name'] + ' Sentiment'
        }
        sentiment_graph.append(graph)
    plot_multi(sentiment_graph, ' Sentiment')

def get_all_sentiments():
    convs = all_conversations()
    sentiments = get_chat_sentiment(convs)
    sentim_time = sentiment_over_time(sentiments)
    sentiment_graph = {
            "x": sentim_time['date'],
            "y": sentim_time['sentiment'],
            "label": 'My Sentiment' #'My' sentiment for now, might change that to name
    }
    plot_one(sentiment_graph, 'Sentiment')

def get_count_graph(name):
    conv = get_json(name)['messages']
    chats = split_conversation(conv)
    count_graph = []
    for chat in chats:
        count = message_count_over_time(chat['messages'])
        graph = {
            "x": count['date'],
            "y": count['message_count'],
            "label": chat['name'] + ' Messages'
        }
        count_graph.append(graph)
    plot_multi(count_graph, 'Message Count')

def get_all_count():
    convs = all_conversations()
    message_count = message_count_over_time(convs)
    graph = {
            "x": message_count['date'],
            "y": message_count['message_count'],
            "label": 'My #'
    }
    plot_one(graph, 'Message Count')