from sentiment import *
from scrape import *
from plot import *


fb_to_json() #don't run this every time





#conv = get_json('namehere') 
#conv = all_conversations()
count = message_count(conv)
print(count)
sentiments = split_sentiment(conv)
me, them = sentiments['sender_sentiment'], sentiments['recipient_sentiment']

plot_two(me['date'], me['sentiment'], them['date'], them['sentiment'])
