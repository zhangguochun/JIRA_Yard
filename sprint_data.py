from jira_connection_base import JiraConnection
import configuration
import pandas as pd

jira_connection = JiraConnection()
jira_connection. \
    setUserAndPass(configuration.userpsw). \
    setHeader()

story_url = '''/sr/jira.issueviews:searchrequest-csv-current-fields/temp/SearchRequest.csv?jqlQuery=project+%3D+awo+AND+%22AWO+Scrum+Team%22+in+%28AWO-CN1%2C+AWO-CN2%2C+AWO-CN3%2C+AWO-CN4%2C+AWO-CN5%2C+AWO-CN6%2C+AWO-CN7%2C+AWO-CN8%2C+AWO-NA1%2C+AWO-NA2%2C+AWO-NA3%29+AND+issuetype+%3D+%22Requirement%2FUser+Story%22+AND+AWO-Committed+%3D+%22Will+Finish%22+AND+Sprint+%3D+%22AWO+Sprint+'''
bug_url = '''/sr/jira.issueviews:searchrequest-csv-current-fields/temp/SearchRequest.csv?jqlQuery=project+%3D+awo+AND+issueFunction+in+subtasksOf%28%22%5C%22AWO+Scrum+Team%5C%22+%3D+AWO-{team}+and+issuetype+%3D+%5C%22Requirement%2FUser+Story%5C%22+%22%29+AND+issuetype+%3D+%22Bug+Sub-Task%22+AND+sprint+%3D+%22AWO+Sprint+{sprint}%22+and+cf%5B10081%5D+in+%28%22Coding+Error%22%2C+%22Coding+Missed+Implementation%22%29'''
teams = ["CN1",
         "CN2",
         "CN3",
         "CN4",
         "CN5",
         "CN6",
         "CN7",
         "CN8",
         "NA1",
         "NA2",
         "NA3"]

rpt=open('summary_report.html','w')

def get_data(url, csv_name):
    raw = jira_connection.requestInGet(url)
    f = open(csv_name, 'wb')
    f.write(raw)
    f.flush()
    f.close()
    try:
        data = pd.read_csv(csv_name)
        return data
    except pd.errors.EmptyDataError:
        return pd.DataFrame()

def sprint_data(sprint):


    sdata = get_data(story_url + sprint + "%22", "story.csv")
    sdata = pd.DataFrame(sdata.groupby(['Custom field (AWO Scrum Team)'])['Custom field (Story Points)'].sum())
    sdata.columns=['Total Story Point']
    sdata.index.names=['Scrum Team']

    # in_Sprint bug
    for team in teams:
        bug_num = len(get_data(bug_url.format(team=team, sprint=sprint), "bug.csv").index)
        sdata.loc['AWO-'+team, 'Bug Number'] = str(bug_num)
        sdata.loc['AWO-'+team, 'Bug Rate'] = str(round(bug_num/float(sdata.loc['AWO-'+team, 'Total Story Point']),3))

    rpt.write(sdata.to_html())
    rpt.flush()

    return sdata

if __name__ == '__main__':

    all_data=pd.DataFrame()
    for sprint in range(56, 75):
        rpt.write('<h3>Sprint #'+str(sprint)+'</h3>')
        all_data= all_data.append(sprint_data(str(sprint)))

    all_data.to_csv('all_data.csv')

    rpt.close()
