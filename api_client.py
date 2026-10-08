import requests
from config.config import Config

class ApiClient:
    """Centralized HTTP transport client abstraction utility wrapper."""
    
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.timeout = 15

    def get(self, url_path, headers=None):
        return requests.get(f"{self.base_url}{url_path}", headers=headers, timeout=self.timeout)

    def post(self, url_path, json_data=None, headers=None):
        return requests.post(f"{self.base_url}{url_path}", json=json_data, headers=headers, timeout=self.timeout)

    def put(self, url_path, json_data=None, headers=None):
        return requests.put(f"{self.base_url}{url_path}", json=json_data, headers=headers, timeout=self.timeout)

    def patch(self, url_path, json_data=None, headers=None):
        return requests.patch(f"{self.base_url}{url_path}", json=json_data, headers=headers, timeout=self.timeout)

    def delete(self, url_path, headers=None):
        return requests.delete(f"{self.base_url}{url_path}", headers=headers, timeout=self.timeout)
