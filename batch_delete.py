#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telethon import TelegramClient
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterEmpty
import asyncio
import yaml

with open('credential') as f:
    credential = yaml.load(f, Loader=yaml.FullLoader)

async def batchDelete(limit=50):
    user = credential['user']
    client = TelegramClient('session_file_' + user['name'], 
        credential['api_id'], credential['api_hash'])
    await client.start(password=user['password'])
    await client.get_dialogs()
    group = await client.get_entity(credential['delete_target_group'])
    backup_group = await client.get_entity(credential['backup_group'])
    result = await client.get_messages(group, 
        search=credential['search_query'], limit=1000)
    if len(result) > limit:
        print('too manay messages to delete:', len(result))
        await client.disconnect()
        return
    for message in result:
        if credential['search_query'] not in message.raw_text:
            continue
        await client.forward_messages(backup_group, message.id, group)
        await client.delete_messages(group, message.id) # not working for media group yet
    await client.disconnect()
    
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    r = loop.run_until_complete(batchDelete())
    loop.close()