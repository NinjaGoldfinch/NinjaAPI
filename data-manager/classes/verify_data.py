import json

def verify_bazaar_data(data: dict):
    if data.get('products', None) is None:
        return False
    
    return True