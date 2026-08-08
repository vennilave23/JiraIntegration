import os
import time
import json
from typing import Optional
import requests

TOKEN_CACHE_PATH = os.path.expanduser('~/.jira_integration_tokens.json')


class TokenManager:
    """Simple token manager supporting client-credentials token exchange.

    This is a minimal implementation for local/dev use. In production use a
    secure secret manager and a more robust library.
    """

    def __init__(self):
        self._cache = self._load_cache()

    def _load_cache(self):
        try:
            with open(TOKEN_CACHE_PATH, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_cache(self):
        try:
            with open(TOKEN_CACHE_PATH, 'w') as f:
                json.dump(self._cache, f)
            os.chmod(TOKEN_CACHE_PATH, 0o600)
        except Exception:
            pass

    def get_token(self, service: str) -> Optional[str]:
        """Return a valid access token for `service` (e.g. 'jira' or 'confluence')."""
        entry = self._cache.get(service)
        if entry and entry.get('expires_at', 0) > time.time() + 30:
            return entry['access_token']

        # Acquire new token via client-credentials flow
        token_url = os.getenv(f'{service.upper()}_TOKEN_URL')
        client_id = os.getenv(f'{service.upper()}_CLIENT_ID')
        client_secret = os.getenv(f'{service.upper()}_CLIENT_SECRET')
        if not token_url or not client_id or not client_secret:
            return None

        resp = requests.post(
            token_url,
            data={'grant_type': 'client_credentials'},
            auth=(client_id, client_secret),
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        access_token = data['access_token']
        expires_in = data.get('expires_in', 3600)
        self._cache[service] = {
            'access_token': access_token,
            'expires_at': time.time() + int(expires_in),
        }
        self._save_cache()
        return access_token


# module-level singleton for convenience
_TM = TokenManager()


def get_token(service: str) -> Optional[str]:
    return _TM.get_token(service)


def get_auth_header(service: str) -> dict:
    """Return an Authorization header dict for the given service.

    Priority:
    1. API token (env: SERVICE_API_EMAIL + SERVICE_API_TOKEN) -> Basic
    2. OAuth2 client-credentials via token endpoint -> Bearer
    3. Empty dict if no auth available
    """
    service_up = service.upper()
    api_email = os.getenv(f'{service_up}_API_EMAIL')
    api_token = os.getenv(f'{service_up}_API_TOKEN')
    headers = {}
    if api_email and api_token:
        import base64

        creds = f"{api_email}:{api_token}".encode('utf-8')
        b64 = base64.b64encode(creds).decode('ascii')
        headers['Authorization'] = f'Basic {b64}'
        return headers

    token = _TM.get_token(service)
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers
