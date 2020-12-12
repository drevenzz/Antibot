from common.util import get_skill, join, skillable
from random import choice
from re import sub

error = 'You need to tag exactly one recipient.'

invuln = {
    'c906acd4-66a3-4275-8f05-3d2b86abb509', # Antitesista
    '7a954dcf-1cd5-4911-ad34-6f11eb4f4e18', # M
    '1cbe94c5-605e-4329-9904-e41e769d1858' # Rosa
}
invulnMsg = '* {username} is invulnerable *'

# Lists of choices for each command
hugs = {
    'single': ['holds one arm with the other'],
    'tag': ['kindly hugs', 'gives a warm hug to', 'strongly hugs', 'squeezes'],
    'invuln': {}
}
kills = {
    'single': ['commits suicide', 'jumps from a tall building', 'dies'],
    'tag': ['viciously murders', 'slowly dismembers', 'patiently kills', 'repeatedly stabs'],
    'invuln': {
        'c906acd4-66a3-4275-8f05-3d2b86abb509', # Antitesista
        '7a954dcf-1cd5-4911-ad34-6f11eb4f4e18', # M
        '1cbe94c5-605e-4329-9904-e41e769d1858' # Rosa
    }
}
kisses = {
    'single': ['wraps one lip around the other in a weird way'],
    'tag': ['kisses', 'passionately kisses', 'gives a french kiss to', 'kisses both cheeks of'],
    'invuln': {}
}
greetings = {
    'single': ['says hi out loud just to be able to hear it from someone, because noone else will say it'],
    'tag': ['says hi to', 'greets', 'waves at', 'salutes'],
    'invuln': {}
}
prayers = {
    'single': ['is reborn from the ashes', 'resurrects on the third day'],
    'tag': ['tries to revive', 'applies CPR to', 'repeatedly slaps the face of', 'vigorously shakes the body of'],
    'invuln': {}
}

# Universal template
template = {
    'single': '* {send} {message} *',
    'tag': '* {send} {message} {dest} *'
}

# Wrapper for all functions in this module
def interact(options):
    @skillable
    def wrapped(data, context):
        # Get the sender details
        sendId = data.message.author.userId
        send = data.message.author.nickname
        # Get the mentioned user
        if 'extensions' in data.message.json and 'mentionedArray' in data.message.json['extensions'] and len(data.message.json['extensions']['mentionedArray']) == 1:
            destId = data.message.json['extensions']['mentionedArray'][0]['uid']
        else:
            # Verify if the user is egocentric or stupid
            temp = choice(options['single'])
            message = template['single'].format(send=send, message=temp)
            return {'message': message, 'messageType': 100}
        # Get a message choice
        temp = choice(options['tag'])
        # Remove weird unicode characters and @
        dest = sub(r'[\u200c\u202c\u202d\u200e\u200f]', '', context.sParams).strip()
        dest = dest[1:] if dest[0] == '@' else dest
        message = template['tag'].format(send=send, message=temp, dest=dest)
        if not destId: return {'message': error}
        elif destId in options['invuln']:
            message = invulnMsg.format(username=dest)
        return {'message': message, 'messageType': 100}
    return wrapped

skills = {
    'hug': {
        'desc': 'Hugs a user. Optional param: @user',
        'run': interact(hugs)
    },
    'kill': {
        'desc': 'Kills a user. Optional param: @user',
        'run': interact(kills)
    },
    'kiss': {
        'desc': 'Kisses a user. Optional param: @user',
        'run': interact(kisses)
    },
    'greet': {
        'desc': 'Greets a user. Optional param: @user',
        'run': interact(greetings)
    },
    'revive': {
        'desc': 'Revives a user. Optional param: @user',
        'run': interact(prayers)
    }
}
