from encodings import utf_8
import re
from unittest import result 

import requests
def unshorten(url):
    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True)
    return resp.url
 
def scrapeData(data):
    restring = r"<a\s+(?:[^>]*?\s+)?href=[\"'](https://.*?/track/click.*?)[\"']"
    resocial = r"instagram|twitter|linkedin|unsubscribe|youtube|profile|facebook|soundcloud|spotify"
    # with open(filename,'r') as f:
    #     data = f.read()
    result = re.findall(restring,data)
    all_links = []
    for i in result:
        temp = unshorten(i)
        if re.search(resocial,temp):
            pass
        else:
            all_links.append(temp)
    # for i in all_links:
    #     print(i)
    return all_links
    
    
