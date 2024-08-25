import discord, json, re, requests, random, time, concurrent.futures, threading, math
from discord.ext import commands

with open('cookies.txt', 'r') as f:
    cookies = [line.strip() for line in f]

with open("config.json") as jsonfile:
    config = json.load(jsonfile)
    token = config["botToken"]
    messageTop = config["message"]
    messageDescription = config["messageDescription"]
    num_threads = config["threads"]
    autoThreads = config["autoThreads"]
    groupID = config["YourGroupID"]
with open('proxys.txt', 'r') as f:
    proxys = [line.strip() for line in f]

wait_event = threading.Event()
errors = 0
def send(idListNum, num, threadCount):
    global messagesSent
    global every1000
    global errors
    global cookiesCleaned
    global cookies
    global validCookies
    global numWait
    global sentUsers
    messagesSent = 0
    validCookies = []
    cookiesCleaned = True
    errors = 0
    every1000 = 0
    numWait = 0
    print("starting")
    for userID in idListNum:
        error = True
        while error == True:
            proxy = random.choice(proxys)
            proxies={
                "http": proxy,
                "https": proxy
                    }
            cookie = random.choice(cookies)
            s = requests.session()
            s.cookies[".ROBLOSECURITY"] = cookie
            try:
                s.headers['X-CSRF-TOKEN'] = s.post("https://auth.roblox.com/v2/login",proxies=proxies, timeout=2).headers['X-CSRF-TOKEN']
                sendTo = userID
                payload = {"subject":messageTop,"body":f"{messageDescription} {groupLink}","recipientid":sendTo}
                send = s.post("https://privatemessages.roblox.com/v1/messages/send",json=payload, proxies=proxies, timeout=2)
                if send.status_code == 200:
                    sentUsers.append(userID)
                    messagesSent+=1
                    every1000+=1
                    error = False
                    print(f"[✔] (THREAD {num+1}) Sending a message, total sent", messagesSent)
                else:
                    errors +=1
                    print(f"[X] (THREAD {num+1}) Unable to send message status code {send.status_code}")
                    time.sleep(num_threads+2)
                if amount==messagesSent:
                    with open("alreadymessaged.json", "r") as infile:
                        listNew = json.load(infile)
                    for x in sentUsers:
                        listNew.append(x)
                    sentUsers.clear()
                    with open("alreadymessaged.json", "w") as outfile:
                        json.dump(listNew, outfile)
                    print("[!] Finished sending messages")
                    return
                if every1000 == 1000:
                    print(f"[!] (THREAD {num+1}) Saving to file...")
                    #cookiesCleaned = False
                    every1000 = 0
                    with open("alreadymessaged.json", "r") as infile:
                        listNew = json.load(infile)
                    for x in sentUsers:
                        listNew.append(x)
                    sentUsers.clear()
                    with open("alreadymessaged.json", "w") as outfile:
                        json.dump(listNew, outfile)

                    # Currently disabled
                    if False:
                        wait_event.clear()
                        print("Waiting for other threads to complete...")
                        while threadCount-1 > numWait:
                            time.sleep(1)
                        time.sleep(2)
                        print("SCANNING COOKIES")

                        for cookie in cookies:
                            try:
                                s = requests.session()
                                s.cookies[".ROBLOSECURITY"] = cookie
                                s.headers['X-CSRF-TOKEN'] = s.post("https://auth.roblox.com/v2/login").headers['X-CSRF-TOKEN']
                                check = s.get("https://users.roblox.com/v1/users/authenticated")
                                if check.status_code == 200:
                                    print(f"[✔] Adding valid cookie ({len(cookies)-cookies.index(cookie)} left)")
                                    validCookies.append(cookie)
                                elif check.status_code != 200:
                                    print(f"[×] Removing invalid cookie ({len(cookies)-cookies.index(cookie)} left)")
                            except:
                                print(f"[×] Removing invalid cookie ({len(cookies)-cookies.index(cookie)} left)")

                        cookies.clear()
                        with open("cookies.txt", "w") as f:
                            for cookie in validCookies:
                                f.write("%s\n" % cookie)
                                cookies.append(cookie)
                        cookies = [*set(cookies)]
                        wait_event.set()
                        cookiesCleaned = True
                #if cookiesCleaned == False:
                    #numWait += 1
                    #while cookiesCleaned == False:
                        #wait_event.wait()
            except Exception as error:
                print(Fore.RED + style.BOLD + "Whoops, something is wrong! - Please check your config (See AboutTheConfig.txt for help)" + style.END)
                print()
                print(style.BOLD + "ERROR INFO:" + style.END, error)
                print()
                input("Press Enter to exit...")
                exit()
            time.sleep(1)
