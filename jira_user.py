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


c.request('GET', '/rest/api/2/user/assignable/search?project=AWO&maxResults=1000', headers=headers)
#get the response back

res = c.getresponse().read()
# at this point you could check the status etc
# this gets the page text

data = json.loads(res)

# for issue_raw in data:
#     print(issue_raw["key"],issue_raw["emailAddress"],issue_raw["displayName"],issue_raw["active"])

def user_dict():
    users={}
    for user in data:
        users[user["key"]]=user["displayName"]

    return users



