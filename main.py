from jira_connection_base import JiraConnection
from Story import Story
from Task import Task
import json

import matplotlib as mpl
mpl.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import time
from configuration import userpsw, DEBUG

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
            setUserAndPass(userpsw).\
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
            setUserAndPass(userpsw).\
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

def story_crunch(stories):

    pdata=pd.DataFrame.from_records(stories,columns=['key','Story Developer','Story Point','status','Bug'])

    data=pd.DataFrame(pdata.groupby('Story Developer')['Story Point'].sum()).\
        join(pdata.groupby('Story Developer')['Bug'].sum()).\
        sort_values(by=['Story Point'])

    print(data)

    return data

def task_crunch(tasks):

    pdata = pd.DataFrame.from_records(
        list(map(lambda x:x[0:4]+[(x[-1]-x[-2])/3600], tasks)),
        columns=['Key','Assignee', 'Issuetype', 'Status', 'Remaining_hrs']
    )

    data=pdata.groupby('Assignee').sum().\
        sort_values(by=['Remaining_hrs'])

    print(data)

    return data

##########################


def report():


    if (DEBUG):
        print("Test story...")
        stories = test_storyfile_json()
        story_data=story_crunch(stories)
        ax=story_data.plot(kind='barh')
        for p in ax.patches:
            ax.annotate(str(p.get_width()), (p.get_width() * 1.005, p.get_y() * 1.005))

        plt.subplots_adjust(left=0.2)
        plt.show()

        print("Test task...")
        tasks = test_taskfile_json()
        task_data=task_crunch(tasks)
        task_data.plot.pie(subplots=True, y=['Remaining_hrs'], figsize=(6, 6), radius=0.7)

        plt.legend(loc="lower right", fontsize=10,
           bbox_transform=plt.gcf().transFigure)
        plt.subplots_adjust(left=0.0, bottom=0.1, right=0.85)
        plt.show()

    if (not DEBUG):
        rpt=open("report.html","w+")
        rpt.write('<h3>'+time.strftime("%c")+'</h3>')
        for i in range(1,9):
            CNx="CN"+str(i)

            rpt.write('<hr/>')
            rpt.write('<h2>Team: %s</h2>'%CNx)

            # render story
            stories = json_story_post(CNx)
            story_data= story_crunch(stories)

            ax=story_data.plot(kind='barh')
            for p in ax.patches:
                ax.annotate(str(p.get_width()), (p.get_width() * 1.01, p.get_y() * 1.005))

            plt.subplots_adjust(left=0.2)
            plt.savefig('pic/SP_'+CNx+'.png')
            rpt.write('<img src="/pic/SP_'+CNx+'.png'+'" />')

            rpt.write('<span style="display: inline-block">%s</span>'%
                      story_data.to_html())
            rpt.flush()

            # render task
            tasks = json_task_post(CNx)
            task_data=task_crunch(tasks)
            # task_data.plot.pie(y=['Remaining_hrs'], subplots=True, figsize=(3, 3), radius=0.5)
            # plt.legend(loc='lower right')
            # plt.subplots_adjust(left=0.0)
            # plt.savefig('pic/hours_'+CNx+'.png')
            # rpt.write('<img src="/pic/hours_'+CNx+'.png'+'" />')

            rpt.write('<span style="display: inline-block">%s</span>'%
                      task_data.to_html())

            rpt.flush()
            plt.close()
            plt.close("all")

        rpt.close()




if __name__ == '__main__':
    while True:
        print('Start running report ...')
        report()
        print('Start sleeping 15 minutes ...')
        time.sleep(60*15)