intents = discord.Intents.default()
intents.guilds = True
client = discord.Client(command_prefix='!', intents=discord.Intents.all())

toUse = 0
x = 0
sentUsers = []

def start_send_threads(items_list, amount):
    num_threads = len(items_list)
    chunk_size = amount // num_threads
    messages_sent_by_thread = []  # Create a list to collect messages sent by each thread

    # Print the amount each thread will process
    for i, items in enumerate(items_list):
        print(f"Thread {i+1} will process {len(items)} items.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_thread = {executor.submit(send, items, i, num_threads): i for i, items in enumerate(items_list)}
        for future in concurrent.futures.as_completed(future_to_thread):
            thread_num = future_to_thread[future]
            try:
                messages_sent = future.result()
                messages_sent_by_thread.append(messages_sent)  # Collect messages sent by each thread
            except Exception as exc:
                print(f'[?] Thread {thread_num+1} generated an exception: {exc}')


@client.event
async def on_message(message):
    global toUse
    global x
    global listNew
    global sentUsers
    global user
    global userIDs
    global proxys
    global cookies
    global groupLink
    global num_threads
    global messagesSent
    global amount
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
            embed = discord.Embed(title="Hello! I am Foox's Message Bot for Roblox!", description="I can advertise your roblox group from the following commands:", color=0x87DC76)
            embed.add_field(name="!help", value="brings up this command.", inline=False)
            embed.add_field(name="!send <amount> <group link>", value="Send a set amount of messages.", inline=False)
            embed.add_field(name="!cookie", value="Removes all invalid cookies", inline=False)
            embed.add_field(name="!size", value="Displays the current amount of users scraped", inline=False)
            embed.add_field(name="!members", value="Displays the current amount of members in your group.", inline=False)
            embed.add_field(name="!whitelist <discordUser>", value="Gives a user permison to use the bot.", inline=False)
            embed.add_field(name="!blacklist <discordUser>", value="Removes a user's permisson to use the bot.", inline=False)
            await message.channel.send(embed=embed)


    #command start
    if message.content.startswith('!members'):

        discordID = str(message.author.id)
        whitelisted = False
        with open("whitelistedusers.json") as jsonfile:
            config = json.load(jsonfile)
            whitelistedUsers = list(set(config))

        for whitelistedUser in whitelistedUsers:
            if whitelistedUser == int(discordID):
                whitelisted = True
                break
        if whitelisted == True:
            #bot stuff
            getGroup = requests.get(f"https://groups.roblox.com/v1/groups/{groupID}").json()
            groupName = getGroup["name"]
            members = getGroup["memberCount"]

            embed = discord.Embed(title=f"{groupName} total members", description=f"{members}", color=0x87DC76)


            await message.channel.send(embed=embed)
            #bot stuff

        else:
            embed = discord.Embed(title=f"Your not whitelisted", color=0x8D2D34)
            await message.channel.send(embed=embed)
    #command end
    #command start
    if message.content.startswith('!size'):

        discordID = str(message.author.id)
        whitelisted = False
        with open("whitelistedusers.json") as jsonfile:
            config = json.load(jsonfile)
            whitelistedUsers = list(set(config))

        for whitelistedUser in whitelistedUsers:
            if whitelistedUser == int(discordID):
                whitelisted = True
                break
        if whitelisted == True:
            with open("alreadymessaged.json", "r") as infile:
                dontMessage = json.load(infile)
                sizeDont = len(dontMessage)
            with open("members.json", "r") as infile:
                try:
                    config = json.load(infile)
                except:
                    embed = discord.Embed(title=f"Delimiter error", description=f"Try again", color=0xFF0000)
                    await message.channel.send(embed=embed)
                sizeMember = len(list(set(config)))
            embed = discord.Embed(title=f"Current Database Size", description=f"{sizeMember} for members({sizeDont} blacklisted; {sizeMember-sizeDont} available)", color=0x87DC76)
            await message.channel.send(embed=embed)
            #bot stuff

        else:
            embed = discord.Embed(title=f"You're not whitelisted", color=0x8D2D34)
            await message.channel.send(embed=embed)
    #command end

    #command start
    
    
    
    
    
    if message.content.startswith('!send'):
        discordID = str(message.author.id)
        whitelisted = False
        with open("whitelistedusers.json") as jsonfile:
            config = json.load(jsonfile)
            whitelistedUsers = list(set(config))

        for whitelistedUser in whitelistedUsers:
            if whitelistedUser == int(discordID):
                whitelisted = True
                break
        if whitelisted == True:
            words = message.content.split()
            if len(words) == 3:
                amount = int(words[1])
                groupLink = words[2]
                if autoThreads == "True":
                    num_threads = math.ceil(len(cookies)/14)
                embed = discord.Embed(title=f"Sending {amount} Messages ({num_threads} Threads)", description=f"Please wait. This will take a while.", color=0x769adc)
                await message.channel.send(embed=embed)
                print(amount, groupLink)
                with open("alreadymessaged.json", "r") as infile:
                    dontMessage = json.load(infile)
                with open(f"members.json", "r") as infile:
                    try:
                        userIDs = json.load(infile)
                    except:
                        userIDs = json.load(infile)
                        embed = discord.Embed(title=f"Delimiter error", description=f"Try again", color=0xFF0000)
                        await message.channel.send(embed=embed)
                userIDs = list(set(userIDs) - set(dontMessage))
                random.shuffle(userIDs)
                size = len(userIDs)
                if size >= amount:
                    listFinal = userIDs[:amount]
                    print(num_threads)
                    chunk_size = len(listFinal) // num_threads
                    print(chunk_size)
                    thread_items = [listFinal[i * chunk_size: (i + 1) * chunk_size] for i in range(num_threads)]
                    start_send_threads([listFinal[i * chunk_size: (i + 1) * chunk_size] for i in range(num_threads)], amount)
                    embed = discord.Embed(title=f"Finished Sending Messages", description=f"Sent {messagesSent} messages ({errors} errors)", color=0x87DC76)
                    await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title=f"Invalid amount", description=f"Database has {size} users, you want {amount} users", color=0x8D2D34)
                    await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title=f"Invalid Message", description=f"!send <amount> <groupLINK>", color=0x8D2D34)
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title=f"Your not whitelisted", color=0x8D2D34)
            await message.channel.send(embed=embed)
    #command end







    if message.content.startswith('!whitelist'):
        discordID = str(message.author.id)
        whitelisted = False
        with open("whitelistedusers.json") as jsonfile:
            config = json.load(jsonfile)
            whitelistedUsers = list(set(config))


        text = str(message.content)
        userToWhitelist = str(re.findall(r'\d+', text))
        for whitelistedUser in whitelistedUsers:
            if whitelistedUser == int(discordID):
                text = str(message.content)
                userToWhitelist = re.findall(r'\d+', text)
                whitelistedUsers.append(int(userToWhitelist[0]))

                whitelistedUsers = json.dumps(whitelistedUsers)
                with open("whitelistedusers.json", "w") as outfile:
                    outfile.write(whitelistedUsers)

                embed = discord.Embed(title=f"Whitelisted {userToWhitelist[0]}", color=0x6B9B6B)
                await message.channel.send(embed=embed)
                whitelisted = True
                break
        if whitelisted == False:
            embed = discord.Embed(title=f"Your not whitelisted", color=0x8D2D34)
            await message.channel.send(embed=embed)
    
    if message.content.startswith('!blacklist'):
        discordID = str(message.author.id)
        whitelisted = False
        with open("whitelistedusers.json") as jsonfile:
            config = json.load(jsonfile)
            whitelistedUsers = list(set(config))


        text = str(message.content)
        userToWhitelist = str(re.findall(r'\d+', text))
        for whitelistedUser in whitelistedUsers:
            if whitelistedUser == int(discordID):
                text = str(message.content)
                userToWhitelist = re.findall(r'\d+', text)
                whitelistedUsers.remove(int(userToWhitelist[0]))

                whitelistedUsers = json.dumps(whitelistedUsers)
                with open("whitelistedusers.json", "w") as outfile:
                    outfile.write(whitelistedUsers)

                embed = discord.Embed(title=f"Blacklisted {userToWhitelist[0]}", color=0x6B9B6B)
                await message.channel.send(embed=embed)
                whitelisted = True
                break
        if whitelisted == False:
            embed = discord.Embed(title=f"Your not whitelisted", color=0x8D2D34)
            await message.channel.send(embed=embed)
    if message.content.startswith('!cookie'):
        discordID = str(message.author.id)
        embed = discord.Embed(title=f"Scanning Cookies...", description=f"Please wait", color=0x769adc)
        await message.channel.send(embed=embed)
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
                    print("[✔] adding valid cookie")
                    validCookies.append(cookie)
                elif check.status_code != 200:
                    print("[×] removing invalid cookie")
            except:
                 print("[×] removing invalid cookie")

        with open("cookies.txt", "w") as f:
            for cookie in validCookies:
                f.write("%s\n" % cookie)
        embed = discord.Embed(title=f"Finished Scanning Cookies", description=f"{len(cookies)-len(validCookies)} invalid cookies removed. {len(validCookies)} valid remaining.", color=0x87DC76)
        cookies = validCookies
        await message.channel.send(embed=embed)


client.run(token)
