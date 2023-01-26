"""
Author: João Victor David de Oliveira (j.victordavid2@gmail.com)
main.py (c) 2023
Desc: description
Created:  2023-01-26T17:39:18.321Z
Modified: 2023-01-26T18:48:47.352Z
"""

import asyncio
import json
import random
import time

from telethon import TelegramClient
from telethon.types import Channel, Chat, User
from telethon.errors import UserPrivacyRestrictedError, PeerFloodError, \
    ChatWriteForbiddenError, ChatAdminRequiredError, FloodWaitError
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest

from config import Config


# Constants
API_ID = 28680284
API_HASH = 'edb7872a5039f5ed5f68ee6278f80d80'
CACHE_FILE = 'cache.json'
CONFIG_FILE = 'config.json'
config = Config(CONFIG_FILE)
cache = Config(CACHE_FILE, {})
SESSIONS = config['sessions']

# Variables
fromGroup = config['fromGroup']
toGroup = config['toGroup']

def createTelegramClient(session: str, app_id: int, api_hash: str, receive_updates: bool = False):
    return TelegramClient(StringSession(session), app_id, api_hash, receive_updates=receive_updates)

async def connectClient(client: TelegramClient):
    check = False
    try:
        await client.connect()
    except OSError:
        print('Failed to connect on session', str(client.session))
    await asyncio.sleep(random.randint(1, 5))
    try:
        sessionMe = await client.get_me()
        if sessionMe:
            print('Connected on user ', sessionMe.first_name)
            check = True
    except Exception as e:
        print(f'Failed to connect on session {str(client.session)} {e}')
    return check

def getGroupCache(key):
    if (cache['groupCache']):
        return cache['groupCache'].get(key)
    return None

def saveGroupCache(key, data):
    if not cache['groupCache']:
        cache['groupCache'] = {}
    cache['groupCache'][key] = data
    cache.save()

async def main():
    sessionsClients: list[TelegramClient] = []
    fullAdded = 0

    for session in SESSIONS:
        client = createTelegramClient(session, API_ID, API_HASH)
        check = await connectClient(client)
        if not check:
            continue
        sessionsClients.append(client)
    if not len(sessionsClients):
        print('No sessions connected')
        return
    print(f'Connected on {len(sessionsClients)} sessions')

    toGroupEntity = None
    toGroupMembers = None
    for client in sessionsClients:
        print('Starting getting toGroup infos')
        toGroupEntityGet: Channel = await client.get_entity(toGroup)
        if not toGroupEntityGet or not toGroupEntityGet.participants_count:
            print(f'{toGroupEntityGet.title} is empty')
            continue
        print(f'{toGroupEntityGet.title} has {toGroupEntityGet.participants_count} members')
        toGroupEntity = toGroupEntityGet
        print('Getting the group Members')
        toGroupMembers = await client.get_participants(toGroup, aggressive=True)
        saveGroupCache(toGroup, toGroupMembers)
        print(f'Finish with {len(toGroupMembers)} members')
        break

    fromGroupEntity = None
    fromGroupMembers = None
    for client in sessionsClients:
        print('Starting getting fromGroup infos')
        fromGroupEntityGet: Channel = await client.get_entity(fromGroup)
        if not fromGroupEntityGet or not fromGroupEntityGet.participants_count:
            print(f'{fromGroupEntityGet.title} is empty')
            continue
        print(f'{fromGroupEntityGet.title} has {fromGroupEntityGet.participants_count} members')
        fromGroupEntity = fromGroupEntityGet
        print('Getting the group Members')
        fromGroupMembers = await client.get_participants(fromGroup, aggressive=True)
        saveGroupCache(fromGroup, toGroupMembers)
        print(f'Finish with {len(fromGroupMembers)} members')
        break

    if not toGroupEntity or not fromGroupEntity:
        print('No groups to add')
        return

    if not toGroupMembers or not fromGroupMembers:
        print('No members to add')
        return

    print('Starting to add members')

    totalClientAdded = 0

    for client in sessionsClients:
        clientAdded = 0


    # for client in sessionsClients:
    #     print('Starting to add members')

    #     clientAdded = 0
    #     floodCount = 0

    #     toGroupEntity = await client.get_entity(toGroup)

    #     try:
    #         await client(JoinChannelRequest(toGroupEntity))
    #         print('Joined to group to add')
    #     except Exception as e:
    #         print(f"Failed to join on {toGroup} {e}")

    #     toGroupMembers = await client.get_participants(toGroup, aggressive=True)

    #     print("Retrieving members...")
    #     members = await client.get_participants(fromGroup, aggressive=True)
    #     print(f"Members caught {len(members)}")

    #     filteredMembers = []
    #     print("Filtering members...")
    #     for user in members:
    #         if not user.bot and not user.is_self and user not in toGroupMembers:
    #             filteredMembers.append(user)

    #     print(f"Filtered {len(filteredMembers)} members")
    #     n = 0
    #     for member in filteredMembers:
    #         if added == 50:
    #             break
    #         n += 1
    #         if n % 50 == 0:
    #             print(f'Sleeping 2 min to prevent possible account ban')
    #             time.sleep(120)
    #         if floodCount == 10:
    #             print("Stopped script to prevent FloodWait")
    #             break
    #         try:
    #             await client(InviteToChannelRequest(toGroupEntity, [member]))
    #             print(f"Added {member.id} to {toGroupEntity.title}")
    #             added += 1
    #             fullAdded += 1
    #             time.sleep(random.randrange(20, 60))
    #         except UserPrivacyRestrictedError:
    #             continue
    #         except FloodWaitError as e:
    #             print(f"Flood wait error {e}")
    #             break
    #         except PeerFloodError:
    #             floodCount += 1
    #             continue
    #         except ChatAdminRequiredError:
    #             print("ChatAdminRequiredError")
    #             break
    #         except ChatWriteForbiddenError:
    #             print("ChatWriteForbiddenError")
    #             break
    #         except Exception:
    #             continue
    #     if added == 50:
    #         continue
    # print(f"Finally added {fullAdded} with {len(sessions)} accounts")

if __name__ == '__main__':
    asyncio.run(main())
