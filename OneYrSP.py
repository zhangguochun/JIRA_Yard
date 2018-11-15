from jira_connection_base import JiraConnection
import configuration
import pandas as pd
import glob

jira_connection = JiraConnection()
jira_connection. \
    setUserAndPass(configuration.userpsw). \
    setHeader()

url = '''/sr/jira.issueviews:searchrequest-csv-current-fields/temp/SearchRequest.csv?jqlQuery=project+%3D+awo+AND+%22AWO+Scrum+Team%22+in+%28AWO-CN1%2C+AWO-CN2%2C+AWO-CN3%2C+AWO-CN4%2C+AWO-CN5%2C+AWO-CN6%2C+AWO-CN7%2C+AWO-CN8%2C+AWO-NA1%2C+AWO-NA2%2C+AWO-NA3%29+AND+issuetype+%3D+%22Requirement%2FUser+Story%22+AND+AWO-Committed+%3D+%22Will+Finish%22+AND+Sprint+%3D+%22AWO+Sprint+'''

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


def get_csv(sprint, csv_name):
    raw = jira_connection.requestInGet(url + str(sprint) + "%22")
    f = open(csv_name, 'w')
    f.write(raw)
    f.flush()
    f.close()


def crunch(sprint):
    csv = 'S' + str(sprint) + '.csv'
    s = pd.read_csv(csv)
    pdata = s[~s['Custom field (Story Developers)'].isnull() & s['Custom field (Story Developers).1'].isnull()]
    pdata.to_csv(csv)

def add_columns(csv_name, sprint, team):
    team_bug_data= pd.read_csv(csv_name)
    team_bug_data['sprint']=sprint
    team_bug_data['team']=team
    team_bug_data.to_csv(csv_name)

if __name__ == '__main__':
    for sprint in range(56, 75):  # Sprint 56, Sep 05, 2017
        get_csv(sprint, csv_name='S' + str(sprint) + '.csv')
        crunch(sprint)

        # in_Sprint bug
        for team in teams:
            bug_url.format(team=team, sprint=str(sprint))
            csv_name='S' + str(sprint)+team+ '_bug.csv'
            get_csv(sprint, csv_name=csv_name)
            add_columns(csv_name=csv_name, sprint='AWO Sprint '+str(sprint), team='AWO-'+team)

    big_frame = pd.concat([pd.read_csv(f) for f in glob.glob("S*.csv")], ignore_index=True)
    big_frame.to_csv('A1.csv')

    # SP per team
    per_team = big_frame.groupby(['Sprint', 'Custom field (AWO Scrum Team)'], as_index=False)[
        'Custom field (Story Points)'].sum().to_csv("rpt_per_team.csv")
    # report = big_frame.groupby(['Sprint', 'Custom field (AWO Scrum Team)'], as_index=False)[
    #     'Custom field (Story Points)'].mean().round(1).rename(
    #     columns={'Custom field (AWO Scrum Team)': 'Scrum Team', 'Custom field (Story Points)': 'SP per person'})
    # report.to_csv('report.csv')

    # bug
    all_bug = pd.concat([pd.read_csv(f) for f in glob.glob("S*_bug.csv")], ignore_index=True)
    all_bug.to_csv('A1_bug.csv')
    all_bug.groupby
