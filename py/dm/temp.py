import re
import sys
import json
from concurrent.futures import ThreadPoolExecutor
import urllib.request
def get_card(name):
    url = r"http://www.wizards.com/duelmasters/dm_autocard.asp?name=" + name;
#    print(url)
    source = urllib.request.urlopen(url).read().decode()
#    print (source)
    pats = {"name":"<b>Name:</b>(.+?)<br/>",
    "cost":"<b>Cost:</b>(.+?)<br/>",
    "race":"<b>Race:</b>(.+?)<br/>",
    "civilization":"<b>Civilization:</b>(.+?)<br/>",
    "type":"<b>Type:</b>(.+?)<br/>",
    "rules_text":"<b>Rules Text:</b><br/>(.+?)<br/>",
    "flavor_text":"<b>Flavor Text:</b><br/>(.+?)<br/>",
    "mana_number":"<b>Mana Number:</b>(.+?)<br/>",
    "artist":"<b>Artist:</b> (.+?)<br/>",
    "power":"<b>Power:</b>(.+?)<br/>",
    "rarity":"<b>Rarity:</b> (.+?)<br/>",
    "collector_number":"><b>Collector Number:</b>(.+?)<br/>",
    "set":"<b>Set:</b>(.+?)<br/>",
    "img_name":name+".jpg"
    }
    found = {}
    for key, pat in pats.items():
        res = re.findall(pat, source)
        if len(res) > 0: found[key] = res[0].strip()
    #imgurl = "http://www.wizards.com/global/images/duelmasters/general/%s.jpg" % name
    #print(imgurl)
    #with open("images/"+name+".jpg", "wb") as f:
    #    f.write(urllib.request.urlopen(imgurl).read())
    return found
pat = r"'/duelmasters/dm_autocard\.asp\?name=(.+?)'"
d = set()
with open("source") as f:
    for line in f:
        res = re.findall(pat, line)
        if len(res) > 0: d.add(res[0])
with ThreadPoolExecutor(max_workers=50) as executor:
    cross = {}
    fin_res = {"cards":[]}
    for i in d:
        cross[executor.submit(get_card, i)] = i
    for i in cross:
        try:
            fin_res["cards"].append(i.result())
        except Exception:
            print(sys.stderr.write(cross[i]+"\n"))
    print(json.dumps(fin_res))
