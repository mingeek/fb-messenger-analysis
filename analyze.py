from sentiment import *
from plot import *
import matplotlib.pyplot as plt
import pandas as pd
pd.plotting.register_matplotlib_converters()


#fb_to_json() #don't run this every time





conv = get_json('NAME HERE lowercase, no spaces') 
#conv = all_conversations()
count = message_count(conv)

sentiments = split_sentiment(conv)
me, them = sentiments['sender_sentiment'], sentiments['recipient_sentiment']

plot_two(me['date'], me['sentiment'], them['date'], them['sentiment'])
