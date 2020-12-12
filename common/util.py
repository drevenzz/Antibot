from re import sub
from datetime import datetime
from io import BytesIO
from requests import get
from pprint import pprint

# Manipulate args
split = lambda l, sep=' ': l.split(sep)
join = lambda l, sep=' ': sep.join(l).strip()

def get_skill(msg):
    data = split(msg.message.content)
    skill = data[0][1:] if len(data[0]) > 1 else ''
    params = data[1:] if len(data) > 1 else []
    return {
        'skill': skill.lower(),
        'params': params
    }

class Context:
    def __init__(self, data):
        temp = get_skill(data)
        self.skill = temp['skill']
        self.params = temp['params']
        self.sParams = join(self.params)
        self.chatId = data.message.chatId
        self.origin = data.message.messageId
        self.author = data.message.author.nickname
        self.authorId = data.message.author.userId
        self.reply = None
        self.replySrc = None
        if data.message.extensions and data.message.extensions.get('replyMessage', None) and data.message.extensions['replyMessage'].get('mediaValue', None):
            self.reply = True
            self.replySrc = data.message.extensions['replyMessage']['mediaValue'].replace('_00.', '_hq.')
            
def skillable(func):
    def wrapper(data):
        context = Context(data)
        return func(data, context)
    return wrapper

def sanitize(msg):
    result = sub(r'[\u200f\u202b\u202e\u061c\u2067]', '', msg)
    return result

def show_message(data):
    template = '[{time}] {username}: {message}'
    time = datetime.now().strftime("%H:%M:%S")
    result = template.format(
        time=time,
        username=data.message.author.nickname,
        message=data.message.content
    )
    print(result)

def gen_file(url):
    temp = get(url)
    result = BytesIO(temp.content)
    return result
