import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from file import savejson,loadjson
import re

load_dotenv()
TOKEN=os.environ['TOKEN']
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


url = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
tweeturl = "https?://twitter.com/[\w/:%#\$&\?\(\)~\.=\+\-]+"
posturl = "https?://x.com/[\w/:%#\$&\?\(\)~\.=\+\-]+"
pixivurl="https?://(?:www\.)?pixiv.net/artworks/[\w/:%#\$&\?\(\)~\.=\+\-]+"

@client.event#init処理
async def on_ready():
    print("起動したンゴねぇ")
    await tree.sync()#スラッシュコマンドを同期
  
    


@tree.command(name="dm",description="DMへの送信のON/OFF")
async def selfsend(ctx:discord.Interaction):
  data = dict(loadjson("dm.json"))
  key = str(ctx.user.id)
  keydata=list(data.keys())
  if key in keydata:
    
    del data[key]
    savejson("dm.json",data)
    await ctx.response.send_message("OFFりました",ephemeral=True)
  else:
    data[key] = "on"
    savejson("dm.json",data)
    await ctx.response.send_message("ONになりました",ephemeral=True)
  
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  else:
    DMchannel="Direct Message with Unknown User"
    messagechannel=str(message.channel)
    if (messagechannel==DMchannel):
        channel = client.get_channel(int(int(os.environ['fulltokumeiid'])))
        embedcolor=0x37393E
        #embed = discord.Embed(description=message.content,color=embedcolor)
        #await channel.send(embed=embed)
        sendmessage=message.content
        if re.match(posturl, message.content):
          urls = re.findall(posturl, message.content)
          converted_urls = ""
          for url in urls:
            converted_url = url.replace("x.com", "fxtwitter.com")
            converted_url = re.sub(r'\?.*', '', converted_url)
            converted_urls += converted_url + "\n"
          sendmessage=converted_urls
          print("post")
        if re.match(tweeturl, message.content):
           urls = re.findall(tweeturl, message.content)
           converted_urls = ""
           for url in urls:
              converted_url = url.replace("twitter.com", "fxtwitter.com")
              converted_url = re.sub(r'\?.*', '', converted_url)
              converted_urls = converted_urls + converted_url + "\n"
           sendmessage=converted_urls
           print("tweet")
        if re.match(pixivurl, message.content):
           urls = re.findall(pixivurl, message.content)
           converted_urls = ""
           for url in urls:
              converted_url = url.replace("pixiv.net", "phixiv.net")
              converted_url = re.sub(r'\?.*', '', converted_url)
              converted_urls = converted_urls + converted_url + "\n"
           sendmessage=converted_urls
           print("pixiv")
        



        await channel.send(sendmessage)
        guild = client.get_guild(int(os.environ['serverid']))
        my_dict =loadjson("dm.json")
        useridlist=list(my_dict.keys())
        for key in useridlist:
          member = guild.get_member(int(key))
          await member.send(sendmessage)
          #await member.send(embed=embed)
        print(f"{message.author}が{message.content}と発言")
        f = open('log.txt', 'a')
        f.write(f"{message.author}が{message.content}と発言\n")
        f.close()
    
client.run(TOKEN)
