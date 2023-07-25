import requests

# Twitch API-URL
url = 'https://api.twitch.tv/helix/streams?user_login={channel_name}'

# Twitch API-Zugriffsschlüssel und Client-ID
secret = 'zn2ldxf4v5y41q7s4n0023lhbzc09s'
access_token = 'io5vysyh4uwh6exyv3ujzbjhv18oq5'
client_id = 'g24x6dbenz9fkmwott2m0ixay11nph'

# Header zusammenstellen
headers = {
    'Client-Id': client_id,
    'Authorization': f'Bearer {access_token}'
}

def checkLive(channel):
# API-Anfrage senden
    for check in channel:
        channel_name = check
        response = requests.get(url.format(channel_name=channel_name), headers=headers)
        data = response.json()
        if 'data' in data and data['data']:
            print(f"{channel_name} is live!")
        else:
            print(f"{channel_name} is offline.")

checkChannels = ['dustiria', 'gothiccheater', 'gronkh', 'papaplatte']

checkLive(checkChannels)