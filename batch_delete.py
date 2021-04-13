#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telethon import TelegramClient
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterEmpty
import asyncio
from settings import Settings

with open('credential') as f:
    credential = yaml.load(f, Loader=yaml.FullLoader)

async def batchDelete(group):
    user = credential['user']
    client = TelegramClient('session_file_' + user['name'], 
        credential['api_id'], credential['api_hash'])
    await client.start(password=user['password'])
    group = await client.get_entity(credential['delete_target_group'])
    print(group.id)
    backup_group = await client.get_entity(credential['backup_group'])
    filter = InputMessagesFilterEmpty()
    result = await client(SearchRequest(
        peer=group,     # On which chat/conversation
        q=credential['search_query'], # What to search for
        filter=filter,  # Filter to use (maybe filter for media)
        min_date=None,  # Minimum date
        max_date=None,  # Maximum date
        offset_id=0,    # ID of the message to use as offset
        add_offset=0,   # Additional offset
        limit=1000,       # How many results
        max_id=0,       # Maximum message ID
        min_id=0,       # Minimum message ID
        from_id=0,
        hash=0
    ))
    for message in result.messages:
        await client.forward_messages(backup_group, message.id, group)
        await client.delete_messages(group, message.id) # not working for media group yet
    await client.disconnect()
    
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    r = loop.run_until_complete(batchDelete())
    loop.close()