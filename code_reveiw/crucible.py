import feedparser
from datetime import datetime
import pandas as pd

url='file:///Users/gavinzhang/PycharmProjects/JIRA_Yard/code_reveiw/rssReviewFilter.xml'
startDate = datetime.strptime('2018-08-11', '%Y-%m-%d').date()
endDate = datetime.now().date()
fileName = 'CR_Monthly_Report_%s_%s.xlsx' % (startDate, endDate)
writer = pd.ExcelWriter(fileName)

cr_list = []
for entry in feedparser.parse(url).entries:

    pubDate = datetime.strptime(entry['published'], '%a, %d %b %Y %H:%M:%S %z').date()

    if (pubDate > startDate):
        cr_list.append([entry['author'], pubDate, entry['link']])

CR = pd.DataFrame(cr_list, columns=['Developer', 'Create Date', 'URL'])

CR.to_excel(writer, sheet_name='Detail')
pd.DataFrame(CR.groupby('Developer')['URL'].count()). \
    to_excel(writer, sheet_name='Summary')

writer.close()



# http://awotordevsvn01.dev.activenetwork.com/rest-service/reviews-v1/filter?author=ban
#
# https://docs.atlassian.com/fisheye-crucible/4.5.1/wadl/crucible.html#rest-service:reviews-v1:filter
