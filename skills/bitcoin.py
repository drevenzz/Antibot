from requests import get

uri = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
error = 'Currency API error.'
name = 'bitcoin'
desc = 'Gets current bitcoin exchange rate in USD.'

def get_rate(data):
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
