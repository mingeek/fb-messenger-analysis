from sentiment import *
from scrape import *
from plot import *
from cli_helper import *
from copy import deepcopy
from pprint import pprint

def main():
    print("Welcome to Facebook Messenger Analysis. Enter 'q' to quit")
    text_input = input("Convert Facebook messages? Only do this once (y/n):").lower()
    if text_input == 'y':
        fb_to_json() #don't run this every time
    elif text_input == 'q':
        return
    text_input = input("Sort friends by gender? (y/n):").lower() #You can check if this is done?
    if text_input =='y':
        pprint('zz')
    elif text_input == 'q':
        return
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
        elif text_input == 'q':
            break
        text_input = input('View analysis of all chats? (y/n): ').lower()
        if text_input == 'y':
            get_all_sentiments()
            get_all_count()
            break

if __name__ == '__main__':
    main()
