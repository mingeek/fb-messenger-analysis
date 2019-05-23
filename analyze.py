from sentiment import *
from scrape import *
from plot import *
from cli_helper import *
from copy import deepcopy
from pprint import pprint

def list_friends(index, friends_list):
    print('Friends [' + str(index) + '-' + str(index+10) + ']')
    for x in range(10):
        if index == len(friends_list):
            break
        print('[' + str(index%10) + '] ' + str(friends_list[index]['name']) + ' [' + str(friends_list[index]['message_count']) + ']')
        index += 1
    return index


def main():
    os.system("clear")
    input("Welcome to Facebook Messenger Analysis.\nPlease ensure your messages are in " + os.getcwd() + "/messages/ before proceeding.\nFigures will be saved in " + os.getcwd() + "/figures/{name}" + "\nPress Enter to continue")
    if os.path.isfile(os.getcwd() + '/friends.json') == False:
        print("Converting your Facebook chat messages...")
        fb_to_json()
    index = 0
    with open('friends.json', 'r') as json_file:
        friends_list = json.load(json_file)
    friends_list = [{"dir_name": dir_name, "name": info[0] ,"message_count": info[1]} for dir_name, info in friends_list.items()]
    friends_list = sorted(friends_list, key = lambda friend: friend['message_count'], reverse=True)
    errors = []
    while True:
        os.system('clear')
        for error in errors:
            print(error)
        errors = []
        if index == len(friends_list):
            pprint("No more friends to be listed.")
        index = list_friends(index, friends_list)
        print('-----')
        text_input = input('[0-9] Select a friend, [N]ext, [O]ptions, [Q]uit: ').lower()
        if text_input == 'q':
            break
        elif text_input == 'n':
            continue
        elif len(text_input) == 1 and text_input.isdigit():
            name = friends_list[int(text_input) + index-10-(index%10)]['name'] #make this a function maybe
            if(get_json(name)): #Add Try Catch here... ACTUALLY...
                #List by Month or Year            
                get_sentiment_graph(name)
                get_count_graph(name)
                get_message_time_graph(name)
        elif text_input == 'o':
            os.system('clear')
            options = [
                '[0] Analysis of all chats',
                '[1] Sort friends by gender',
            ]
            for option in options:
                print(option)
            text_input = input('[0-1] Select, [B]ack, [Q]uit: ').lower()
            if text_input == '0':
                get_all_sentiments()
                get_all_count()
            elif text_input == '1':
                #do something here
                print('1')
            elif text_input == 'b':
                continue
            elif text_input == 'q':
                break
            else: 
                errors.append("= You entered an invalid input =")
        else:
            errors.append("= You entered an invalid input =")
        index = 0

    
if __name__ == '__main__':
    main()
