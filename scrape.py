import simplejson
import os
from bs4 import BeautifulSoup
from dateutil import parser
from tqdm import tqdm as pbar



#Requirement: The Facebook messages must be in {current_dir}/messages in the way they were downloaded
#Input: N/A 
#Returns: N/A
def fb_to_json():
    if not os.path.exists(os.getcwd() + '/json'):
        os.makedirs(os.getcwd() + '/json')    
    for root, dirs, files in os.walk('messages'): 
        for dir in pbar(dirs, desc='Converting messages to JSON:'):
            curr_dir = os.getcwd() + '/messages/' + dir
            for file in os.listdir(curr_dir):
                if file.endswith(".html"):
                    with open(curr_dir + '/' + file, "rb") as fp:
                        group_chat = False
                        soup = BeautifulSoup(fp, 'lxml')
                        conv_name = soup.find('div', {'class' : '_3b0d'}).text #The first word in message1.html is always the friend's name, or the group chat name
                        chatname = soup.find('div', {'class' : '_2lek'}).text
                        print(chatname)
                        if chatname.split(' ')[0] == "Participants:": #thisisagroupchat
                            print('this is a group')
                            your_name = chatname.split(" ")[-1]
                            group_chat = True
                        messages = soup.findAll('div', {'class' : '_2let'})
                        message_list = []
                        friend = dir.split('_')[0]
                        for message in pbar(messages, desc=conv_name):

                            sender = message.previous_sibling.text
                            div = message.findChild()
                            if len(div.findChildren()) == 4:#otherwise it's an image or file or something
                                text = div.findChildren()[1].text
                                date = parser.parse(message.next_sibling.text).isoformat()
                                sent = False
                                if group_chat:
                                    if your_name == sender:
                                        sent = True
                                elif conv_name != sender:
                                    sent = True #Sent by you
                                message = {
                                    "friend": friend, #this is also the chat name
                                    "sent": sent,
                                    "sender": sender,
                                    "text": text,   
                                    "date": date
                                }
                                message_list.append(message)
                        ###Do not fix duplicate names, because then you need to address it while scraping###
                        with open('json/' + friend + '.json', 'w') as json_file:  
                            simplejson.dump(message_list, json_file)
        return #only go to 2nd level of dirs