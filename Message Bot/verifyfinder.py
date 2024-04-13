import requests, json

with open('cookies.txt', 'r') as f:
    cookies = [line.strip() for line in f]
final = []
for cookie in cookies:
    s = requests.session()
    s.cookies[".ROBLOSECURITY"] = cookie
    s.headers['X-CSRF-TOKEN'] = s.post("https://auth.roblox.com/v2/login", timeout=2).headers['X-CSRF-TOKEN']
    send = s.get("https://accountsettings.roblox.com/v1/email")
    data = send.json()
    try:
        if str(data["verified"]) == "True":
            print("Verified")
            final.append(cookie)
        else:
            print("Not Verified")
    except:
        print("Invalid cookie")
with open("cookies.txt", "w") as f:
    for cookie in final:
        f.write("%s\n" % cookie)