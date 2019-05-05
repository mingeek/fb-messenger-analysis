import os
import json
from bs4 import BeautifulSoup
from dateutil import parser
from tqdm import tqdm as pbar



#Requirement: The Facebook messages must be in {current_dir}/messages in the way they were downloaded
#Input: N/A
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
                        participants_div = soup.find('div', {'class' : '_2lek'}).text
                        if participants_div.split(' ')[0] == "Participants:": #thisisagroupchat
                            your_name = participants_div.split(" ")[-1]
                            group_chat = True
                        messages = soup.findAll('div', {'class' : '_2let'})
                        message_list = []
                        chatname = dir.split('_')[0]
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
                                    "chatname": chatname, #this is also the chat name
                                    "sent": sent,
                                    "sender": sender,
                                    "text": text,   
                                    "date": date
                                }
                                message_list.append(message)
                        ###Do not fix duplicate names, because then you need to address it while scraping###
                        with open('json/' + chatname + '.json', 'w') as json_file:  
                            simplejson.dump(message_list, json_file)
        return #only go to 2nd level of dirs

def whatsapp_to_json(input): #This only works for iOS
    if not os.path.exists(os.getcwd() + '/json'):
        os.makedirs(os.getcwd() + '/json') 
    curr_dir = os.getcwd() + '/whatsappmessages'
    chatname = input.split('.')[0]
    with open(curr_dir + '/' + input, "rb") as messages:
        found_name = False
        message_list = []
        for message in messages:
            message = str(message, 'utf-8')
            date_split = message.split(']')
            date = date = parser.parse(date_split[0][3:]).isoformat()
            text_array = date_split[1].split(':')
            name = text_array[0].strip()
            text = ''.join(text_array[1:])
            sent = (chatname.lower().replace(" ", "") == name.lower().replace(" ", ""))
            message = {
                "chatname": chatname,
                "sent": sent,
                "sender": name,
                "text": text,
                "date": date
            }
            message_list.append(message)
        with open('json/' + chatname + '-WA' + '.json', 'w') as json_file:  
            json.dump(message_list, json_file)
