import sys
from pathlib import Path

import streamlit as st
import pandas as pd

# Ensure project root is on sys.path so `import src` works when Streamlit
# is started from a different working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Build a local engine pointing at the project `data.db` so the app works
# regardless of how Streamlit sets up module paths.
default_db = PROJECT_ROOT / 'data.db'
DB_URL = f'sqlite:///{default_db}'
from sqlalchemy import create_engine
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})


@st.cache_data
def load_issues():
    df = pd.read_sql_table('issues', con=engine)
    return df


def main():
    st.title('Jira & Confluence Dashboard')
    st.markdown('Stories by status and assignee')
    df = load_issues()
    if df.empty:
        st.info('No issues found. Run the extractor first.')
        return
    # derive project from key prefix
    df['project'] = df['key'].str.split(pat='-', n=1).str[0]

    project = st.selectbox('Project', options=sorted(df['project'].unique()))
    df = df[df['project'] == project]

    status_sel = st.multiselect('Status', options=sorted(df['status'].dropna().unique()), default=list(df['status'].dropna().unique()))
    assignee_sel = st.multiselect('Assignee', options=sorted(df['assignee'].dropna().unique()), default=list(df['assignee'].dropna().unique()))

    if status_sel:
        df = df[df['status'].isin(status_sel)]
    if assignee_sel:
        df = df[df['assignee'].isin(assignee_sel)]

    st.subheader('Status distribution')
    status_counts = df.groupby('status').size().sort_values(ascending=False)
    st.bar_chart(status_counts)

    st.subheader('Top assignees')
    assignee_counts = df.groupby('assignee').size().sort_values(ascending=False).head(10)
    st.bar_chart(assignee_counts)

    st.subheader('Issues table')
    st.dataframe(df[['key', 'summary', 'status', 'assignee', 'labels', 'epic']])


if __name__ == '__main__':
    main()
