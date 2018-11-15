from jira_connection_base import JiraConnection
import configuration
import pandas as pd
import io, pkgutil
import sys

jira_connection = JiraConnection()
jira_connection. \
    setUserAndPass(configuration.userpsw). \
    setHeader()

url = '''/sr/jira.issueviews:searchrequest-csv-current-fields/temp/SearchRequest.csv?jqlQuery=parent%3D{jirakey}'''

# environment settings:
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

def get_csv(url):

    raw = jira_connection.requestInGet(url)
    pdata = pd.read_csv(io.BytesIO(raw))

    # print(pdata.head(0))

    pdata['Σ Time Spent']=pdata['Σ Time Spent']/3600
    pdata['Σ Remaining Estimate']=pdata['Σ Remaining Estimate']/3600

    print(pdata[['Issue key', 'Custom field (Task Category)', 'Assignee', 'Σ Time Spent', 'Σ Remaining Estimate']])

    print(pdata.groupby(['Assignee'])['Σ Remaining Estimate'].sum())


if __name__ == '__main__':

    if (len(sys.argv)!=2):
        print("python look_inside.py [story jira number]")
        sys.exit(0)

    jirakey=sys.argv[1]
    jira_tasks_url= url.format(url,jirakey=jirakey)
    get_csv(url=jira_tasks_url)
