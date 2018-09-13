import feedparser
from datetime import datetime
import pandas as pd

# url = 'http://awotordevsvn01.dev.activenetwork.com/cru/rssReviewFilter?filter=allReviews&project=CDEV&FEAUTH='
filename = 'cr_css'
startDate = datetime.strptime('2018-06-18', '%Y-%m-%d').date()
endDate = datetime.now().date()
fileName = 'CR_Monthly_Report_%s_%s.xlsx' % (startDate, endDate)
writer = pd.ExcelWriter(fileName)

cr_list = []
for entry in feedparser.parse(filename).entries:

    pubDate = datetime.strptime(entry['published'], '%a, %d %b %Y %H:%M:%S %z').date()

    if (pubDate > startDate):
        cr_list.append([entry['author'], pubDate, entry['link']])

CR = pd.DataFrame(cr_list, columns=['Developer', 'Create Date', 'URL'])

CR.to_excel(writer, sheet_name='Detail')
CR_summary = CR.groupby('Developer', as_index=False)['URL'].count()
pd.DataFrame(CR_summary.to_excel(writer, sheet_name='Summary'))

#########
names = pd.read_csv('dev_names.txt', names=['Developer'])

pd.DataFrame(names.merge(pd.DataFrame(CR_summary),
                         how='left', on=['Developer']).to_excel(writer, sheet_name='Need CR'))

writer.close()

# http://awotordevsvn01.dev.activenetwork.com/rest-service/reviews-v1/filter?author=ban
#
# https://docs.atlassian.com/fisheye-crucible/4.5.1/wadl/crucible.html#rest-service:reviews-v1:filter
