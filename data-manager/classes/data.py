import json

class bazaar_data:
    def __init__(self, data: dict) -> None:
        self.data = data
        self.products = self.data.get('products', [])
        self.last_updated = self.data.get('last_updated', None)
        
        self.products_formatted = {product_name: {'price_info': {item: product_info.get('quick_status', {}).get(item, None) for item in ['sellPrice', 'sellVolume', 'sellMovingWeek', 'sellOrders', 'buyPrice', 'buyVolume', 'buyMovingWeek', 'buyOrders']}, 'sell_summary': product_info.get('sell_summary', None), 'buy_summary': product_info.get('buy_summary', None)} for product_name, product_info in self.products.items()}
        