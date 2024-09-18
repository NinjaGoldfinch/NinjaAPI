import requests
from datetime import datetime

from classes.data import bazaar_data

class updater:
    def __init__(self, bazaar_url, listener_server, user_agent) -> None:
        self.session = requests.Session()
        self.running = False
    
        self.bazaar_url = bazaar_url
        self.api_server = listener_server
        self.user_agent = user_agent
        self.cache = {
            'last_updated': {
                'timestamp': 0,
                'timestring': "",
                'data': {}
            }
        }
        
    def get_data(self) -> bazaar_data:
        data = self.session.get(self.bazaar_url, headers={'User-Agent': self.user_agent})
        return bazaar_data(data)
    
    def cache_data(self, data: bazaar_data) -> None:
        self.cache['last_updated']['timestamp'] = data.timestamp
        self.cache['last_updated']['timestring'] = data.last_updated
        self.cache['last_updated']['data'] = data.json()
        
    def send_to_server(self, data: bazaar_data) -> None:
        try:
            self.session.post(self.api_server, json=data.json())
            print(f"Data sent to server at {datetime.now()}")
        except requests.exceptions.RequestException as e:
            print(e)
    
    def update(self) -> None:
        response = self.get_data()
        if type(response) == bazaar_data:
            if self.cache['last_updated']['timestamp'] != response.timestamp:
                self.cache_data(response)
                self.send_to_server(response)
                
                print(f"Cache updated at {datetime.now()}")
        else:
            print("Error getting data")
    
    def run(self) -> None:
        self.running = True
        
        while self.running:
            self.update()
        
    def stop(self) -> None:
        self.running = False
        self.session.close()
        
        
def start_updater(bazaar_url, listener_server, user_agent) -> None:
    updater_instance = updater(bazaar_url, listener_server, user_agent)
    updater_instance.run()
    
    return updater_instance