import requests, os, random, json, sys
import concurrent.futures
os.system('clear')
def proxy():
  with open('spamProxies.txt', 'r') as f:
     return [line.strip() for line in f]


with open('cookies.txt', 'r') as f:
    cookies = [line.strip() for line in f]
groupIDs = []
print(f"[ BOT ] Loaded {len(proxy())} proxies.")
print(f"[ BOT ] Loaded {len(cookies)} cookies.")
inputExtra = input("[ CONFIG ] Enter Group ID to scrape from: ")
if inputExtra.isdigit():
    groupIDs.append(inputExtra)

if not inputExtra.isdigit():
    print("[ ERR ] Please enter a valid group ID.")
else:
    inputExtra = input("[ CONFIG ] Enter extra Group ID to scrape from (enter anything other than integer to finish): ")
    if inputExtra.isdigit():
        groupIDs.append(inputExtra)
    while inputExtra.isdigit():
        inputExtra = input("[ CONFIG ] Enter extra Group ID to scrape from (enter anything other than integer to finish): ")
        if not inputExtra == '':
            groupIDs.append(inputExtra)
print(groupIDs)
for groupID in groupIDs:
    groupID = int(groupID)
    print("[ SYSTEM ] Obtaining data, please wait...")
    getGroup = requests.get(f"https://groups.roblox.com/v1/groups/{groupID}").json()
    if "errors" in getGroup:
        print("[ ERR ] Group not found, please enter a valid group ID.")
    else:
        groupName = getGroup["name"]
        members = getGroup["memberCount"]
        if members > 1:
            print(f"[ OK ] Success! Group '{groupName}' has {members} members.")
        else:
            print("[ ERR ] Group members too low, please select another group.")
            sys.exit(0)
    print(f"[ PROC ] Starting process to obtain data | Name: {groupName}, Members: {members}")
    totalUsers = members
    totalChecks = 0
    scrapedUsers = []
    tempScrape100 = []
    users = []
    foundAccounts = []
    items = []
    getRoles = requests.get(f"https://groups.roblox.com/v1/groups/{groupID}/roles").json()["roles"]
    for role in getRoles:
        roleID = role["id"]
        memberCount = role["memberCount"]
        if memberCount >= 1:
            nextPageCursor = None
            while True:
                params = {"cursor": nextPageCursor, "limit": 100}
                scrape = True
                try:
                    getUsers = requests.get(f"https://groups.roblox.com/v1/groups/{groupID}/roles/{roleID}/users?cursor=&limit=100&sortOrder=Desc",params=params, timeout=3)
                except:
                    scrape = False
                if scrape == True:
                    if getUsers.status_code == 200:
                        getUsers = getUsers.json()
                        nextPageCursor = getUsers["nextPageCursor"]
                        if nextPageCursor == None:
                            print("[ BOT ] Finished Checking Role", roleID)
                            break
                        getUsers = getUsers["data"]
                        tempScrape100 = []
                        print("[ BOT ] Scraped Role Adding Users To List")
                        for user in getUsers:
                            tempScrape100.append(user["userId"])
                        if len(tempScrape100) >= 10:
                            accounts = tempScrape100
                            users = []

                            y = 0
                            while True:
                                items = []
                                x = 0
                                while x <= 10:
                                    items.append(accounts[y])
                                    y+=1
                                    x+=1
                                    if y == len(accounts)-1:
                                        users.append(items)
                                        break
                                if y == len(accounts)-1:
                                        break
                                users.append(items)
                            toUse = 0
                            foundAccounts = []
                            auth = False
                            while auth != True:
                                try:
                                    s = requests.session()
                                    s.cookies[".ROBLOSECURITY"] = random.choice(cookies)
                                    s.headers['X-CSRF-TOKEN'] = s.post("https://auth.roblox.com/v2/login").headers['X-CSRF-TOKEN']
                                    auth = True
                                except:
                                    pass
                            def someFunction(i):
                                global totalChecks
                                global toUse
                                global foundAccounts
                                try:
                                  accounts2check = users[toUse]
                                except:
                                    accounts2check = None
                                toUse+=1
                                for userID in accounts2check:
                                    totalChecks+=1
                                    try:
                                        check = s.get(f"https://privatemessages.roblox.com/v1/messages/{userID}/can-message", timeout=3)
                                        print(check.json(), userID)
                                        if check.status_code == 200:
                                            
                                            if check.json() == {'canMessage': True}:
                                                foundAccounts.append(userID)
                                                scrapedUsers.append(userID)
                                                #print(f"[ BOT ] Found a user to message {userID}  {totalChecks}/{totalUsers}, Messageable users: {len(scrapedUsers)}")
                                                print(f"[ OK ] Found messageable user: {userID}\n[ STATS ] {totalChecks}/{totalUsers}\n[ DATABASE ] {len(scrapedUsers)} users.")
                                            elif check.json() == {'canMessage': False}:
                                                print(f"[ ERR ] {userID} has messages off.")
                                        else:
                                            print(f"[ FATAL ] Unable to check for messages on {userID}, Error code {check.status_code}, {check.json()}")
                                    except:
                                        print("[ FATAL ] Couldn't parse html object.")
                                print("[ PROC ] Thread has finished")
                            threads = len(users)
                            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                                futures = [executor.submit(someFunction, i) for i in range(threads)]
                            tokens = [future.result() for future in futures]
                            if not len(foundAccounts) == 0:
                                try:
                                    with open(f"members.json", "r") as infile:
                                        existing_list = json.load(infile)
                                    combined_list = existing_list + foundAccounts
                                    combined_list = list(set(combined_list))
                                    with open(f"members.json", "w") as outfile:
                                        json.dump(combined_list, outfile)
                                    print("done")
                                except:
                                    print("error")
                            else:
                                print("no new users. Wont write to file.")
                        else:
                            print("[ ERR ] Skipping role, Under 10 members in request")
                    else:
                        print("[ FATAL ] Error scraping members", getUsers.status_code)

    print("[ OK ] Finished Scraping Group.")
    try:
        with open(f"members.json", "r") as infile:
            existing_list = json.load(infile)
        combined_list = existing_list + foundAccounts
        combined_list = list(set(combined_list))
        with open(f"members.json", "w") as outfile:
            json.dump(combined_list, outfile)
    except:
        print("error")
        
sys.exit(0)
