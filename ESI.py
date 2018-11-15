from jira_connection_base import JiraConnection
import configuration
import pandas as pd
import io, pkgutil
import sys
from itertools import groupby
import name

jira_connection = JiraConnection()
jira_connection. \
    setUserAndPass(configuration.userpsw). \
    setHeader()

esi_url = '''/sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv?jqlQuery=Project+%3D+%22AWO+Product+Development%22+AND+type+%3D+%22Escalated+Support+Issue%22+AND+createdDate+%3E+2018-01-01'''
bug_url = '''/sr/jira.issueviews:searchrequest-csv-all-fields/temp/SearchRequest.csv?jqlQuery=Project+%3D+%22AWO+Product+Development%22+AND+type+%3D+Bug+AND+status+%3D+closed+AND+createdDate+%3E+2018-11-01'''

# environment settings:
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

def download_csv_file(issuetype, url):
    raw = jira_connection.requestInGet(url)
    f=open(issuetype + '.csv', 'wb')
    f.write(raw)
    f.close()

def count_on_name(logs):
    data=[]
    for log in logs:
        if (type(log) is not float): # is not NaN
            data.append(log.split(';')[-2:])

    return data

def run_report(issuetype, url):
    download_csv_file(issuetype=issuetype, url=url)

    pdata=pd.read_csv(issuetype + '.csv', dtype='unicode')
    efforts=[]


    for col in pdata.filter(regex='Log').itertuples():
        for row in col:
            if (type(row) is not float and type(row) is not int): # is not NaN
                efforts.append(row.split(';')[-2:])

    peffort=pd.DataFrame(efforts, columns=['Name','Hr'])
    peffort['Hr']=pd.to_numeric(peffort['Hr'])/3600

    result= peffort.groupby('Name', as_index=False).sum()
    result['Name']=result['Name'].apply(lambda x: name.get_name(x))

    result.to_excel(issuetype + '_report.xlsx')

if __name__ == '__main__':
    # run_report('ESI', esi_url)
    run_report(issuetype='BUG', url=bug_url)
