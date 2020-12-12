import requests
from common.util import gen_file, skillable, join
import json
from time import asctime

mediaDetails = '''[bcu]"{name}" details

[cu]Output
[c]{output}

[cu]Created
[c]{creation}

[cu]Last modified
[c]{modification}

[cu]Author
[c]<$@{author}$>
'''

files = {}
with open('skills/media/src.json') as f:
    files = json.load(f)

@skillable
def save(data, context):
    syntaxError = 'No name found for the file.'
    fileError = 'No valid media found.'
    typeError = 'Not supported media type.'
    success = 'The {mediaType} "{name}" has been {known}created.'
    if not context.sParams:
        return {'message': syntaxError, 'replyTo': context.origin}
    if not context.reply:
        return {'message': fileError, 'replyTo': context.origin}
    name = context.sParams
    now = asctime()
    known = 're'
    if context.chatId not in files:
        files[context.chatId] = {}
    if name not in files[context.chatId]:
        known = ''
        files[context.chatId][name] = {
            'creation': now
        }
    extension = context.replySrc.split('.')[-1]
    if extension == 'jpg':
        mediaType = 'image'
    elif extension == 'gif':
        mediaType = 'gif'
    elif extension == 'aac':
        mediaType = 'audio'
    else:
        return {'message': typeError, 'replyTo': context.origin}
    files[context.chatId][name].update({
        'name': name.capitalize(),
        'output': context.replySrc,
        'type': mediaType,
        'author': context.author,
        'authorId': context.authorId,
        'modification': now
    })
    with open('skills/media/src.json', 'w+') as f:
        json.dump(files, f, indent=2)
    return {
        'message': success.format(
            mediaType=mediaType,
            name=name,
            known=known),
        'replyTo': context.origin
    }

@skillable
def resend(data, context):
    syntaxError = 'You need to give me a name.'
    fileError = 'File not found.'
    success = 'There you go.'
    if not context.sParams:
        return {'message': syntaxError, 'replyTo': context.origin}
    if context.sParams not in files.get(context.chatId, []):
        return {'message': fileError, 'replyTo': context.origin}
    temp = gen_file(files[context.chatId][context.sParams]['output'])
    return {'message': success, 'file': temp, 'fileType': files[context.chatId][context.sParams]['type']}

@skillable
def show(data, context):
    result = '[bcu]Available media\n\n'
    temp = []
    for name in files.get(context.chatId, []):
        temp.append(f'- {name}')
    if temp:
        result += join(temp, sep='\n')
    else:
        result += '[ci]* No available media *'
    return {'message': result}

@skillable
def delete(data, context):
    syntaxError = 'You need to give me a name.'
    fileError = 'File not found.'
    success = 'The {type} "{name}" has been deleted.'
    if not context.sParams:
        return {'message': syntaxError, 'replyTo': context.origin}
    if context.sParams not in files.get(context.chatId, []):
        return {'message': fileError, 'replyTo': context.origin}
    deleted = files[context.chatId].pop(context.sParams)
    with open('skills/media/src.json', 'w+') as f:
        json.dump(files, f, indent=2)
    return {'message': success.format(type=deleted['type'], name=context.sParams), 'replyTo': context.origin}

@skillable
def details(data, context):
    '''
        Shows the details of the media and tags the user.
    '''
    error = 'File not found.'
    name = context.sParams.strip().lower()
    if name not in files[context.chatId]:
        return {'message': error, 'replyTo': context.origin}
    result = mediaDetails.format(**files[context.chatId][name])
    return {'message': result, 'mentionUserIds': [files[context.chatId][name]['authorId']]}

skills = {
    'save': {
        'desc': 'Saves media for future use. Params: <name>',
        'run': save
    },
    'show': {
        'desc': 'Shows saved media. Params: <name>',
        'run': resend
    },
    'media': {
        'desc': 'Lists all available media.',
        'run': show
    },
    'delete': {
        'desc': 'Deletes saved media. Params: <name>',
        'run': delete
    },
    'media-details': {
        'desc': 'Shows details of the media. Params: <name>',
        'run': details
    }
}
