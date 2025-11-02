import json
from typing import List, Dict, Optional

class PhoneDatabase:
    def __init__(self, data_path: str = "data/phone.json"):
        with open(data_path, 'r') as f:
            self.phones = json.load(f)
    
    def get_all_phones(self) -> List[Dict]:
        return self.phones
    
    def filter_by_price(self, min_price: int = 0, max_price: int = 200000) -> List[Dict]:
        return [p for p in self.phones if min_price <= p['price'] <= max_price]
    
    def filter_by_brand(self, brand: str) -> List[Dict]:
        return [p for p in self.phones if p['brand'].lower() == brand.lower()]
    
    def filter_by_feature(self, feature: str) -> List[Dict]:
        feature_lower = feature.lower()
        return [p for p in self.phones if any(feature_lower in f.lower() for f in p['features'])]
    
    def get_by_id(self, phone_id: int) -> Optional[Dict]:
        for phone in self.phones:
            if phone['id'] == phone_id:
                return phone
        return None
    
    def search_phones(self, query: str) -> List[Dict]:
        query_lower = query.lower()
        results = []
        for phone in self.phones:
            if (query_lower in phone['name'].lower() or 
                query_lower in phone['brand'].lower()):
                results.append(phone)
        return results
    
    def get_top_battery_phones(self, count: int = 5) -> List[Dict]:
        sorted_phones = sorted(self.phones, 
                             key=lambda x: int(x['battery'].replace('mAh', '')), 
                             reverse=True)
        return sorted_phones[:count]
    
    def get_compact_phones(self) -> List[Dict]:
        return [p for p in self.phones if p['size'] == 'Compact']