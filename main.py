from jira_connection_base import JiraConnection
from Story import Story
from Task import Task
import json
import pandas as pd
import matplotlib.pyplot as plt
import time

DEBUG=True

def json_task_post(scrumteam):

    body='''
    {
	"jql": "filter=AWO-%s-Sprint-Task",
	            "startAt": 0,
            "maxResults" : 2000,
            "fields": [
            	"assignee",
            	"issuetype",
            	"status",
                "aggregateprogress"
            ]
    }
    '''%scrumteam

    jira_connection = JiraConnection()

    jira_connection.\
            setUserAndPass("gzhang:Pinwen@18").\
            setHeader().\
            setBody(body)

    x=jira_connection.sendRequest()

    task= Task(json.loads(x.decode()))

    return task.get_task()

def json_story_post(scrumteam):
        # Body
    body='''
    {
        "jql": "filter=AWO-%s-Sprint-Story",
                    "startAt": 0,
                "maxResults" : 1000
    }
    '''%scrumteam

    jira_connection = JiraConnection()

    jira_connection.\
            setUserAndPass("user:psw").\
            setHeader().\
            setBody(body)

    x=jira_connection.sendRequest()

    story = Story(json.loads(x.decode()))

    return story.get_story()

def test_storyfile_json():
    jfile=open("jira_story.json")

    story = Story(json.loads(jfile.read()))

    return story.get_story()

def test_taskfile_json():
    jfile=open("jira_task.json")
    tasks = Task(json.loads(jfile.read()))

    return tasks.get_task()

def story_crunch(scrumteam, stories):

    pdata=pd.DataFrame.from_records(stories,columns=['key','Story Developer','Story Point','status','Bug'])

    data=pd.DataFrame(pdata.groupby('Story Developer')['Story Point'].sum()).\
        join(pdata.groupby('Story Developer')['Bug'].sum())

    print(data)
    ax=data.plot(kind='barh')
    for p in ax.patches:
        ax.annotate(str(p.get_width()), (p.get_width() * 1.005, p.get_y() * 1.005))

    plt.savefig(scrumteam+'.png')

def task_crunch(scrumteam, tasks):

    pdata = pd.DataFrame.from_records(
        list(map(lambda x:x[0:4]+[(x[-1]-x[-2])/3600], tasks)),
        columns=['Key','Assignee', 'Issuetype', 'Status', 'Remaining_hrs']
    )

    data=pdata.groupby('Assignee').sum()
    print(data)

##########################
if __name__ == '__main__':

    DEBUG=False

    if (DEBUG):
        print("Test story...")
        stories = test_storyfile_json()
        story_crunch('CN_test', stories)

        print("Test task...")
        tasks = test_taskfile_json()
        task_crunch('CN_test', tasks)

    if (not DEBUG):
        print(time.strftime("%c"))
        for i in range(1,9):
            CNx="CN"+str(i)
            print("=== Team: %s ==="%CNx)
            stories = json_story_post(CNx)
            story_crunch(CNx, stories)

            tasks = json_task_post(CNx)
            task_crunch(CNx,tasks)



