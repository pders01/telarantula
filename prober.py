from telethon.sync import TelegramClient
from settings import api_id, api_hash, phone
import json

client = TelegramClient(phone, api_id, api_hash)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

def prober():
    targets = []
    channel_dict = {}
    with open('targets.txt', 'r') as target_list:
        for line in target_list:
            channel = client.get_entity(line)
            targets.append(channel.id)
            channel_dict[channel.id] = line
    print(channel_dict)

    with open('channel_ids.txt', 'w') as out_file:
        for target in targets:
            out_file.write(str(f"{target}\n"))
        out_file.close()

    with open('channel_lookup.json', 'w', encoding='utf-8') as lo_file:
        json.dumps(channel_dict, lo_file)
        lo_file.close()

prober()
    # pprint.pp(targets)
    