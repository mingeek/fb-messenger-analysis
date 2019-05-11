import os
import json
from bs4 import BeautifulSoup
from dateutil import parser
from tqdm import tqdm as pbar
from textblob import TextBlob
from whatsapptojson import whatsapptojson


#Input: Text to be removed and an optional list of words to remove
#Returns: Text with cursewords removed
def remove_word(text, remove = ['fuck','bitch','shit','idiot', 'sick', 'lit']): #cursewords only used in derogatry manners not set by default
    for word in remove:
        text = text.replace(word, "")
    return text

#Requirement: The Facebook messages must be in {current_dir}/messages in the way they were downloaded
#Input: N/A
def fb_to_json():
    if not os.path.exists(os.getcwd() + '/json'):
        os.makedirs(os.getcwd() + '/json')    
    chats = {}
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
                        participants = set()
                        chatname = dir.split('_')[0]
                        for message in pbar(messages, desc=conv_name):
                            sender = message.previous_sibling.text
                            div = message.findChild()
                            if len(div.findChildren()) == 4:#otherwise it's an image or file or something
                                text = div.findChildren()[1].text
                                date = parser.parse(message.next_sibling.text).isoformat()
                                sentiment = TextBlob(remove_word(text)).sentiment[0]
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
                                    "sentiment": sentiment,  
                                    "date": date
                                }
                                message_list.append(message)
                                participants.add(sender)
                        ###Do not fix duplicate names, because then you need to address it while scraping###
                        store = {
                            "messages": message_list,
                            "participants": sender
                        }
                        with open('json/' + chatname + '.json', 'w') as json_file:  
                            json.dump(store, json_file, indent=2)
                        chats[dir] = chatname
        with open('friends.json', 'w') as json_file:  
            json.dump(chats, json_file, indent=2)
        return #only go to 2nd level of dirs