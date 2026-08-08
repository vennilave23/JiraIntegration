import os
import requests
from typing import Dict, Any, Optional
from .auth.token_manager import get_token, get_auth_header


class ConfluenceClient:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv('CONFLUENCE_BASE_URL')

    def _headers(self):
        headers = {'Accept': 'application/json'}
        auth = get_auth_header('confluence')
        headers.update(auth)
        return headers

    def get_page(self, page_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/wiki/rest/api/content/{page_id}"
        resp = requests.get(url, headers=self._headers(), timeout=15)
        resp.raise_for_status()
        return resp.json()
