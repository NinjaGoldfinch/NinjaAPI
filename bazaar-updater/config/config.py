import yaml

class config_loader:
    def __init__(self) -> None:
        try:
            with open('config/config.yml') as config:    
                try:
                    self.config = yaml.safe_load(config)
                except yaml.YAMLError as exc:
                    print("Error loading config.yml. Config has been set to default.")
                    print(exc)
                    self.config = self.default_config()
                    
        except FileNotFoundError as exc:
            self.config = self.default_config()

        if self.config == None: # Config file is empty
            print("Config file is empty. User-defined config has been set to default.")
            self.config = self.default_config()
        
    def default_config(self) -> dict:
        return {
            "bazaar_url": "https://api.hypixel.net/skyblock/bazaar",
            "listener_server": "http://localhost:5050",
            "user_agent": "NinjaBot/0.1"
        }
        
    def get_config(self) -> dict:
        return self.config
    
    def get(self, item: str) -> str:
        if item in self.config:
            value = self.config[item]
            print(f"Config value {item} set to {value}.")
        elif item in self.default_config():
            value = self.default_config()[item]
            print(f"Config value {item} not found in user-defined configuration. Defaulting to default value {value}.")
        else:
            value = None
            print(f"Config query {item} not found in any configuration file. Defaulting to {value}.")
        
        return value