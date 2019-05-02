from sentiment import *
import matplotlib.pyplot as plt
import pandas as pd
pd.plotting.register_matplotlib_converters()


fb_to_json()
chats = get_chats()
chat = chat_sentiment_analysis(get_json(chats[0])) #insert names here
df = chat_sentiment_analysis_time(chat)
date = df.index.tolist()
sentiment = df['sentiment'].tolist()

plt.plot(date, sentiment)
plt.ylabel('Sentiment')
plt.gcf().autofmt_xdate()
plt.show()