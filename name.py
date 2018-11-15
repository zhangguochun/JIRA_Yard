from jira_connection_base import JiraConnection
import configuration, json

path='/rest/api/2/user/assignable/search?project=AWO&maxResults=1000'

jira_connection = JiraConnection()
jira_connection.\
            setUserAndPass(configuration.userpsw).\
            setHeader()

def get_json():
    return jira_connection.requestInGet(path)

def get_json_testfile():
    return open('user.json')


def get_name(key):
    names={}
    j=json.load(get_json_testfile())
    for user_json in j:
        names[user_json['key']]=user_json['displayName']

    try:
        name = names[key]
        return name
    except KeyError:
        return key

if __name__ == '__main__':
    print(get_name('ban'))

