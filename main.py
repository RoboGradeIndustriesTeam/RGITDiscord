import discord
import discord.ext.commands as commands
from dotenv import load_dotenv
import json
import codecs
load_dotenv()
import os

bot = commands.Bot(command_prefix="!")
addEventsConfirms = [] # {'user': userid, 'channel': channelid,  'event': event, 'message': botmessage}

@bot.event
async def on_ready():
    print(f'{bot.user} запущен')

@bot.command()
async def hello(ctx):
    await ctx.send(f"Хай, {ctx.message.author.mention}")

@bot.command()
async def events(ctx):
    data = json.loads(codecs.open("database.json", encoding='utf-8').read())
    for i in data['events']:
        id_ = i["id"]
        name = i['name']
        desc = i['desc']
        link = i['link']
        await ctx.send(f"Айди в базе: {id_}\nНазвание: {name}\nОписание: {desc}\nСсылка: {link}")

@bot.command()
async def addEvent(ctx):
    data = json.loads(codecs.open("database.json", encoding='utf-8').read())
    i = {}
    print(len(ctx.message.content.split(";")))
    if len(ctx.message.content.split(";")) > 2:
        i.update({'id': data['events'][-1]['id'] + 1, "name": ctx.message.content.split(";")[0].replace("!addEvent", "").strip(), "desc": ctx.message.content.split(";")[1], "link": ctx.message.content.split(";")[2]})
        id_ = i["id"]
        name = i['name']
        desc = i['desc']
        link = i['link']
        sendedmsg : discord.Message = await ctx.send(f"Подвердить добавления конкурса\nАйди в базе: {id_}\nНазвание: {name}\nОписание: {desc}\nСсылка: {link}")
        await sendedmsg.add_reaction(":accept:821453588403716147")
        await sendedmsg.add_reaction(":cancel:821453700957995010")
        addEventsConfirms.append({'user': ctx.author.id, "channel": ctx.channel.id, "event": i, "message": sendedmsg})

@bot.event
async def on_reaction_add(reaction, user):
    for i in addEventsConfirms:
        if i['user'] == user.id:
            if reaction.emoji.name == "accept":
                data = json.loads(codecs.open("database.json", encoding='utf-8').read())
                newData = data
                newData['events'].append(i['event'])
                print(newData)
                codecs.open("database.json", encoding='utf-8', mode='w').write(json.dumps(newData, sort_keys=True, indent=4))
            await i['message'].delete()
bot.run(os.getenv('TOKEN'))