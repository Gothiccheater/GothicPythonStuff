import requests
import json
from datetime import datetime, timedelta
import os

directory = "TwitchAPI"
json_path = os.path.join(directory, 'config.json')
if os.path.exists(json_path):
    with open(json_path, 'r') as json_file:
        auth_data = json.load(json_file)

        client_id = auth_data.get("client_id")
        client_secret = auth_data.get("client_secret")
        access_token = auth_data.get("access_token")
        token_expiry = datetime.strptime(auth_data.get("token_expiry", "1970-01-01"), "%Y-%m-%d")

def changeAccessToken():
    token_url = "https://id.twitch.tv/oauth2/token"
    params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "client_credentials"
    }

    current_time = datetime.now()
    expiration = timedelta(days=7)

    if (current_time - token_expiry) > expiration :

        print("Access Token is invalid, generating new one!")

        response = requests.post(token_url, params=params)

        if response.status_code == 200:
            token_data = response.json()

            auth_data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "access_token": token_data.get("access_token"),
                "token_expiry": datetime.now().strftime("%Y-%m-%d")
            }

            # Daten in JSON-Datei speichern
            with open(json_path, 'w') as json_file:
                json.dump(auth_data, json_file, indent=4)

        else:
            print("Error fetching token. Status:", response.status_code)
            print("Answer:", response.text)
    else:
        print("Access Token is valid!")


# Twitch API-URL
url = 'https://api.twitch.tv/helix/streams?user_login={channel_name}'

# Header zusammenstellen
headers = {
    'Client-Id': client_id,
    'Authorization': f'Bearer {access_token}'
}
# Array mit Channeln
channelsToCheck = []

# Funktion um channel zu prüfen
def checkLive(channel):
    # API-Anfrage senden
    for check in channel:
        print('----------------------------------------------------------------')
        channel_name = check
        response = requests.get(url.format(channel_name=channel_name), headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and data['data']:
                print(f"{channel_name} is live! Go to https://www.twitch.tv/{channel_name} to watch!")
            else:
                print(f"{channel_name} is offline.")
        else:
            print("Error: No response from Twitch!")
            print("Status: ", response.status_code)
            print("Answer: ", response.text)

# Funktion um User eingeben zu lassen, welche Channel geprüft werden sollen
def getChannels():
    print('----------------------------------------------------------------')
    while True:
        channelName = input("Enter a Channel or type 'Exit' to check for live Channels: ")
        if channelName.lower() == 'exit':
            break
        channelsToCheck.append(channelName.lower())
    return channelsToCheck

# Funktionsaufrufe um das Skript auszuführen
changeAccessToken()
getChannels()
checkLive(channelsToCheck)
input()