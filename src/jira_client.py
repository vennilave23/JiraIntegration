import os
import requests
from typing import Dict, Any, Optional
from .auth.token_manager import get_token, get_auth_header


class JiraClient:
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv('JIRA_BASE_URL')

    def _headers(self):
        headers = {'Accept': 'application/json'}
        auth = get_auth_header('jira')
        headers.update(auth)
        return headers

    def search(self, jql: str, max_results: int = 50, start_at: int = 0) -> Dict[str, Any]:
        # Use the newer JQL endpoint for Cloud: POST /rest/api/3/search/jql
        # Request key fields explicitly to ensure the API returns useful data
        payload = {
            'jql': jql,
            'maxResults': max_results,
            'fields': ['summary', 'status', 'assignee', 'labels']
        }
        url_jql = f"{self.base_url}/rest/api/3/search/jql"
        # POST without startAt for the first page (some Jira Cloud instances reject startAt in POST)
        if start_at == 0:
            resp = requests.post(url_jql, headers=self._headers(), json=payload, timeout=15)
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code not in (410, 404):
                resp.raise_for_status()
        # For subsequent pages, use the GET search endpoint with startAt
        params = {'jql': jql, 'maxResults': max_results, 'startAt': start_at, 'fields': ','.join(payload['fields'])}
        for ver in ('3', '2'):
            url = f"{self.base_url}/rest/api/{ver}/search"
            resp2 = requests.get(url, headers=self._headers(), params=params, timeout=15)
            if resp2.status_code == 200:
                return resp2.json()
            if resp2.status_code in (410, 404):
                continue
            resp2.raise_for_status()
        # If neither worked, raise last error
        resp.raise_for_status()
        # If the JQL endpoint is not available, fall back to older search endpoints
        if resp.status_code not in (410, 404):
            resp.raise_for_status()

        params = {'jql': jql, 'maxResults': max_results}
        for ver in ('3', '2'):
            url = f"{self.base_url}/rest/api/{ver}/search"
            resp2 = requests.get(url, headers=self._headers(), params=params, timeout=15)
            if resp2.status_code == 200:
                return resp2.json()
            if resp2.status_code in (410, 404):
                continue
            resp2.raise_for_status()
        resp2.raise_for_status()
