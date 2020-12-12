from common.util import skillable

# This module manages actions and users in a chat

error = 'Currency API error.'
name = 'bitcoin'
desc = 'Gets current bitcoin exchange rate in USD.'

@skillable
def get_rate(data, context):
    resp = get(uri)
    if resp.status_code // 100 != 2:
        return error
    result = resp.json()['bitcoin']['usd']
    result = f'{result} USD' if result else error
    return {'message': result}

skills = {
    name: {
        'desc': desc,
        'run': get_rate
    }
}
