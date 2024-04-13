import requests

with open("cookies.txt") as f:
    cookies = [line.strip() for line in f]
validCookies = []
for cookie in cookies:
    try:
        s = requests.session()
        s.cookies[".ROBLOSECURITY"] = cookie
        s.headers['X-CSRF-TOKEN'] = s.post("https://auth.roblox.com/v2/login").headers['X-CSRF-TOKEN']
        check = s.get("https://users.roblox.com/v1/users/authenticated")
        if check.status_code == 200:
            print(f"[✔] adding valid cookie ({len(cookies)-cookies.index(cookie)} left)")
            validCookies.append(cookie)
        elif check.status_code != 200:
            print(f"[×] removing invalid cookie ({len(cookies)-cookies.index(cookie)} left)")
    except:
         print(f"[×] removing invalid cookie ({len(cookies)-cookies.index(cookie)} left)")

with open("cookies.txt", "w") as f:
    for cookie in validCookies:
        f.write("%s\n" % cookie)