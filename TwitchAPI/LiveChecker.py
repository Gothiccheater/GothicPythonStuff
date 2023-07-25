import requests
import config

# Twitch API-URL
url = 'https://api.twitch.tv/helix/streams?user_login={channel_name}'

# Header zusammenstellen
headers = {
    'Client-Id': config.client_id,
    'Authorization': f'Bearer {config.access_token}'
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