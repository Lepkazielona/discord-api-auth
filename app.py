from flask import Flask, request
import requests

app = Flask(__name__)

API_ENDPOINT = 'https://discord.com/api'
CLIENT_ID = '838414833790484551'
CLIENT_SECRET = 'YgoqPRUQ9uJgbArgieLl571VjYOMx9xE'
REDIRECT_URI = 'http://localhost:5000/auth/'
GUILD_ID = '990292899210080339'
BOT_TOKEN = 'ODM4NDE0ODMzNzkwNDg0NTUx.GHCglS.rAD5h3D_QGcsUtLtJM9LLGVd_kVyA6A1bmM2ys'

@app.route('/auth/')
def auth():
    a = exchange_code(request.args.get('code'))
    userInfo = user_details(a['access_token'])
    add_guild(a['access_token'], userInfo['id'])
    return userInfo


def exchange_code(code):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
    r.raise_for_status()
    return r.json()


def user_details(token):
    headers = {
        'Authorization': f"Bearer {token}"
    }

    r = requests.get('%s/users/@me' % API_ENDPOINT, headers=headers)
    r.raise_for_status()
    return r.json()


def add_guild(token, userid):
    data = {
        'access_token': token
    }
    headers = {
        'Authorization': "Bot " + BOT_TOKEN,
        'Content-Type': 'application/json'
    }

    r = requests.put(f'%s/guilds/{GUILD_ID}/members/{userid}' % API_ENDPOINT, headers=headers, json=data)
    r.raise_for_status()


if __name__ == '__main__':
    app.run()
