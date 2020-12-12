from common.util import get_skill, join, skillable
from urllib.parse import quote_plus as quote
from requests import get

uri = 'https://newton.now.sh/api/v2/simplify/{exp}'
error = 'No valid expression found.'
name = 'solve'
desc = 'Evaluates a mathematical expression. Params: <expression>'

@skillable
def solve(data, context):
    if not context.params:
        return {'message': error, 'replyTo': origin}
    resp = get(uri.format(
        exp=quote(context.sParams)
    ))
    if resp.status_code // 100 != 2:
        return error
    result = resp.json()['result']
    result = result if result else error
    return {'message': result, 'replyTo': context.origin}

skills = {
    name: {
        'desc': desc,
        'run': solve
    }
}