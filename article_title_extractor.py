# install packages
import requests
from bs4 import BeautifulSoup
import pandas as pd

dates = ['june','july','august','september']
starting_url = "http://www.espn.com/nfl/news/archive/_/month/{}/year/2018"

# create dataframe to return
df = pd.DataFrame(columns=['ID', 'Article Title', 'Link'])

id_num = 1
for date in dates:
    curr_url = starting_url.format(date)
    print(curr_url)
    
    # get webpage
    page = requests.get(curr_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    li_tags = soup.find_all("li")
    a_tags = soup.find_all("a")
    
    for a_tag in a_tags:
        if a_tag.parent.name != "li": #must be within li tag
            continue
        href = a_tag.get("href")
        title = a_tag.get("title")
        
        if href.find("insider") != -1: # ignore insider stories
            continue
        elif href.find("nfl") == -1: # must be in nfl
            continue
        elif href.find("http") == -1 or href.find("espn") == -1: # must have http link and from espn
            continue
        elif title is None:
            continue
        else:
            print(title)
            # add article info to dataframe
            curr_article = [id_num, title, href]
            df.loc[df.shape[0]] = curr_article

            id_num = id_num + 1

print('Number of article titles: ' + str(df.shape[0]))

# save to csv
df.to_csv("data/nfl_article_title_data.csv", index = False)


