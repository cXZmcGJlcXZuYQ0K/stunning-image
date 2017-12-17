from bot.utils.danny.dataIO import dataIO # import a utility file made by @Danny#0007
data = {"token": "none", "id": "none"}
print("Type the bot's secret token")
token = input("> ")
data["token"] = token
print("Input your id")
ownerid = input("> ")
data["id"] = ownerid # fix to int
dataIO.save_json("bot/storage/userinf.json", data)
quit() # exits the file
