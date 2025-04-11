import os
import json

class SaveFetcher:
    def __init__(self):
        self.local_low_path = self.get_local_low_path()
        self.game_save_path = self.get_Game_Save_Folder()

    @staticmethod
    def get_local_low_path() -> str:
        return os.path.join(os.getenv('USERPROFILE', ''), 'AppData', 'LocalLow')

    def get_Game_Save_Folder(self) -> str:
        game_save_path = os.path.join(self.local_low_path, 'TVGS', 'Schedule I', 'Saves')
        if not os.path.exists(game_save_path):
            raise FileNotFoundError(f"Game save folder not found: {game_save_path}")
        else:
            return game_save_path
        
    def get_steam_account_folder(self) -> list:
        steam_account_folders = [f for f in os.listdir(self.game_save_path) if os.path.isdir(os.path.join(self.game_save_path, f))]
        if not steam_account_folders:
            raise FileNotFoundError("No Steam account folders found in the game save folder.")
        else:
            return [str(os.path.join(self.game_save_path, f)) for f in steam_account_folders if f.isdigit()]

    def get_info(self) -> dict:
        try:
            save_path_info = {
                'local_low_path': self.local_low_path,
                'game_save_path': self.game_save_path,
            }
            steam_account_folders = self.get_steam_account_folder()
            for path in steam_account_folders:
                save_path_info[os.path.basename(path)] = path
            return save_path_info
        except Exception as e:
            raise Exception(f"Error fetching save path info: {e}")
        
