# setting up a client

#import pprint
import sys
import os
from settings import api_id, api_hash, phone
from datetime import datetime
from ruamel.yaml import YAML

#client = client()
from telethon import functions, types, errors
#from telethon.tl.types import InputPeerEmpty
#from telethon.tl.functions.messages import GetDialogsRequest
#from typing import Type
from telethon.sync import TelegramClient


client = TelegramClient(phone, api_id, api_hash)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


# scraping massages and photos


def prober():
    yaml = YAML()

    from telethon.tl.functions.messages import GetDialogsRequest
    from telethon.tl.types import InputPeerEmpty
    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    channel_ids = []
    channel_titles = {}

    for chat in result.chats:
        channel_ids.append(chat.id)
        channel_titles[chat.id] = chat.title

    # pprint.pp(channel_titles)

    targets = []
    for channel_id in channel_ids:
        if channel_id in [
            1152266850, 
            458119564, 
            1006503122, 
            1027214245, 
            1021345616, 
            1001839309, 
            324512588, 
            1443252557, 
            1485239691, 
            365057030, 
            1228946795]:
            continue
        else:
            targets.append(channel_id)

    # pprint.pp(targets)
    print('Targets generated!')
    return targets


yaml = YAML()

chats = []
last_date = None
chunk_size = 200
groups = []

list_messages = []
dict_messages = {}
dict_photos = {}

now = datetime.now()

message_limit = 5

def scrape(entity):
    i = 1
<<<<<<< HEAD
    for message in client.iter_messages(entity=entity):
        
        print(message.id, end='\r')
        
=======
    for message in client.iter_messages(entity=entity, limit=message_limit):
        print(f"{message.id}/0")
>>>>>>> a48f43aeda54445fd1c57754ad6d3af9808b4c68
        if message.media != None:
            message_hasMedia = True
        else:
            message_hasMedia = False
        
        if message.web_preview != None:
            message_web = message.web_preview
            message_web_description = message_web.description
            message_web_url = message_web.url
        else:
            message_web_description = None
            message_web_url = None

        list_messages.append({
            'message_id': message.id,
<<<<<<< HEAD
            'message_text': str(message.raw_text),
=======
            'message_text': str(message.text),
>>>>>>> a48f43aeda54445fd1c57754ad6d3af9808b4c68
            'message_date': message.date,
            'message_views': message.views,
            'message_forwards': message.forwards,
            'message_hasMedia': message_hasMedia,
            'message_web_description': message_web_description,
            'message_web_url': message_web_url
        })
        i += 1
    output = "{}_{}".format(entity, now.strftime("%d%m%Y_%H%M%S"))

    sys.stdout = open("{}.yml".format(output), 'w+')
<<<<<<< HEAD
    yaml.dump(list_messages, sys.stdout)
=======
    yaml.dump(dict_messages, sys.stdout)
>>>>>>> a48f43aeda54445fd1c57754ad6d3af9808b4c68

    os.system("{} {}.yml {} {}.json ".format('yj', output, '>', output))

import telethon
arg = sys.argv
try:
    scrape(arg[1])
except ValueError:
    print(f"Input entity not found, skipping ..")
    pass
except telethon.errors.rpcerrorlist.PeerIdInvalidError:
    print("An invalid Peer was used ..")
    pass


