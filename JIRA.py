import json
from base64 import b64encode
from http.client import HTTPSConnection

#This sets up the https connection
c = HTTPSConnection("jira.aspiraconnect.com")
#we need to base 64 encode it
#and then decode it to acsii as python 3 stores it as a byte string
userAndPass = b64encode(b"gzhang:Pinwen@18").decode("ascii")
headers = { 'Authorization' : 'Basic %s' %  userAndPass, 'Content-Type': 'application/json' }
#then connect

# Body
body='''
{
	"jql": "filter=AWO-CN1-Sprint-Task",
	            "startAt": 0,
            "maxResults" : 500,
            "fields": [
                "key",
                "customfield_12866",
                "customfield_10242",
                "subtasks",
                "aggregatetimeoriginalestimate",
                "aggregateprogress",
                "customfield_12551"
            ]
}
'''

c.request('POST', '/rest/api/2/search', headers=headers, body=body)
#get the response back
print(headers)
res = c.getresponse()
# at this point you could check the status etc
# this gets the page text
data = res.read()

d=json.loads(data)

for issue_raw in d["issues"]:
    print(issue_raw["key"])

# objects = ijson.items(data, 'issues.fields.item')
#
# column=list(objects)
# print(column)
# cities = (o for o in objects if o['type'] == 'subtasks')
# for city in cities:
#     print(city)