class save_data():
    def __init__(self):
        self.selected_account = None
        self.selected_save_folder = None
        self.steamID = None
        self.BulkSave = None

    def get_json_data(self, save_folder, file):
        if "\\" or "/" in file:
            file = file.split("\\") if "\\" in file else file.split("/")
            if isinstance(file, list):
                for f in file:
                    if f.endswith('.json'):
                        file_json = os.path.join(save_folder, f)
                        break
                    else:
                        save_folder = os.path.join(save_folder, f)
        else:
            file_json = os.path.join(save_folder, file)

        if not os.path.exists(file_json):
            raise FileNotFoundError(f"{os.path.basename(file_json)} file does not exist in the save folder: {file_json}")

        with open(file_json, 'r') as file:
            file_data = file.read()

        if not file_data:   
            raise ValueError(f"{os.path.basename(file_json)} file is empty.")
        
        try:
            file_data = json.loads(file_data)
        except json.JSONDecodeError:
            raise ValueError(f"Failed to decode JSON from {os.path.basename(file_json)} file.")
        
        if not isinstance(file_data, dict):
            raise ValueError(f"{os.path.basename(file_json)} file does not contain valid JSON data.")
        return file_data

    def save_game_data(self, save_folder):
        game_data = {}

        rank_conversion = ["Street Rat", "Hoodlum", "Peddler", "Hustler", "Bagman", "Enforcer", "Shot Caller", "Block Boss", "Underlord", "Baron", "Kingpin"]
        tier_conversion = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

        game_json = self.get_json_data(save_folder, 'Game.json')
        
        Organization_Name = game_json.get('OrganisationName')
        World_seed = game_json.get('Seed')
        Console_Enbaled = game_json.get('Settings').get('ConsoleEnabled')

        money_json = self.get_json_data(save_folder, 'Money.json')
        Online_Balance = money_json.get('OnlineBalance')
        Networth_balance = money_json.get('Networth')
        lifetime_earnings = money_json.get('LifetimeEarnings')

        rank_json = self.get_json_data(save_folder, 'Rank.json')
        Rank = rank_json.get('Rank')
        Tier = rank_json.get('Tier')
        tier_xp = rank_json.get('XP')
        total_xp = rank_json.get('TotalXP')

        time_json = self.get_json_data(save_folder, 'Time.json')
        time_played_seconds = time_json.get('Playtime')

        game_data['OrganisationName'] = Organization_Name
        game_data['WorldSeed'] = World_seed
        game_data['ConsoleEnabled'] = Console_Enbaled
        game_data['OnlineBalance'] = round(float(Online_Balance), 2)
        game_data['Networth'] = round(float(Networth_balance), 2)
        game_data['LifetimeEarnings'] = round(float(lifetime_earnings), 2)
        game_data['Rank'] = rank_conversion[int(Rank)]
        game_data['Tier'] = tier_conversion[int(Tier)]
        game_data['XP'] = tier_xp
        game_data['TotalXP'] = total_xp
        game_data['TimePlayed'] = round((int(time_played_seconds)) / 3600)
        return  game_data
    
    def get_variable_data(self, save_folder):
        variable_data = {}

        acid_json = self.get_json_data(save_folder, "Variables\\acid_acquired.json")
        phosphorus_json = self.get_json_data(save_folder, "Variables\\phosphorus_acquired.json")
        acid_count = acid_json.get('Value')
        phosphorus_count = phosphorus_json.get('Value')
        variable_data['AcidCount'] = acid_count
        variable_data['PhosphorusCount'] = phosphorus_count

        collected_trash_json = self.get_json_data(save_folder, "Variables\\ContainedTrashItems.json")
        collected_trash_count = collected_trash_json.get('Value')
        variable_data['CollectedTrashCount'] = collected_trash_count

        trash_bagged_json = self.get_json_data(save_folder, "Variables\\TrashContainersBagged.json")
        trash_bagged_count = trash_bagged_json.get('Value')
        variable_data['TrashBaggedCount'] = trash_bagged_count

        dead_drop_order_json = self.get_json_data(save_folder, "Variables\\Deaddrops_Ordered.json")
        dead_drop_count = dead_drop_order_json.get('Value')
        variable_data['DeadDropCount'] = dead_drop_count

        shirley_deaddrop_json = self.get_json_data(save_folder, "Variables\\ShirleyDeaddropOrders.json")
        shirley_deaddrop_count = shirley_deaddrop_json.get('Value')
        variable_data['ShirleyDeaddropCount'] = shirley_deaddrop_count

        benji_completed_deals_json = self.get_json_data(save_folder, "Variables\\Benji_CompletedDealCount.json")
        benji_completed_deals_count = benji_completed_deals_json.get('Value')
        variable_data['BenjiCompletedDealsCount'] = benji_completed_deals_count

        completed_contracts_json = self.get_json_data(save_folder, "Variables\\Completed_Contracts_Count.json")
        completed_contracts = completed_contracts_json.get('Value')
        variable_data['CompletedContractsCount'] = completed_contracts

        runninggame_json = self.get_json_data(save_folder, "Variables\\RunGameHighScore.json")
        runninggame_highscore = runninggame_json.get('Value')
        variable_data['RunningGameHighScore'] = round(float(runninggame_highscore))

        packed_product_json = self.get_json_data(save_folder, "Variables\\PackagedProductCount.json")
        packed_product_count = packed_product_json.get('Value')
        variable_data['PackedProductCount'] = packed_product_count

        sample_success_json = self.get_json_data(save_folder, "Variables\\SuccessfulSampleCount.json")
        sample_success_count = sample_success_json.get('Value')
        variable_data['SampleSuccessCount'] = sample_success_count

        sample_rejected_json = self.get_json_data(save_folder, "Variables\\SampleRejectionCount.json")
        sample_rejected_count = sample_rejected_json.get('Value')
        variable_data['SampleRejectedCount'] = sample_rejected_count

        return variable_data
    
    def get_save_trash_world_state(self, save_folder):
        trash_data = {}
        trash_json = self.get_json_data(save_folder, "Trash\\Trash.json")
        trash_items = trash_json.get('Items')
        trash_count = len(trash_items)

        trash_data['TrashCount'] = trash_count
        return trash_data
    
    def get_created_products(self, save_folder):
        created_products = {}
        created_products_json = self.get_json_data(save_folder, "Products\\Products.json")
        created_products_list = created_products_json.get('DiscoveredProducts')
        created_products_count = len(created_products_list)

        created_products['CreatedProductsCount'] = created_products_count
        return created_products

    def collector(self, account_info):
        self.selected_account = account_info.get('account_summary').get('steam_name')
        self.selected_save_folder = account_info.get('save_folder')
        self.steamID = account_info.get('steam_ID')

        if not self.selected_save_folder:
            raise Exception("No save folder selected.")
        
        if not os.path.exists(self.selected_save_folder):
            raise FileNotFoundError(f"Save folder does not exist: {self.selected_save_folder}")

        game_data = self.save_game_data(self.selected_save_folder)

        variable_data = self.get_variable_data(self.selected_save_folder)

        trash_data = self.get_save_trash_world_state(self.selected_save_folder)

        created_products = self.get_created_products(self.selected_save_folder)

        account_info['game_data'] = game_data
        account_info['variable_data'] = variable_data
        account_info['trash_data'] = trash_data
        account_info['product_info'] = created_products

        self.BulkSave = account_info

        return self.BulkSave