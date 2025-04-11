import requests

class SteamAPI:
    def __init__(self, STEAM_API_KEY=None):
        import os
        if STEAM_API_KEY is None:
            self.api_key = os.getenv('STEAM_API_KEY')
        else:
            self.api_key = STEAM_API_KEY
        self.api_url = "http://api.steampowered.com/"

    def GetNewsForApp(self, appID: str, entries: int = 3, max_length: int = 300):
        interface_name = "ISteamNews"
        method_name = "GetNewsForApp"
        version = 2
        format = "json"
        url = f"{self.api_url}{interface_name}/{method_name}/v000{version}/?appid={appID}&count={entries}&maxlength={max_length}&format={format}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data from Steam API: {response.status_code}")

    def GetGlobalAchievementPercentagesForApp(self, appID: str):
        interface_name = "ISteamUserStats"
        method_name = "GetGlobalAchievementPercentagesForApp"
        version = 2
        format = "json"
        url = f"{self.api_url}{interface_name}/{method_name}/v000{version}/?gameid={appID}&format={format}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data from Steam API: {response.status_code}")
        
    def GetPlayerSummaries(self, steamID: str):
        interface_name = "ISteamUser"
        method_name = "GetPlayerSummaries"
        version = 2
        format = "json"
        url = f"{self.api_url}{interface_name}/{method_name}/v000{version}/?key={self.api_key}&steamids={steamID}&format={format}"
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            if 'response' in response:
                return response['response']
        else:
            raise Exception(f"Error fetching data from Steam API: {response.status_code}")

    def GetFriendList(self, steamID: str):
        interface_name = "ISteamUser"
        method_name = "GetFriendList"
        version = 1
        format = "json"
        relationship = "friend"
        url = f"{self.api_url}{interface_name}/{method_name}/v000{version}/?key={self.api_key}&steamid={steamID}&relationship={relationship}&format={format}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data from Steam API: {response.status_code}")

    def GetPlayerAchievements(self, steamID: str, appID: str):
        interface_name = "ISteamUserStats"
        method_name = "GetPlayerAchievements"
        version = 1
        format = "json"
        url = f"{self.api_url}{interface_name}/{method_name}/v000{version}/?appid={appID}&key={self.api_key}&steamid={steamID}&format={format}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data from Steam API: {response.status_code}")
        
    def GetUserStatsForGame(self, steamID: str, appID: str):
        interface_name = "ISteamUserStats"
        method_name = "GetUserStatsForGame"
        version = 2
        format = "json"
        url = f"{self.api_url}{interface_name}/{method_name}/v000{version}/?appid={appID}&key={self.api_key}&steamid={steamID}&format={format}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data from Steam API: {response.status_code}")

    def GetOwnedGames(self, steamID: str):
        interface_name = "IPlayerService"
        method_name = "GetOwnedGames"
        version = 1
        format = "json"
        url = f"{self.api_url}{interface_name}/{method_name}/v000{version}/?key={self.api_key}&steamid={steamID}&format={format}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                response_json = response.json()
                if 'response' in response_json and 'games' in response_json['response']:
                    return response_json['response']
                else:
                    return {'games': []}
            else:
                print(f"Error fetching owned games: HTTP {response.status_code}") 
                response.raise_for_status()
        except Exception as e:
            print(f"Exception occurred while fetching owned games for Steam ID {steamID}: {e}")
            return {'games': []}
        
    def GetRecentlyPlayedGames(self, steamID: str):
        interface_name = "IPlayerService"
        method_name = "GetRecentlyPlayedGames"
        version = 1
        format = "json"
        url = f"{self.api_url}{interface_name}/{method_name}/v000{version}/?key={self.api_key}&steamid={steamID}&format={format}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data from Steam API: {response.status_code}")