import os
import json
import datetime
from sentiment import *
from plot import *


def get_sentiment_graph(name):
    conv = get_json(name)['messages']
    sentiments = split_sentiment(conv)
    sender_sent, recipient_sent = sentiments['sender_sentiment'], sentiments['recipient_sentiment']
    sentiment_graph = [
    {
            "x": sender_sent['date'],
            "y": sender_sent['sentiment'],
            "label": 'My Sentiment' #'My' sentiment for now, might change that to name
    },
    {
            "x": recipient_sent['date'],
            "y": recipient_sent['sentiment'],
            "label": 'Their Sentiment'
    }
    ]
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
    convs = split_conversation(conv)
    sender_count, recipient_count = message_count_over_time(convs['sent']), message_count_over_time(convs['received'])
    graphs = [
        {
            "x": sender_count['date'],
            "y": sender_count['message_count'],
            "label": 'My #'
        },
        {
            "x": recipient_count['date'],
            "y": recipient_count['message_count'],
            "label": 'Their #'
        }
    ]
    plot_multi(graphs, 'Message Count')

def get_all_count():
    convs = all_conversations()
    message_count = message_count_over_time(convs)
    graph = {
            "x": message_count['date'],
            "y": message_count['message_count'],
            "label": 'My #'
    }
    plot_one(graph, 'Message Count')