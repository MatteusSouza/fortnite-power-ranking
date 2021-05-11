'''
SIMPLIFIED VERSION || easy to understand
Original page from where I got the data:
https://fortnitetracker.com/events/powerrankings?platform=global&region=global

'''

import requests
from bs4 import BeautifulSoup
import pandas as pd

get_top_n_players = 6
platform = 'global' # platforms: pc, console, mobile || global is default
region = 'global'  # regions: NAE, NAW, EU, OCE, BR, ASIA, ME || global is default


url = (
    'https://fortnitetracker.com/events/powerrankings?platform='
     + platform + '&region=' + region)

response = requests.get(url)
content = response.content
content_html = BeautifulSoup(content, 'html.parser')
table = content_html.find(name='table')
# print(table)

df_raw = pd.read_html(str(table))[0].head(get_top_n_players)
df = df_raw.drop(columns=['Unnamed: 5']) #delete the columm
# print(df)

'''
The "Points" column contains two pieces of 
information that must be separated into two separate columns.
'''

points = df.Points.str.split(expand=True,) #split the columns
points.columns = ['Points', 'Top' ,'Percentile' ] #rename the titles columns
points['Top'] = points['Top'].map({'Top':'Top '}, na_action=None) #Rename the "Top" value with space at the end.
points["Percentile"] = points["Top"] + points["Percentile"] #merge the columns
points = points.drop(columns=['Top'])
# print(points)

df = df.drop(columns=['Points'])
df.insert(2, "Points", points['Points'], allow_duplicates=False)
df.insert(3, "Percentile", points['Percentile'], allow_duplicates=False)
# print(df)

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

if __name__  == '__main__':
    space = "\n===============\n"

    print(df)

    print(space,'to_dict()',space)
    print(df.to_dict())

    print(space,'to_dict(\'index\')',space)
    print(df.to_dict('index'))

    print(space,'to_json(orient="index")',space)
    print(df.to_json(orient="index",indent=2, force_ascii=False))

    #create a json file
    # df.to_json('power_ranking.json', orient="index",indent=2, force_ascii=False)

