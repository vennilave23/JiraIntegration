import os
from src.auth.token_manager import get_token


def test_get_token_no_env():
    # With no env vars configured, get_token should return None (no crash)
    os.environ.pop('JIRA_TOKEN_URL', None)
    os.environ.pop('JIRA_CLIENT_ID', None)
    os.environ.pop('JIRA_CLIENT_SECRET', None)
    assert get_token('jira') is None
