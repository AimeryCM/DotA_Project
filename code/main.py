import requests
import json

STEAM_KEY_SOURCE = "../steam_web_api_key.txt"

#main
steam_key = open(STEAM_KEY_SOURCE).read()
matchID = {'key' : steam_key}
response = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1', params=matchID)
#response = requests.get('https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=440&count=3')
response_json = response.json()
print(response_json['result']['num_results'])