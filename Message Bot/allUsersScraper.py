import requests
import os
import random
import json
import sys
import concurrent.futures

while True:
    os.system('clear')

    with open('cookies.txt', 'r') as f:
        cookies = [line.strip() for line in f]

    groupIDs = []
    print(f"[ BOT ] Loaded {len(cookies)} cookies.")

    with open("last_user_id.txt", "r") as f:
        userID = int(f.read().strip())
    foundAccounts = []
    scrapedUsers = []
    totalChecks = 0
    totalUsers = 100  # Set the number of users you want to check, you can adjust this value as needed

    def save_user_id(user_id):
        with open("last_user_id.txt", "w") as f:
            f.write(str(user_id))

    def check_user_messages(user_id):
        global foundAccounts, scrapedUsers, totalChecks

        try:
            s = requests.session()
            s.cookies[".ROBLOSECURITY"] = random.choice(cookies)
            s.headers['X-CSRF-TOKEN'] = s.post("https://auth.roblox.com/v2/login").headers['X-CSRF-TOKEN']
            auth = True
        except:
            print("error")

        check = s.get(f"https://privatemessages.roblox.com/v1/messages/{user_id}/can-message")

        if check.status_code == 200:
            if check.json() == {'canMessage': True}:
                foundAccounts.append(user_id)
                scrapedUsers.append(user_id)
                print(f"[ OK ] Found messageable user: {user_id}")
            elif check.json() == {'canMessage': False}:
                print(f"[ ER ] Not messagable: {user_id}")

        totalChecks += 1
        if user_id % 1000 == 0:
            try:
                save_user_id(user_id)
                with open(f"allmemberslist.json", "r") as infile:
                    existing_list = json.load(infile)
                combined_list = existing_list + foundAccounts
                combined_list = list(set(combined_list))
                with open(f"allmemberslist.json", "w") as outfile:
                    json.dump(combined_list, outfile)
            except:
                print("error")
            

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        while totalChecks < totalUsers:
            executor.submit(check_user_messages, userID)
            userID += 1

    try:
        with open(f"allmemberslist.json", "r") as infile:
            existing_list = json.load(infile)
        combined_list = existing_list + foundAccounts
        combined_list = list(set(combined_list))
        with open(f"allmemberslist.json", "w") as outfile:
            json.dump(combined_list, outfile)
    except:
        print("error")

sys.exit(0)
