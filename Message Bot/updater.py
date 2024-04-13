import json, requests, random, sys

cookiemethed = 2

if cookiemethed == 1 :
    with open("cookies.txt") as f:
        cookies = ["".join(cookie.split(":")[2:]) for cookie in f.read().splitlines()]
elif cookiemethed == 2:
    with open('cookies.txt', 'r') as f:
        cookies = [line.strip() for line in f]
        
    
with open('proxys.txt', 'r') as f:
    proxys = [line.strip() for line in f]
for cookie in cookies:
    s = requests.session()
    s.cookies[".ROBLOSECURITY"] = cookie
    s.headers['X-CSRF-TOKEN'] = s.post("https://auth.roblox.com/v2/login").headers['X-CSRF-TOKEN']

    proxy = random.choice(proxys)
    proxies={
        "http": proxy,
        "https": proxy
                }
    change = s.post("https://accountsettings.roblox.com/v1/private-message-privacy", json={"privateMessagePrivacy": "All"})
    print(change.json())
    print("")
    print(cookie)
    print("")