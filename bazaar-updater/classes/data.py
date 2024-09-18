# This file contains the data classes for the bazaar-updater
from datetime import datetime
from requests import Response


class bazaar_data:
    def __init__(self, requests_data: Response) -> None:
        self.data = requests_data
        self.last_updated = requests_data.headers['last-modified']
        self.timestamp = datetime.timestamp(datetime.strptime(self.last_updated, "%a, %d %b %Y %H:%M:%S GMT"))
        
        self.headers = requests_data.headers
        
    def json(self):
        return self.data.json()