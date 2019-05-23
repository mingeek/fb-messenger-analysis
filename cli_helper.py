import os
import json
import datetime
from sentiment import *
from plot import *


def get_sentiment_graph(name):
    conv = get_json(name)['messages']
    chats = split_sentiment(conv)
    sentiment_graph = []
    print('FUCK')
    # while True:
    #     os.system("clear")
    #     print("Select which participants to include in graph")
    #     for x in range(len(chats)):
    #         print('[' + str(x) + '] ' + chats[x]['name'])
    #     index = input("[0-" + str(x) + "]")

    #     #only show ten at a time, and should show by message length fuck
    #     participants.append()
    for chat in chats:
        graph = {
            "x": chat['date'],
            "y": chat['sentiment'],
            "label": chat['name']
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
            "label": 'Sentiment' #'My' sentiment for now, might change that to name
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
            "label": chat['name']
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

def get_message_time_graph(name):
    conv = get_json(name)['messages']
    chats = split_conversation(conv)

    time_graph = []
    for chat in chats:
        count = count_by_time(chat['messages'])
        graph = {
            "x": count['time'],
            "y": count['message_count'],
            "label": chat['name'] + ' Messages'
        }
        time_graph.append(graph)
    plot_multi(time_graph, ' Messages/Hour')