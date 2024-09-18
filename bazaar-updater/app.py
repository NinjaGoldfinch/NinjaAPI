import yaml
from update import start_updater

import os

# Get environment variable
docker_container = os.getenv('DOCKER_CONTAINER', False)

print(docker_container)

if docker_container:
    print("Docker container found. Using enviroment variables.")
    bazaaar_url = os.getenv('BAZAAR_URL')
    listener_service = os.getenv('API_SERVER')
    user_agent = os.getenv('USER_AGENT')
else:
    from config.config import config_loader
    
    print("Script is not running in a Docker container. Using config file.")

    if not os.path.exists("config/config.yml"):
        print("Config file not found. Creating default.")
        
        os.makedirs("config", exist_ok=True)
        default_config = config_loader().default_config()

        with open("config/config.yml", "w") as config_file:
                yaml.dump(default_config, config_file)
                print("Default config created. Please edit the config file and restart the app.")
                exit()
    
    config = config_loader()
    
    bazaaar_url = config.get('bazaar_url')
    listener_service = config.get('listener_server')
    user_agent = config.get('user_agent')

print(f"Starting updater with bazaar URL {bazaaar_url}, listener server {listener_service}, and user agent {user_agent}")

# Start updater
start_updater(bazaaar_url, listener_service, user_agent)