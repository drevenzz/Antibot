'''
This is just a skill for Christmas time.
Am an atheist tho'.
'''

from common.util import gen_file, skillable
import random
import json

villancicos = []

try:
    with open('skills/speak/villancicos.json') as f:
        villancicos = json.load(f)
except Exception:
    with open('skills/speak/villancicos.json', 'w+') as f:
        json.dump(villancicos, f, indent=2)

@skillable
def play_villancico(data, context):
    villancico = random.choice(villancicos)
    print(villancico['name'])
    result = {
        'message': villancico['name'],
        'file': gen_file(villancico['url']),
        'fileType': 'audio'
    }
    return result

skills = {
    'villancico': {
        'desc': 'Plays a random villancico.',
        'run': play_villancico
    }
}