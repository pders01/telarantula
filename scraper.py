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

dict_messages = {}
dict_photos = {}

now = datetime.now()
#myEntities = prober()
#output = ["{}_{}".format(id, now.strftime("%d%m%Y_%H%M%S")) for id in myEntity]
message_limit = 5

def scrape(entity):
    i = 1
    for message in client.iter_messages(entity=entity, limit=message_limit):
        print(f"{message.id}/0")
        if message.media != None:
            message_hasMedia = True
        else:
            message_hasMedia = False
        dict_messages[i] = {
            'message_id': message.id,
            'message_text': str(message.text),
            'message_date': message.date,
            'message_views': message.views,
            'message_forwards': message.forwards,
            'message_hasMedia': message_hasMedia
        }
        i += 1
    output = "{}_{}".format(entity, now.strftime("%d%m%Y_%H%M%S"))

    sys.stdout = open("{}.yml".format(output), 'w+')
    yaml.dump(dict_messages, sys.stdout)

    os.system("{} {}.yml {} {}.json ".format('yj', output, '>', output))

import telethon
arg = sys.argv
try:
    scrape(int(arg[1]))
except ValueError:
    print(f"Input entity not found, skipping ..")
    pass
except telethon.errors.rpcerrorlist.PeerIdInvalidError:
    print("An invalid Peer was used ..")
    pass


