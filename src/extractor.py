import logging
from .jira_client import JiraClient
from .confluence_client import ConfluenceClient
from .db import get_session, engine
from .models import Base, Issue, ConfluencePage
import os

logger = logging.getLogger(__name__)


def init_db():
    Base.metadata.create_all(bind=engine)


def extract_issues(jql: str = 'project = TEST AND issuetype = Story ORDER BY updated DESC'):
    client = JiraClient()
    session = get_session()
    start_at = 0
    page = 0
    while True:
        page += 1
        data = client.search(jql, max_results=50, start_at=start_at)
        issues = data.get('issues', [])
        if not issues:
            break
        for it in issues:
            key = it.get('key')
            if not key:
                logger.warning('Skipping issue without key: %s', it.get('id'))
                continue
            fields = it.get('fields', {})
            status = (fields.get('status') or {}).get('name')
            assignee = (fields.get('assignee') or {}).get('displayName') if fields.get('assignee') else None
            summary = fields.get('summary')
            labels = fields.get('labels')
            epic = None
            # common epic link customfield key
            if fields.get('customfield_10008'):
                epic = fields.get('customfield_10008')
            # upsert by key
            existing = session.query(Issue).filter(Issue.key == key).one_or_none()
            if existing:
                existing.summary = summary
                existing.status = status
                existing.assignee = assignee
                existing.labels = labels
                existing.epic = epic
                existing.raw = it
            else:
                session.add(Issue(key=key, summary=summary, status=status, assignee=assignee, labels=labels, epic=epic, raw=it))
        session.commit()
        # pagination
        if data.get('isLast'):
            break
        start_at = data.get('startAt', 0) + data.get('maxResults', len(issues))
    session.close()


def extract_confluence_page(page_id: str):
    client = ConfluenceClient()
    data = client.get_page(page_id)
    session = get_session()
    existing = session.query(ConfluencePage).filter(ConfluencePage.page_id == str(page_id)).one_or_none()
    if existing:
        existing.title = data.get('title')
        existing.url = data.get('_links', {}).get('base')
        existing.raw = data
    else:
        session.add(ConfluencePage(page_id=str(page_id), title=data.get('title'), url=data.get('_links', {}).get('base'), raw=data))
    session.commit()
    session.close()


if __name__ == '__main__':
    logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
    init_db()
    extract_issues()
