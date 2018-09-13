import pandas as pd
import xml.etree.cElementTree as ET


def get_namemap():
    xml_data1 = """<?xml version="1.0"?> and the rest of your XML here"""
    tree = ET.parse('name_map.xml')  # or `ET.parse(<filename>)`
    name = {}
    for elem in tree.findall('userData'):
        name[elem.find('userName').text] = elem.find('displayName').text

    return name


name = get_namemap()

dname = []
pdata = pd.read_csv('cr.csv')

for n in pdata['author']:
    if n in name:
        dname.append(name[n])
    else:
        dname.append(n)

pdata['displayName'] = dname

# for dev in pdata["displayName"].unique():
#
#     reviews = set()
#     for review in pdata[pdata.displayName == dev]['reviews']:
#         if (type(review) == type('')):
#             reviews.add(review)
#
#     if (len(reviews) != 0):
#         print(dev, '\t\t\t' + str(len(reviews)), str(reviews))
#     else:
#         print(dev, '\t\t\t' + str(len(reviews)))

print(
    pdata[pdata['displayName']=='Jacky Zhang']['reviews']
)
