import json
from common.util import get_skill, join, split, skillable
from time import asctime

custom = {}
with open('skills/custom/skills.json') as f:
    custom = json.load(f)

skillDetails = '''[bcu]"{name}" details

[cu]Output
[c]{output}

[cu]Created
[c]{creation}

[cu]Last modified
[c]{modification}

[cu]Author
[c]<$@{author}$>
'''

@skillable
def run(data, context):
    '''
        Runs a custom skill.
    '''
    error = 'Custom skill not found'
    skill = context.sParams.lower()
    if skill not in custom.get(context.chatId, []):
        return {'message': error, 'replyTo': context.origin}
    result = custom[context.chatId][skill]['output']
    return {'message': result}

@skillable
def learn(data, context):
    '''
        Learns a new custom skill.
        It saves the output of the skill as well as the nickname and details of the user who created it.
    '''
    syntaxError = "Your custom skill's syntax is wrong."
    kiddoError = "Don't get ahead of yourself, kiddo."
    temp = split(context.sParams, sep=',')
    if len(temp) < 2: 
        return {'message': syntaxError, 'replyTo': context.origin}
    skill = temp[0].strip().lower()
    params = join(temp[1:], sep=',').strip()
    if params[0] == '$':
        return {'message': kiddoError, 'replyTo': context.origin}
    now = asctime()
    known = 're'
    if context.chatId not in custom:
        custom[context.chatId] = {}
    if skill not in custom[context.chatId]:
        known = ''
        custom[context.chatId][skill] = {
            'creation': now
        }
    custom[context.chatId][skill].update({
        'name': skill.capitalize(),
        'output': params,
        'author': context.author,
        'authorId': context.authorId,
        'modification': now
    })
    with open('skills/custom/skills.json', 'w+') as f:
        json.dump(custom, f, indent=2)
    result = f'The skill "{skill}" has just been {known}learnt.'
    return {'message': result, 'replyTo': context.origin}

@skillable
def show(data, context):
    '''
        Lists all custom skills. If used with '-v', berbosity is added.
    '''
    isVerbose = context.sParams == '-v'
    result = '[BC]Custom skills' + (' (detailed)' if isVerbose else '') + '\n\n'
    temp = []
    for skill in custom.get(context.chatId, []):
        temp.append(f'- {skill}' + (f": {custom[context.chatId][skill]['output']}" if isVerbose else ''))
    if not temp:
        temp = '[CI]* No custom skills yet *'
    else:
        temp = join(sorted(temp), sep='\n')
    result += temp
    return {'message': result}

@skillable
def forget(data, context):
    '''
        Forgets a custom skill
    '''
    error = 'That custom skill does not exist.'
    skill = context.sParams.strip().lower()
    if skill not in custom.get(context.chatId, []):
        return {'message': error, 'replyTo': context.origin}
    custom[context.chatId].pop(skill)
    with open('skills/custom/skills.json', 'w+') as f:
        json.dump(custom, f, indent=2)
    result = f'The skill "{skill}" has been forgotten. You can rest in peace now.'
    return {'message': result}

@skillable
def details(data, context):
    '''
        Shows the details of the skill and tags the user.
    '''
    error = 'That custom skill does not exist.'
    skill = context.sParams.strip().lower()
    if skill not in custom.get(context.chatId, []):
        return {'message': error, 'replyTo': context.origin}
    result = skillDetails.format(**custom[context.chatId][skill])
    return {'message': result, 'mentionUserIds': [custom[context.chatId][skill]['authorId']]}

skills = {
    'do': {
        'desc': 'Runs a custom skill. Params: <skill name>',
        'run': run
    },
    'learn': {
        'desc': 'Learns a custom skill. Usage: \n[c]"$learn <skill name>, <output>""',
        'run': learn
    },
    'list': {
        'desc': 'Lists custom skills. Optional param: -v',
        'run': show
    },
    'forget': {
        'desc': 'Forgets a custom skill. Param: <custom skill>',
        'run': forget
    },
    'skill-details': {
        'desc': 'Tags the author of the custom skill. Param: <custom skill>',
        'run': details
    }
}
