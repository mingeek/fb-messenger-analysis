from sentiment import *
from scrape import *
from plot import *
from cli_helper import *
from copy import deepcopy
from pprint import pprint


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
    sentiments = chat_sentiment_analysis(convs)
    sentim_time = chat_sentiment_analysis_time(sentiments)
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

#message_count_over_time(conv)

if __name__ == '__main__':
    print("Welcome to Facebook Messenger Analysis. Enter 'q' to quit")
    text_input = input("Convert Facebook messages? Only do this once (y/n):").lower()
    if text_input == 'y':
        fb_to_json() #don't run this every time
    text_input = input("Sort friends by gender (y/n):").lower()


    while True:
        text_input = input('Name of conversation (first and last name of friend, no spaces): ').lower()
        if text_input == 'q':
            break
        else:
            if(get_json(text_input)):
                get_sentiment_graph(text_input)
                get_count_graph(text_input)
        text_input = input('Check another friend? (y/n): ')
        if text_input == 'y':
            continue
        text_input = input('View analysis of all chats? (y/n): ').lower()
        if text_input == 'y':
            get_all_sentiments()
            get_all_count()
            break