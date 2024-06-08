import json
import urllib.request
import http.client
import argparse
import os
import re

os.system('cls')

config = {
    # place path to your log file dir 
    "path_to_log": "O:\Epic Games\WutheringWavesj3oFh\Wuthering Waves Game\Client\Saved\Logs"    
}

clear = lambda: os.system('cls')
clear()

convenceURL = ""

parser = argparse.ArgumentParser()
parser.add_argument(
    '-nsts',
    '--no_skip_three_star',
    type=int,
    default=0,
    help='no skip three star pulls (default: 1)'
)
parser.add_argument(
    '-a',
    '--auto_link',
    type=bool,
    default=False,
    help='auto link'
)

args = parser.parse_args()

clear()
if not args.auto_link:
    convenceURL = input("Paste here URl from Client/Logs/Client.txt: ")
else:
    
    with open(f'{config['path_to_log']}\Client.log', 'r', encoding='utf-8') as f:
        for line in f:
            try:
                # print(line)
                convenceURL = re.search("(?P<url>https?://[^\s]+)", line).group("url").split("\",\"")[0]
                print(convenceURL)
            except AttributeError:
                pass
clear()


NameBanner = {
    "1": "Featured Resonator",
    "2": "Featured Weapon",
    "3": "Standard Resonator",
    "4": "Standard Weapon",
    "5": "Beginner Convene",
    "6": "Beginner Convene Choice",
    "7": "Other Banner",
}

print("Banner Name\n\n 1 - Featured Resonator\n 2 - Featured Weapon\n 3 - Standard Resonator\n 4 - Standard Weapon\n 5 - Beginner Convene\n 6 - Beginner Convene Choice\n 7 - Other Banner\n")

    
bannerID = input("[1-7]: ")

clear()

print(NameBanner[bannerID] + "\n")

query = list(map(lambda values: values.split("=")[1], convenceURL.split("?")[1].split("&")))
query.remove('global')
# print(query)
conn = http.client.HTTPSConnection("gmserver-api.aki-game2.net")

payvload= json.dumps({
    "cardPoolId": query[6],
    "cardPoolType": int(bannerID),
    "languageCode": query[2],
    "playerId": int(query[1]),
    "recordId": query[5],
    "serverId": query[0],
})

conn.request("POST", "/gacha/record/query", payvload, headers={"Content-Type": "application/json; charset=utf-8"})

res = conn.getresponse()
data = json.loads(res.read().decode("utf-8"))

# print(json.dumps(data,indent=4))

def out_blue(text):
    return "\033[34m{}\033[0m".format(text)
def out_purple(text):
    return "\033[35m{}\033[0m".format(text)
def out_yellow(text):
    return "\033[33m{}\033[0m".format(text)
def out_red(text):
    return "\033[31m{}\033[0m".format(text)
def out_green(text):
    return "\033[32m{}\033[0m".format(text)



pulls = list(data['data'])
utilitydata = {
    "five_star": 0,
    "five_star_pull": 0,
    "last_five_star": 0,
    "four_star": 0,
    "four_star_pull": 0,
    "last_four_star": 0,
}

for i, item in enumerate(reversed(pulls)):
    itemLevel = item['qualityLevel']
    
    colored_four_star = utilitydata['last_four_star']
    colored_five_star = utilitydata['last_five_star']
    
    if utilitydata['last_four_star'] <= 4:
        colored_four_star = out_green(utilitydata['last_four_star'])
    elif utilitydata['last_four_star'] <= 7:
        colored_four_star = out_yellow(utilitydata['last_four_star'])
    else: 
        colored_four_star = out_red(utilitydata['last_four_star'])
        
    if utilitydata['last_five_star'] <= 48:
        colored_five_star = out_green(utilitydata['last_five_star'])
    elif utilitydata['last_five_star'] <= 64:
        colored_five_star = out_yellow(utilitydata['last_five_star'])
    else: 
        colored_five_star = out_red(utilitydata['last_five_star'])
    match itemLevel:
        case 3:
            if args.no_skip_three_star:
                print(out_blue(f"№{i+1}\t{item['time']}\t{1}\t{out_blue(item['name'])}"))
        case 4:
            print(out_purple(f"№{i+1}\t{item['time']}\t{colored_four_star}\t{out_purple(item['name'])}"))
        case 5:
            print(out_yellow(f"№{i+1}\t{item['time']}\t{colored_five_star}\t{out_yellow(item['name'])}"))
            
    if itemLevel != 4:
        utilitydata['last_four_star']+=1
    else:
        utilitydata['four_star']+=1
        utilitydata['four_star_pull']+=utilitydata['last_four_star']
        utilitydata['last_four_star'] = 0
    if itemLevel != 5:
        utilitydata['last_five_star']+=1
    else:
        utilitydata['five_star'] += 1
        utilitydata['five_star_pull'] += utilitydata['last_five_star']
        utilitydata['last_five_star'] = 0
        
print(f"\nTotal pulls - {len(pulls)}\nAsterit - {len(pulls)*160}\n")
print(f"Pity 5* - {utilitydata['last_five_star']}")
print(f"Pity 4* - {utilitydata['last_four_star']}\n")
if utilitydata['five_star'] > 0:
    print(f"Average 5* Pity - {int(utilitydata['five_star_pull']/utilitydata['five_star'])}")
if utilitydata['four_star'] > 0:
    print(f"Average 4* Pity - {int(utilitydata['four_star_pull']/utilitydata['four_star'])}")
    