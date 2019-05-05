from sentiment import *
from scrape import *
from plot import *


#fb_to_json() #don't run this every time

name = ''

whatsapp_to_json(name + '.txt')
friendname = ''
conv = get_json(name + '-MA') 
#conv = all_conversations()
#message_count_over_time(conv)


# Post people by conversation length
# chats = get_chats_names()
# count_ranking = []
# for chat in chats:
#     count_ranking.append((chat, len(get_json(chat))))
# count_ranking = sorted(count_ranking, key=lambda x: x[1])

# Get counts of two ppl
convs = split_conversation(conv)
my_count, their_count = message_count_over_time(convs['sent']), message_count_over_time(convs['received'])

# Get sentiments of two ppl
sentiments = split_sentiment(conv)
me, them = sentiments['sender_sentiment'], sentiments['recipient_sentiment']

sentiment_graph = [
    {
            "x": me['date'],
            "y": me['sentiment'],
            "label": 'My Sentiment'
    },
    {
            "x": them['date'],
            "y": them['sentiment'],
            "label": 'Their Sentiment'
    }
]

graphs = [
        {
            "x": me['date'],
            "y": my_count['message_count'],
            "label": 'My #'
        },
        {
            "x": me['date'],
            "y": their_count['message_count'],
            "label": 'Their #'
        }
        ]

graphset = [
    [
        {
            "x": my_count['date'],
            "y": my_count['message_count'],
            "label": 'My #',
            "ylabel": "Message Count"
        },
        # {
        #     "x": their_count['date'],
        #     "y": their_count['message_count'],
        #     "label": 'Their #',
        #     "ylabel": "Message Count"
        # }
    ],

    [
        {
            "x": me['date'],
            "y": me['sentiment'],
            "label": 'My sentiment',
            "ylabel": "Sentiment"
        },
        # {
        #     "x": them['date'],
        #     "y": them['sentiment'],
        #     "label": 'Their sentiment',
        #     "ylabel": "Sentiment"
        # },
    ]
]



#plot_multi_two(graphset, 'Message/Sentiments')

#plot_multi(graphs, 'Message/Sentiments')

#plot_two(my_count['date'], my_count['message_count'], their_count['date'], their_count['message_count'], 'Message Count')



plot_multi(sentiment_graph, friendname + ' Sentiment')
