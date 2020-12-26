from skills import base, bitcoin, newton, usery, custom, media, speak
from common.util import get_skill, sanitize
from re import sub

skills = base.skills
modules = [bitcoin, newton, usery, custom, media, speak]
for module in modules:
    skills.update(module.skills)

error = {'message': "I don't have that skill yet."}
# Check for skills
def check(msg):
    temp = get_skill(msg)
    if temp['skill'] in skills:
        result = skills[temp['skill']]['run'](msg)
        result = result if result else error
        result['message'] = sanitize(result['message'])
        return result
    return error
