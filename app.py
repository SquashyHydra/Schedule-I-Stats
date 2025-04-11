import os
import Save
from Steam import SteamAPI
import webview
import argparse
import sys
import tempfile

# Set the PYTHONNET_PYDLL environment variable
python_dll_path = os.path.join(os.path.dirname(sys.executable), "python39.dll")  # Adjust for your Python version
os.environ["PYTHONNET_PYDLL"] = python_dll_path

os.environ["PYTHONNET_RUNTIME"] = "netfx"

if getattr(sys, 'frozen', False):
    frontend_dir = os.path.join(os.path.join(tempfile.gettempdir(), "Schedule I Stats"), "frontend")
else:
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")

schedule_I_steam_appid = "3164500"

save_fetcher = Save.SaveFetcher()
steam_api = SteamAPI()

class SteamAppGUI:
    def __init__(self):
        self.save_path_info = save_fetcher.get_info()
        self.selected_account = None
        self.selected_save_folder = None
        self.steamID = None
        
    def check_steam_api_key(self):
        """Check if the Steam API key is set in the environment."""
        return os.getenv("STEAM_API_KEY") is not None

    def set_steam_api_key(self, api_key: str):
        """Set the Steam API key in the user's environment variables."""
        try:
            import winreg  # Use Windows Registry to store the API key
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Environment")
            winreg.SetValueEx(key, "STEAM_API_KEY", 0, winreg.REG_SZ, api_key)
            winreg.CloseKey(key)
            os.environ["STEAM_API_KEY"] = api_key
            steam_api.api_key = api_key
            return {"status": "success", "message": "Steam API key saved successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_steam_account_info(self, steamID: str) -> dict:
        try:
            player_summary = steam_api.GetPlayerSummaries(steamID)['players'][0]
            owned_games = steam_api.GetOwnedGames(steamID)['games']
            account_summery = {
                'community_visibility_state': player_summary['communityvisibilitystate'],
                'profile_state': player_summary['profilestate'],
                'steam_name': player_summary['personaname'],
                'avatar_url': player_summary['avatarfull'],
                'avatar_medium': player_summary['avatarmedium'],
                'avatar': player_summary['avatar'],
            }
            schedule_I_owned = False
            for game_info in owned_games:
                appID = str(game_info['appid'])
                if appID == schedule_I_steam_appid:
                    schedule_I_owned = True
            return {
                steamID: {
                    'account_summary': account_summery,
                    'Schedule_I_owned': schedule_I_owned,
                },
            }
        except Exception as e:
            print(f"Error fetching data for {steamID}: {e}")
            return None

    def fetch_accounts(self):
        accounts = []
        for key, value in self.save_path_info.items():
            if isinstance(value, str) and os.path.isdir(value):
                if key.isdigit():
                    steamID = key
                    try:
                        steam_account_info = self.get_steam_account_info(steamID)
                        accounts.append(steam_account_info)
                    except Exception as e:
                        print(f"Error fetching friend list for {steamID}: {e}")
            else:
                raise ValueError(f"Invalid path: {value}\n{key} {value}")
        return accounts

    def select_account(self, account):
        self.selected_account = account
        return {"status": "success", "selected_account": account}

    def get_save_folders(self):
        if not self.selected_account:
            raise Exception("No account selected.")

        # Ensure the selected account key is accessed correctly
        if isinstance(self.selected_account, dict):
            account_key = list(self.selected_account.keys())[0]  # Get the first key from the dictionary
            self.steamID = account_key
        else:
            raise Exception("Selected account is not in the expected format.")

        accounts_save_path = self.save_path_info.get(account_key)

        save_folders = [folder for folder in os.listdir(accounts_save_path) if os.path.isdir(os.path.join(accounts_save_path, folder))]

        return {"status": "success", "save_folders": save_folders}

    def load_stats(self):
        if not self.selected_account:
            raise Exception("No account selected.")

        webview.windows[0].load_url(os.path.join(frontend_dir, "loading.html"))
        return {"status": "stats_loaded"}

    def select_save_folder(self, folder_name):
        try:
            self.selected_save_folder = folder_name

            folder_path = os.path.join(self.save_path_info.get(self.steamID), self.selected_save_folder)
            account = self.selected_account.get(self.steamID)
            account_info = {}
            account_info["steam_ID"] = self.steamID
            for key, value in account.items():
                account_info[key] = value
            account_info['save_folder'] = folder_path
            return {"status": "success", "account_info": account_info}
        except Exception as e:
            print(f"Error selecting save folder: {e}")
            return {"status": "error", "message": str(e)}

    def get_save_data(self):
        try:
            if not self.selected_save_folder:
                raise Exception("No save folder selected.")
            
            account_info = {
                "account_summary": self.selected_account.get(self.steamID),
                "save_folder": os.path.join(self.save_path_info.get(self.steamID), self.selected_save_folder),
                "selected_save": self.selected_save_folder,
                "steam_ID": self.steamID
            }
            save_collector = Save.save_data()
            account_info = save_collector.collector(account_info)

            return {"status": "success", "data": account_info}
        except Exception as e:
            print(f"Error fetching save data: {e}")
            return {"status": "error", "message": str(e)}

    def load_save_data_page(self):
        webview.windows[0].load_url(os.path.join(frontend_dir, "stats.html"))
        return {"status": "save_data_page_loaded"}

# Initialize the GUI and start the PyWebView window
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Schedule I Save Game Data Display")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("--gui", choices=["cef", "edgechromium", "qt", "winforms"], default="winforms", help="Specify the GUI backend.")
    args = parser.parse_args()

    gui = SteamAppGUI()

    webview.create_window(
        "Steam Account Info",
        os.path.join(frontend_dir, "accounts.html"),
        js_api=gui,
        width=1280,
        height=720,
        zoomable=False,
        resizable=True
    )
    webview.start(debug=args.debug, gui=args.gui)  # Specify the GUI backend explicitly