#!/usr/bin/env python3
import amino
from getpass import getpass
from pprint import pprint
import skills
import time
from common.util import sanitize, show_message, gen_file
import os

REFRESHTIME = 300

creds = {
    'email': os.environ['AMINO_USER'],
    'password': os.environ['AMINO_PASS']
}
client = amino.Client(security=False)
client.login(**creds)
print('Logged in.')

# Helper function to send a message
def send_message(com, msg):
    sub = amino.SubClient(comId=com, profile=client.profile)
    #try:
    sub.send_message(**msg)
    #except Exception:
    #    print("Something happened. The message might have been sent anyway tho'.")

# Wait for incoming text messages
@client.callbacks.event('on_text_message')
def on_text_message(data):
    show_message(data)
    if data.message.content[0] != '$': return
    msg = skills.check(data)
    if not msg: return
    msg.update(chatId=data.message.chatId)
    send_message(data.comId, msg)

@client.callbacks.event('on_group_member_join')
def on_group_member_join(data):
    message = f'As I am alive, I might as well welcome you to this chat, <$@{data.message.author.nickname}$>.'
    msg = {
        'message': sanitize(message),
        'chatId': data.message.chatId,
        'mentionUserIds': [data.message.author.userId]
    }
    send_message(data.comId, msg)
