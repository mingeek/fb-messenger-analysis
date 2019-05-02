from sentiment import *
import matplotlib.pyplot as plt
import pandas as pd
import itertools
pd.plotting.register_matplotlib_converters()


fb_to_json() #don't run this every time
chats = get_chats()



#all conversations
convs = [chat_sentiment_analysis(get_json(chat)) for chat in chats]
all_convs = list(itertools.chain.from_iterable(convs))

df = chat_sentiment_analysis_time(all_convs)
date = df.index.tolist()
sentiment = df['sentiment'].tolist()

f, ax = plt.subplots()
ax.plot(date, sentiment, 'b')
ax.set_title('Relationship Comparison')
ax.set_ylabel('Sentiment')
plt.gcf().autofmt_xdate()
plt.grid(True, which='both')
plt.show()