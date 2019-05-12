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
        friends = {}
        with open('friends.json', 'r') as json_file:
            friends_list = json.load(json_file)
        friends_list = [{"dir_name": dir_name, "name": info[0] ,"message_count": info[1]} for dir_name, info in friends_list.items()]
        friends_list = sorted(friends_list, key = lambda friend: friend['message_count'], reverse=True)

        for x in range(len(friends_list)):
            if x%10 == 0:
                print('Friends [' + str(x) + '-' + str(x+10) + ']')
            print('[' + str(x%10) + '] ' + str(friends_list[x]['name']) + ' [' + str(friends_list[x]['message_count']) + ']') #make this a function maybe
            if x%10 == 9:
                text_input = input('Choose your conversation. \'n\' to see more conversations. \'q\' to quit.')
                if text_input == 'q':
                    break
                elif text_input == 'n':
                    continue
                else:
                    print(str(x))
                    name = friends_list[int(text_input) + x-(x%10)]['name'] #make this a function maybe
                    if(get_json(name)): #Add Try Catch here... ACTUALLY...
                        get_sentiment_graph(name)
                        get_count_graph(name)
                        get_message_time_graph(name)
                        break
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
