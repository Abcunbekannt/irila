import asyncio
import random
import pickle
import os
from asyncio import wait_for
import _json
import json
import discord
import time

from discord import User
from discord import Member, Guild, guild
from discord.ext import commands
client = discord.Client()
#########################################################################
antworten = ['Ja', 'Nein', 'Vielleicht', 'Wahrscheinlich', 'Sieht so aus', 'Sehr wahrscheinlich',
             'Sehr unwahrscheinlich']
logchannelid = 0
neueid = 0
m = {}
amout1 =0
neueid2 = 0
memberupdateid = 0
YOURGUILDSID = 699934843961868319
YOURID = 667476267477762068
suggest = False
users = 0
mess = 0
count = 0
tempc = 0
amoutk = 10
amoutb = 100
global_chat_channel_name = "globalchat"
suggest_chat_channel_name = "suggestions"
suggest_chat_channel_name2 = "vorschläge"
ticket_chat_channel_name = "ticket-erstellen"
ticket_chat_channel_name2 = "create-ticket"
ticket_chat_channel_name3 = "ticket-support"
filesize = os.path.getsize("next244.txt")

blacklistwords = ['arsch', 'anal', 'hure', 'anal', 'ficken']
os.chdir(r'C:\pythonprojects\test001\21.4')


@client.event
async def on_member_update(before, after):
    if not before.bot:
        channel = client.get_channel(memberupdateid)  # Hier deine Channel ID rein
        global count
        if before.guild.id == 699934843961868319:  # Hier deine Server-ID rein
            if before.status != after.status:
                count = count - count
                for m in after.guild.members:
                    if not str(m.status) == 'offline':  # Heißt dass der "Offline" Status nicht mit gezählt wird
                        count = count + 1
                        print(count)
                #await channel.edit(name="🔴 Online: {}".format(count))


@client.event
async def on_ready():
    print('Wir sind eingeloggt als User {}'.format(client.user.name))
    client.loop.create_task(status_task())
    # client.loop.create_task(help_menu())
    if filesize == 18:
        with open('next244.txt', 'r') as f:
            # print(filesize)
            global logchannelid
            logchannelid = f.readline()
            print(logchannelid)
        with open('on_member_update_id.txt', 'r') as f:
            global memberupdateid
            memberupdateid = f.readline()
            print('memberupdatid:' + memberupdateid)
    with open('deutscheblacklist.txt', 'r') as f:
        # blacklistwords = [f.readlines()]
        print(blacklistwords)
    global m
    with open('memberswarns.json', "r") as jj:
        m = json.load(jj)
        jj.close()
    if len(m) == 0:
        m = {}
        for member in client.get_guild(YOURGUILDSID).members:
            m[str(member.id)] = {"warns": 0}
    with open('suggestions.json', "r") as j:
        f = json.load(j)
        j.close()
    if len(f) == 0:
        f = {}
        f = {"suggest": False}
    if len(f) != 0:
        global suggest
        suggest = str(f["suggest"])
        print(suggest)


# @client.event
# async def on_message(message: discord.Message):
# if message.author.bot:
# return
# if message.channel.name.lower() == global_chat_channel_name.lower():
# Nachicht wurde in einem GlobalChat geschrieben
# for guild in client.guilds:
# Geht durch alle Server in denen der Bot ist
# for channel in guild.channels:
# Geht durch alle Channels von den Servern
# if channel.name.lower() == global_chat_channel_name.lower():
# Checkt ob der channel GlobalChat heißt
# if channel.type == discord.ChannelType.text and message.channel.id != channel.id:
# Checkt ob der channel ein TextChannel ist
# und ob es nicht der ist in den die nachicht geschrieben würde
# embed = discord.Embed(title=str(message.author), description=str(message.content),
# color=0x99ccff)
# embed.set_thumbnail(url=message.author.avatar_url)
# await channel.send(embed=embed)
# sendet einen Embed mit Name, Nachicht und Profielbild
@client.event
async def read_logchannelid(logchennelid):
    filesize = os.path.getsize('next244.txt')
    if filesize == 18:
        with open('next244.txt', 'r') as f:
            logchennelid = f.readline()
async def clear_warn(towwho):
    m[str(towwho)]["warns"] = 0
    with open('memberswarns.json', "w") as j:
        j.write(json.dumps(m))
        j.close()
        print(f'closed json file after warns for {towwho} got reseted')
async def add_warn(towwho):
    m[str(towwho)]["warns"] += 1
    with open('memberswarns.json', "w") as j:
        j.write(json.dumps(m))
        j.close()
        print('closed json file after warn got added')
async def add_warnaction(amout,action,user,message):
    if m[str(message.author.id)]["warns"] >= amout:
        await message.author.send(f'{user}Du hast jetzt {amout} (oder mehr) Warnungen, die Admins haben festgelegt, dass du wegen dieser Anzahl von Warns ge{action}t wirst.')
        if action == 'ban':
            await user.ban()
            await message.channel.send(f'Member {user} gekickt.')

        if action == 'kick':
            #member: Member = discord.utils.find(lambda m: message.author in m.name, message.guild.members)
            #if member:
            await user.kick()
            await message.channel.send(f'Member {user} gekickt.')


                #global logchannelid
                # print(logchannelid)
                #channel = client.get_channel(int(logchannelid))
                #await channel.send(f'Member {member.name} gebannt.')
            #args = message.content.split(' ')
            #if len(args) == 2:
                #member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
                #if member:
                    #await member.ban()
                    #await message.channel.send(f'Member {member.name} gebannt.')
                #else:
                    #await message.channel.send(f'Kein user mit dem Namen {args[1]} gefunden.')

        #if action == kick:
        #if action == ban:
        #if action == mute:
        else:
            print('Fehler bei add_warnaction')

async def help_menu(message):
    while True:
        embedanfang = discord.Embed(
            title='⚙ Einstellungen',
            description='Hier sind die Einstellungen von Irila',
            colour=discord.Colour.red()
        )
        embedanfang.set_footer(
            text='Super! Du hast alles gelesen ! :) Hast du weitere Fragen oder Verbesserungsvorschläge? -> Wende dich an die Administratoren oder die Entwickler des Bot.')
        embedanfang.set_author(name='Irila Bot')
        embedanfang.add_field(name='🔧 Commands', value='Schickt dir die Hilfe mit allen Commands', inline=False)
        embedanfang.add_field(name=' ⠀⠀', value='🅰 -> Moderation', inline=False)
        embedanfang.add_field(name=' ⠀⠀', value='🅱 -> Gimmicks', inline=False)

        embedmodd = discord.Embed(
            title='⚙ Einstellungen >> Moderation',
            colour=discord.Colour.blue()
        )
        embedmodd.set_footer(
            text='Super! Du hast alles gelesen ! :) Hast du weitere Fragen oder Verbesserungsvorschläge? -> Wende dich an die Administratoren oder die Entwickler des Bot.')
        embedmodd.set_author(name='Irila Bot')
        embedmodd.add_field(name='🔧 Commands', value='Schickt dir die Hilfe mit allen Commands', inline=False)
        embedmodd.add_field(name='🅰 ->  🚪 KICK', value=' ⠀⠀', inline=False)
        page1 = embedanfang
        page2 = embedmodd
        pages = [page1, page2]

        messsettings2 = await message.channel.send(embed=pages[0])
        await messsettings2.add_reaction('◀')
        await messsettings2.add_reaction('🅰')
        await messsettings2.add_reaction('🅱')
        await messsettings2.add_reaction(u"\U0001F1E8")  # c
        await messsettings2.add_reaction(u"\U0001F1E9")  # d
        await messsettings2.add_reaction(u"\U0001F1EA")  # e
        await messsettings2.add_reaction(u"\U0001F1EB")  # f
        await messsettings2.add_reaction(u"\U0001F1EC")  # g
        await messsettings2.add_reaction(u"\U0001F1ED")  # h

        def check(reaction, user):
            return user == message.author and (str(reaction.emoji) == '◀' or
                                               (str(reaction.emoji) == '🅰') or
                                               (str(reaction.emoji) == '🅱') or
                                               (str(reaction.emoji) == u"\U0001F1E8") or
                                               (str(reaction.emoji) == u"\U0001F1E9") or
                                               (str(reaction.emoji) == u"\U0001F1EA") or
                                               (str(reaction.emoji) == u"\U0001F1EB") or
                                               (str(reaction.emoji) == u"\U0001F1EC") or
                                               (str(reaction.emoji) == u"\U0001F1ED")
                                               )

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await message.author.send('Zeitlimit für Reaktion abgelaufen')
        else:
            # jedes einzelnt und reactions dann in liste also reaction1=a in der liste dann reaction1
            emoji1 = '◀'
            emoji2 = '🅰'
            emoji3 = '🅱'
            emoji4 = u"\U0001F1E8"
            emoji5 = u"\U0001F1E9"
            emoji6 = u"\U0001F1EA"
            emoji7 = u"\U0001F1EB"
            emoji8 = u"\U0001F1EC"
            emoji9 = u"\U0001F1ED"
            stanardemojis = [emoji1, emoji2, emoji3, emoji4, emoji5, emoji6, emoji7, emoji8, emoji9]
            if str(reaction.emoji) == '◀':  # and pages[1] or pages[]
                await message.channel.purge(limit=1, check=is_not_pinned)
                await message.channel.send(embed=pages[0])
                await message.add_reaction(stanardemojis)
            if str(reaction.emoji) == '🅰':
                await message.channel.purge(limit=1, check=is_not_pinned)
                message = await message.channel.send(embed=pages[1])
                await message.add_reaction(stanardemojis[0])
                await message.add_reaction(stanardemojis[1])
                await message.add_reaction(stanardemojis[2])
                await message.add_reaction(stanardemojis[3])
                await message.add_reaction(stanardemojis[4])
                await message.add_reaction(stanardemojis[5])
                await message.add_reaction(stanardemojis[6])
                await message.add_reaction(stanardemojis[7])
                await message.add_reaction(stanardemojis[8])

    #while True:



@client.event
async def status_task():
    colors = [discord.Colour.red(), discord.Colour.orange(), discord.Colour.gold(), discord.Colour.green(),
              discord.Colour.blue(), discord.Colour.purple()]
    while True:
        await client.change_presence(activity=discord.Game('Ersteller Canned Heat'), status=discord.Status.online)
        await asyncio.sleep(5)
        # await client.change_presence(activity=discord.Game('Mein cooler Bot!'), status=discord.Status.online)
        # await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game('irila!help für Hilfe'), status=discord.Status.online)
        await asyncio.sleep(5)


def is_not_pinned(mess):
    return not mess.pinned


@client.event
# WIll ich das haben?
async def on_message(message):
    if message.author.bot:
        return
    #with open('mitglieder.txt','r') as f:
        #mitglieder = f.readlines()
    #await update_daten(mitglieder, user=client.user)
    #with open('mitglieder.txt', 'w') as f:
        #f.writelines()
    #with open('users.json','r') as f:
        #global users
        #users = json.load(f)
    #await update_data(users, message.author)
    #await add_experience(users, message.author, 5)
    #await level_up(users, message.author, message.channel)
    #with open('users.json','w') as f:
        #json.dump(users, f.write())
    global m
    global suggest
    global suggest_chat_channel_name3
    global tempc
    if message.content == "irila!stop" and message.author.id == YOURID:
        with open('memberswarns.json', "w") as j:
            j.write(json.dumps(m))
            j.close()
        await client.close()
    if message.content == "irila!warns":
        await message.channel.send('Deine aktuelle Anzahl von Verwarnungen ist: ' + str(m[str(message.author.id)]["warns"]))
    #elif message.author != client.user:
        #if m[str(message.author.id)]["messageCountdown"] <= 0:
            #m[str(message.author.id)]["xp"] += 10
            #m[str(message.author.id)]["messageCountdown"] = 10
    if message.content.startswith('irila!clearwarns') and message.author.guild_permissions.manage_roles:
        args = message.content.split(' ')
        if len(args) == 2:
            user = ' '.join(args[1:2])
            print(user)
            reason = ' ⠀⠀'
            print(reason)
            #memberw: Member = discord.utils.get(lambda m: args[1] in m.name, message.guild.members)
            memberw = discord.utils.find(lambda m: m.name == args[1], message.guild.members)
            #member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            print(memberw)
            embed = discord.Embed(title='Warn entfernen',
                                  description='**{}** warns wurden reseted'.format(user),
                                  color=0x00FF1F)
            embed.add_field(name='Aktion', value='Warns reseted',
                            inline=True),
            embed.add_field(name="Grund", value=reason,
                            inline=True)
            embed.add_field(name="Reseted von:", value=message.author,
                            inline=True)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_footer(text="Sollte es zu Missverständnissen gekommen sein, wende dich an die "
                                  "Adminstration!Warncase 2(Admin|Owner)")
            await message.author.send(f'Du hast erfolgreich {memberw} warns reseted')
            await message.channel.purge(limit=1, check=is_not_pinned)
            await memberw.send(embed=embed)
            mess7 = await message.channel.send(embed=embed)
            await asyncio.sleep(10)
            await mess7.channel.purge(limit=1, check=is_not_pinned)
            tempa = str(m[str(memberw.id)]["warns"])
            # print(tempa)
            tempb = int(tempa)
            # print(tempb)
            await memberw.send(f'Deine aktuelle Anzahl von Verwarnungen ist: 0')
            # print(memberw.id)
            await clear_warn(memberw.id)
            filesize = os.path.getsize('next244.txt')
            if filesize == 18:
                with open('next244.txt', 'r') as f:
                    logchennelid = f.readline()
            channel = client.get_channel(int(logchennelid))
            await channel.send(embed=embed)

    if message.content.startswith('irila!warn') and message.author.guild_permissions.manage_roles:
        args = message.content.split(' ')
        if len(args) == 2:
            user = ' '.join(args[1:2])
            print(user)
            reason = ' ⠀⠀'
            print(reason)
            #memberw: Member = discord.utils.get(lambda m: args[1] in m.name, message.guild.members)
            memberw = discord.utils.find(lambda m: m.name == args[1], message.guild.members)
            #member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            print(memberw)
            embed = discord.Embed(title='Warn',
                                  description='**{}** wurde gewarnt'.format(user),
                                  color=0x00FF1F)
            embed.add_field(name='Aktion', value='Warn',
                            inline=True),
            embed.add_field(name="Grund", value=reason,
                            inline=True)
            embed.add_field(name="Gewarnt von:", value=message.author,
                            inline=True)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_footer(text="Sollte es zu Missverständnissen gekommen sein, wende dich an die "
                                  "Adminstration!Warncase 2(Admin|Owner)")
            await message.author.send(f'Du hast erfolgreich {memberw} verwarnt')
            await message.channel.purge(limit=1, check=is_not_pinned)
            await memberw.send(embed=embed)
            mess7 = await message.channel.send(embed=embed)
            await asyncio.sleep(10)
            await mess7.channel.purge(limit=1, check=is_not_pinned)
            tempa = str(m[str(memberw.id)]["warns"])
            # print(tempa)
            tempb = int(tempa) + int(1)
            # print(tempb)
            await memberw.send(f'Deine aktuelle Anzahl von Verwarnungen ist: {tempb}')
            # print(memberw.id)
            await add_warn(memberw.id)
            filesize = os.path.getsize('next244.txt')
            if filesize == 18:
                with open('next244.txt', 'r') as f:
                    logchennelid = f.readline()
            channel = client.get_channel(int(logchennelid))
            await channel.send(embed=embed)




        if len(args) == 3:
            user = ' '.join(args[1:2])
            print(user)
            reason = ' '.join(args[2:])
            print(reason)
            #memberw: Member = discord.utils.get(lambda m: args[1] in m.name, message.guild.members)
            memberw = discord.utils.find(lambda m: m.name == args[1], message.guild.members)
            #member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            print(memberw)
            embed = discord.Embed(title='Warn',
                                  description='**{}** wurde gewarnt'.format(user),
                                  color=0x00FF1F)
            embed.add_field(name='Aktion', value='Warn',
                            inline=True),
            embed.add_field(name="Grund", value=reason,
                            inline=True)
            embed.add_field(name="Gewarnt von:", value=message.author,
                            inline=True)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_footer(text="Sollte es zu Missverständnissen gekommen sein, wende dich an die "
                                  "Adminstration!Warncase 2(Admin|Owner)")
            await message.author.send(f'Du hast erfolgreich {memberw} verwarnt')
            await message.channel.purge(limit=1, check=is_not_pinned)
            await memberw.send(embed=embed)
            mess7 = await message.channel.send(embed=embed)
            await asyncio.sleep(10)
            await mess7.channel.purge(limit=1, check=is_not_pinned)
            tempa = str(m[str(memberw.id)]["warns"])
            #print(tempa)
            tempb = int(tempa)+int(1)
            #print(tempb)
            await memberw.send(f'Deine aktuelle Anzahl von Verwarnungen ist: {tempb}')
            #print(memberw.id)
            await add_warn(memberw.id)
            filesize = os.path.getsize('next244.txt')
            if filesize == 18:
                with open('next244.txt', 'r') as f:
                    logchennelid = f.readline()
            #logchannelid2 = 0
            #await read_logchannelid(logchennelid=logchennelid)
            channel = client.get_channel(int(logchennelid))
            await channel.send(embed=embed)



                    #print('args[1] client.user')
                    #n = args[1]
                    #embedwarn = discord.Embed(title='Warnung',
                        #                      description=f'Du wurdest gewarnt von {urheber} und kein Grund wurde angegeben.')
                    # await n.send(f'Du wurdest gewarnt von {urheber} und kein Grund wurde angegeben.')
                    # await message.channel.send('Deine aktuelle Anzahl von Verwarnungen ist: ' + str(m[str(message.author.id)]["warns"]))
                    #mess7 = await message.channel.send(embed=embedwarn)
                    #await asyncio.sleep(5)
                    #await mess7.channel.purge(limit=1, check=is_not_pinned)
                    #await n.send(
                       # 'Deine aktuelle Anzahl von Verwarnungen ist: ' + str(m[str(message.author.id)]["warns"]))
                    #m[str(message.author.id)]["warns"] += 1
                    #with open('memberswarns.json', "w") as j:
                       # j.write(json.dumps(m))
                      #  j.close()
                     #   print('closed json file after user got warned')
                    #await message.author.send(
                    #    f'{str(args[1])}hat jetzt: ' + str(m[str(n.id)]["warns"]) + '  ' + ' Verwarnungen!')


    if message.content.startswith('irila!new') and message.channel.name.lower() == ticket_chat_channel_name.lower() or message.channel.name.lower() == ticket_chat_channel_name2.lower() or message.channel.name.lower() == ticket_chat_channel_name3.lower():
        #if category tickets exist
        with open("ticket_data.json") as g:
            data = json.load(g)

        ticket_number = int(data["ticket-counter"])
        ticket_number += 1
        print(ticket_number)
        #guild = discord.Guild
        #ticket_channel = await guild.create_text_channel( name=f"ticket-{ticket_number}", type=discord.ChannelType.text) #overwrites=None, category=None, reason=None)

    if message.channel.name.lower() == suggest_chat_channel_name.lower() or message.channel.name.lower() == suggest_chat_channel_name2.lower():
        # Nachicht wurde in einem GlobalChat geschrieben
        for guild in client.guilds:
            # Geht durch alle Server in denen der Bot ist
            for channel in guild.channels:
                # Geht durch alle Channels von den Servern
                if channel.name.lower() == suggest_chat_channel_name.lower() or suggest_chat_channel_name2.lower():
                    if suggest == True:
                        await message.add_reaction ('✔')
                        await message.add_reaction ('❌')
                    #if suggest == False:
                        #print('Suggestion made but suggestions were turned off')
    if message.content.startswith ('irila!suggestchannel'): #currently not working
        args = message.content.split(' ')
        if len(args) == 2:
            print('len args suggestchannelset = 2 '+ args[1])
            #args[1] = '#'+args[1]
            print (args[1])
            for guild in client.guilds:
                # Geht durch alle Server in denen der Bot ist
                for channel in guild.channels:
                    # Geht durch alle Channels von den Servern
                    if channel.name.lower() == args[1]:
                        #hier geht er nicht rein
                        suggest_chat_channel_name3 = args[1]
                        print(suggest_chat_channel_name3)
                        print(args[1])
    if message.content == 'irila!suggestoff':
        suggest = False
        await message.channel.send(f"{message.author} you have turned suggestions off. Valid names for suggestionchannels are '{suggest_chat_channel_name}' and '{suggest_chat_channel_name2}'")
        f = {"suggest": False}
        with open('suggestions.json', "w") as j:
            j.write(json.dumps(f))
            j.close()
            print('closed json file after suggest set to true ')
    if message.content == 'irila!suggeston':
        suggest = True
        await message.channel.send(f"{message.author} you have turned suggestions on. Valid names for suggestionchannels are '{suggest_chat_channel_name}' and '{suggest_chat_channel_name2}'")
        f = {"suggest": True}
        with open('suggestions.json', "w") as j:
            j.write(json.dumps(f))
            j.close()
            print('closed json file after suggest set to true ')
    if message.content.startswith('irila!help'):
        await message.channel.send('**Hilfe zum PyBot**\r\n'
                                   '**irila!help** - Zeigt diese Hilfe an\r\n'
                                   '**irila!userinfo + Name des gewünschten Users** - Zeigt Infos zu dem User an\r\n'
                                   '**irila!8ball + Frage** - Der Bot kontaktiert das Orakel und schickt dir die Antwort des Orakels\r\n'
                                   '**irila!clear + Anzahl der Nachrichten, die gelöscht werden sollen** - Löscht die angegebene Anzahl von Nachrichten\r\n'
                                   '**irila!privatehelp** - Du bekommst die Hilfe per DM zugesendet\r\n'
                                   '**irila!ping + Nachricht** - Pingt die Nachricht, die du mit einem Leerzeichen nach irila!ping geschrieben hast\r\n'
                                   '**irila!tempping + Nachricht** - Pingt die Nachricht, die du mit einem Leerzeichen nach irila!ping geschrieben hast für 10 Sekunden\r\n'
                                   '**irila!embedhelp** - Zeigt die Embed-Hilfe an\r\n'
                                   '**irila!embedprivatehelp** - Du bekommst die Embed-Hilfe per DM zugesendet\r\n'

                                   )
    if str.lower(message.content) in blacklistwords:
        await message.delete()
        embed = discord.Embed(title="Wortgebrauch",
                              description=f'Du {message.author.mention} hast ein Wort genutzt was auf meiner Blacklist vermerkt ist!')
        #embed.set_thumbnail(
            #url="https://cdn.discordapp.com/attachments/703227380545618070/704430275802955806/filter-4881943_960_720.png")
        embed.add_field(name="Meine Aktion", value="Nachricht gelöscht + Verwarnung", inline=True)
        embed.add_field(name="Inhalt der Nachricht", value=message.content, inline=True)
        embed.add_field(name="Autor der Nachricht", value=message.author, inline=True)
        embed.add_field(name="Kanal ", value=message.channel, inline=True)
        mess6 = await message.channel.send(embed=embed)
        await asyncio.sleep(5)
        await mess6.channel.purge(limit=1, check=is_not_pinned)
        await message.author.send('Dieses Wort: {} ist hier verboten'.format(message.content))
        m[str(message.author.id)]["warns"] += 1
        with open('memberswarns.json', "w") as j:
            j.write(json.dumps(m))
            j.close()
            print('closed json file after blacklisted word was used')
        await message.author.send(f'{message.author}hat jetzt: ' + str(m[str(message.author.id)]["warns"]) + '  ' + ' Verwarnungen!')
        a = client.get_user(YOURID)
        await a.send(f'{message.author}hat jetzt: ' + str(m[str(message.author.id)]["warns"]) + '  ' + ' Verwarnungen!')

        #global amoutk
            #global actionk
            #global amoutb
            #global actionb
        await add_warnaction(amout=amoutk,action='kick',user=message.author,message=message)
        await add_warnaction(amout=amoutb, action='ban', user=message.author, message=message)
    if message.content.startswith('irila!setamoutforkick'):
        args = message.content.split(' ')
        if len(args) == 2:
            #global amoutk
            args[1] = amoutk
            print(amoutk)
            print('Done')

    #if message.content.startswith('irila!addwarnaction') and message.author.permissions_in(message.channel).administrator:
        #await message.author.send('Aktuell kannst du aus ban und kick auswählen.)
        #await message.author.send('Gebe jetzt die Anzahl von Warns, bei der die Aktion ausgeführt werden soll.(Einfach nur die Zahl)')
        #if discord.ChannelType.private:
            #await client.wait_for('message', timeout=90, )  # channel= discord.ChannelType.private)
            #except asyncio.TimeoutError:
                #await message.author.send('Zeitlimit für Reaktion abgelaufen')
            #else:
                #args = message.content
                #if args[0].isdigit():
                    #global amout1
                    #message.content == amout1
                    #await message.author.send('Gebe jetzt in ban oder kick ein.')
                    #await client.wait_for('message', timeout=90, )  # channel=discord.ChannelType.private)
                    #except asyncio.TimeoutError:
                        #await message.author.send('Zeitlimit für Reaktion abgelaufen')
                    #else:
                        #if message.content == 'ban':
                            # global amoutb
                            #amout1 == amoutb
                        #if message.content == 'kick':
                            # global amoutk
                            #amout1 == amoutk


        #if message.content.startswith('{}'.isdigit()):
            #global amout1
            #global amoutk
            #message.content == amout1
            #await message.author.send('Gebe jetzt entweder :ban: oder :kick: ein um die Aktion anzugeben. (Lasse die : bitte weg !!)')
            ##if message.content == 'kick':
                #global actionk
                #global amoutk
                #amout1 = amoutk
                #actionk = 'kick'
                #print('worked set kick')
            #if message.content == 'ban':
                #global amoutb
                #global actionb
                #amout1 = amoutb
                #actionb = 'ban'
                #print('worked set ban')



    if message.content.startswith('irila!embedhelp'):
        embed = discord.Embed(
            title='Hilfe',
            description='Hier ist die Embed-Hilfe von Irila',
            colour=discord.Colour.red()

        )
        embed.set_footer(
            text='Super! Du hast die ganze Hilfe gelesen ! :) Hast du weitere Fragen oder Verbesserungsvorschläge? -> Wende dich an die Administratoren oder die Entwickler des Bot.')
        embed.set_author(name='Irila Bot')
        # embed.set_image(url='https://www.google.com/imgres?imgurl=https%3A%2F%2Ftechcrunch.com%2Fwp-content%2Fuploads%2F2017%2F04%2Fgettyimages-171206284.jpg%3Fw%3D730%26crop%3D1&imgrefurl=https%3A%2F%2Ftechcrunch.com%2F2017%2F04%2F05%2Ftalla-service-bot-lets-it-ease-into-ai%2F&tbnid=8yg_ws6WLBcvaM&vet=12ahUKEwj0_MLO-PnoAhUOr6QKHZ5tA90QMygAegUIARDvAQ..i&docid=idcsntOA3supAM&w=730&h=730&q=bot%20help&ved=2ahUKEwj0_MLO-PnoAhUOr6QKHZ5tA90QMygAegUIARDvAQ')
        embed.add_field(name='irila!help', value='Zeigt die Text-Hilfe an', inline=False)
        embed.add_field(name='irila!embedhelp', value='Zeigt diese Hilfe an', inline=False)
        embed.add_field(name='irila!privatehelp', value='Du bekommst die Text-Hilfe per DM zugesendet', inline=False)
        embed.add_field(name='irila!embedprivatehelp', value='Du bekommst die Embed-Hilfe per DM zugesendet',
                        inline=False)
        embed.add_field(name='irila!userinfo + Name des gewünschten Users', value='Zeigt Infos zu dem User an',
                        inline=False)
        embed.add_field(name='irila!8ball + Frage',
                        value='Der Bot kontaktiert das Orakel und schickt dir die Antwort des Orakels', inline=False)
        embed.add_field(name='irila!clear + Anzahl der Nachrichten, die gelöscht werden sollen',
                        value='Löscht die angegebene Anzahl von Nachrichten', inline=False)
        embed.add_field(name='irila!ping + Nachricht',
                        value='Pingt die Nachricht, die du mit einem Leerzeichen nach irila!ping geschrieben hast',
                        inline=False)
        embed.add_field(name='irila!tempping + Nachricht',
                        value='Pingt die Nachricht, die du mit einem Leerzeichen nach irila!ping geschrieben hast für 10 Sekunden',
                        inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith('irila!2'):
        embedanfang = discord.Embed(
            title='⚙ Einstellungen',
            description='Hier sind die Einstellungen von Irila',
            colour=discord.Colour.red()
        )
        embedanfang.set_footer(
            text='Super! Du hast alles gelesen ! :) Hast du weitere Fragen oder Verbesserungsvorschläge? -> Wende dich an die Administratoren oder die Entwickler des Bot.')
        embedanfang.set_author(name='Irila Bot')
        embedanfang.add_field(name='🔧 Commands', value='Schickt dir die Hilfe mit allen Commands', inline=False)
        embedanfang.add_field(name=' ⠀⠀', value='🅰 -> Moderation', inline=False)
        embedanfang.add_field(name=' ⠀⠀', value='🅱 -> Gimmicks', inline=False)

        embedmodd = discord.Embed(
            title='⚙ Einstellungen >> Moderation',
            colour=discord.Colour.blue()
        )
        embedmodd.set_footer(
            text='Super! Du hast alles gelesen ! :) Hast du weitere Fragen oder Verbesserungsvorschläge? -> Wende dich an die Administratoren oder die Entwickler des Bot.')
        embedmodd.set_author(name='Irila Bot')
        embedmodd.add_field(name='🔧 Commands', value='Schickt dir die Hilfe mit allen Commands', inline=False)
        embedmodd.add_field(name='🅰 ->  🚪 KICK', value=' ⠀⠀', inline=False)
        page1 = embedanfang
        page2 = embedmodd
        pages = [page1, page2]

        messsettings2 = await message.channel.send(embed=pages[0])
        await messsettings2.add_reaction('◀')
        await messsettings2.add_reaction('🅰')
        await messsettings2.add_reaction('🅱')
        await messsettings2.add_reaction(u"\U0001F1E8")  # c
        await messsettings2.add_reaction(u"\U0001F1E9")  # d
        await messsettings2.add_reaction(u"\U0001F1EA")  # e
        await messsettings2.add_reaction(u"\U0001F1EB")  # f
        await messsettings2.add_reaction(u"\U0001F1EC")  # g
        await messsettings2.add_reaction(u"\U0001F1ED")  # h

        def check(reaction, user):
            return user == message.author and (str(reaction.emoji) == '◀' or
                                               (str(reaction.emoji) == '🅰') or
                                               (str(reaction.emoji) == '🅱') or
                                               (str(reaction.emoji) == u"\U0001F1E8") or
                                               (str(reaction.emoji) == u"\U0001F1E9") or
                                               (str(reaction.emoji) == u"\U0001F1EA") or
                                               (str(reaction.emoji) == u"\U0001F1EB") or
                                               (str(reaction.emoji) == u"\U0001F1EC") or
                                               (str(reaction.emoji) == u"\U0001F1ED")
                                               )

        async def rst(r):
            if str(reaction.emoji) == r:
                print('rst')

        async def menu(i, message):
            await message.channel.purge(limit=1, check=is_not_pinned)
            message = await message.channel.send(embed=pages[i])
            await message.add_reaction(stanardemojis[0])
            await message.add_reaction(stanardemojis[1])
            await message.add_reaction(stanardemojis[2])
            await message.add_reaction(stanardemojis[3])
            await message.add_reaction(stanardemojis[4])
            await message.add_reaction(stanardemojis[5])
            await message.add_reaction(stanardemojis[6])
            await message.add_reaction(stanardemojis[7])
            await message.add_reaction(stanardemojis[8])

        async def welr(message):
            print('Y')
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                print('Hallo')
                if str(reaction.emoji) == '🅰':
                    await menu(0, message)
            except asyncio.TimeoutError:
                print('Zeit abgelaufen')
            else:
                print('X')

        async def wait(message):
            print('Y')
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                print('Hallo')
                if str(reaction.emoji) == '🅰':
                    await menu(0, message)
            except asyncio.TimeoutError:
                print('Zeit abgelaufen')
            else:
                print('X')
                # if str(reaction.emoji) == '🅰':
                # await menu(0,message)

                # if str(reaction.emoji) == '◀':  # and pages[1] or pages[]
                # print('J')
                # await message.channel.purge(limit=1, check=is_not_pinned)
                # message = await message.channel.send(embed=pages[0])
                # await message.add_reaction(stanardemojis[0])
                # await message.add_reaction(stanardemojis[1])
                # await message.add_reaction(stanardemojis[2])
                # await message.add_reaction(stanardemojis[3])
                # await message.add_reaction(stanardemojis[4])
                # await message.add_reaction(stanardemojis[5])
                # await message.add_reaction(stanardemojis[6])
                # await message.add_reaction(stanardemojis[7])
                # await message.add_reaction(stanardemojis[8])

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await message.author.send('Zeitlimit für Reaktion abgelaufen')
        else:
            # jedes einzelnt und reactions dann in liste also reaction1=a in der liste dann reaction1
            emoji1 = '◀'
            emoji2 = '🅰'
            emoji3 = '🅱'
            emoji4 = u"\U0001F1E8"
            emoji5 = u"\U0001F1E9"
            emoji6 = u"\U0001F1EA"
            emoji7 = u"\U0001F1EB"
            emoji8 = u"\U0001F1EC"
            emoji9 = u"\U0001F1ED"
            stanardemojis = [emoji1, emoji2, emoji3, emoji4, emoji5, emoji6, emoji7, emoji8, emoji9]
            if str(reaction.emoji) == '◀':  # and pages[1] or pages[]
                await message.channel.purge(limit=1, check=is_not_pinned)
                message = await message.channel.send(embed=pages[0])
                await message.add_reaction(stanardemojis[0])
                await message.add_reaction(stanardemojis[1])
                await message.add_reaction(stanardemojis[2])
                await message.add_reaction(stanardemojis[3])
                await message.add_reaction(stanardemojis[4])
                await message.add_reaction(stanardemojis[5])
                await message.add_reaction(stanardemojis[6])
                await message.add_reaction(stanardemojis[7])
                await message.add_reaction(stanardemojis[8])
            if str(reaction.emoji) == '🅰':
                print('h')
                await message.channel.purge(limit=1, check=is_not_pinned)
                message = await message.channel.send(embed=pages[1])
                await message.add_reaction(stanardemojis[0])
                await message.add_reaction(stanardemojis[1])
                await message.add_reaction(stanardemojis[2])
                await message.add_reaction(stanardemojis[3])
                await message.add_reaction(stanardemojis[4])
                await message.add_reaction(stanardemojis[5])
                await message.add_reaction(stanardemojis[6])
                await message.add_reaction(stanardemojis[7])
                await message.add_reaction(stanardemojis[8])
                print('f')
                # client.event(h)
                # client.run(h)
                # client.close(h)
                # await client.start(h)
                # await h()
                # await wait(message)
                # if str(reaction.emoji) == '🅰':
                # await menu(0,message)



    if message.content.startswith('irila!settings'):
        embed = discord.Embed(
            title='⚙ Einstellungen',
            description='Hier sind die Einstellungen von Irila',
            colour=discord.Colour.red()

        )
        embed.set_footer(
            text='Super! Du hast alles gelesen ! :) Hast du weitere Fragen oder Verbesserungsvorschläge? -> Wende dich an die Administratoren oder die Entwickler des Bot.')
        embed.set_author(name='Irila Bot')
        embed.add_field(name='🔧 Commands', value='Schickt dir die Hilfe mit allen Commands', inline=False)
        embed.add_field(name='🅰 -> Moderation', value=None, inline=False)
        embed.add_field(name='🅱 -> Gimmicks', value=None, inline=False)
        global mess
        mess = await message.channel.send(embed=embed)
        await mess.add_reaction('🔧')
        await mess.add_reaction('🅰')
        await mess.add_reaction('🅱')
        channel = message.channel
        await channel.send('If you want you can tap one of the reactions and see what happens ;)')

        def check(reaction, user):
            return user == message.author and (str(reaction.emoji) == '🔧' or (str(reaction.emoji) == '🅰')
                                               )

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await message.author.send('Zeitlimit für Reaktion abgelaufen')
        else:
            if str(reaction.emoji) == '🔧':
                embed = discord.Embed(
                    title='Hilfe',
                    description='Hier ist die Embed-Hilfe von Irila',
                    colour=discord.Colour.red()

                )
                embed.set_footer(
                    text='Super! Du hast die ganze Hilfe gelesen ! :) Hast du weitere Fragen oder Verbesserungsvorschläge? -> Wende dich an die Administratoren oder die Entwickler des Bot.')
                embed.set_author(name='Irila Bot')
                # embed.set_image(url='https://www.google.com/imgres?imgurl=https%3A%2F%2Ftechcrunch.com%2Fwp-content%2Fuploads%2F2017%2F04%2Fgettyimages-171206284.jpg%3Fw%3D730%26crop%3D1&imgrefurl=https%3A%2F%2Ftechcrunch.com%2F2017%2F04%2F05%2Ftalla-service-bot-lets-it-ease-into-ai%2F&tbnid=8yg_ws6WLBcvaM&vet=12ahUKEwj0_MLO-PnoAhUOr6QKHZ5tA90QMygAegUIARDvAQ..i&docid=idcsntOA3supAM&w=730&h=730&q=bot%20help&ved=2ahUKEwj0_MLO-PnoAhUOr6QKHZ5tA90QMygAegUIARDvAQ')
                embed.add_field(name='irila!help', value='Zeigt die Text-Hilfe an', inline=False)
                embed.add_field(name='irila!embedhelp', value='Zeigt diese Hilfe an', inline=False)
                embed.add_field(name='irila!privatehelp', value='Du bekommst die Text-Hilfe per DM zugesendet',
                                inline=False)
                embed.add_field(name='irila!embedprivatehelp', value='Du bekommst die Embed-Hilfe per DM zugesendet',
                                inline=False)
                embed.add_field(name='irila!userinfo + Name des gewünschten Users', value='Zeigt Infos zu dem User an',
                                inline=False)
                embed.add_field(name='irila!8ball + Frage',
                                value='Der Bot kontaktiert das Orakel und schickt dir die Antwort des Orakels',
                                inline=False)
                embed.add_field(name='irila!clear + Anzahl der Nachrichten, die gelöscht werden sollen',
                                value='Löscht die angegebene Anzahl von Nachrichten', inline=False)
                embed.add_field(name='irila!ping + Nachricht',
                                value='Pingt die Nachricht, die du mit einem Leerzeichen nach irila!ping geschrieben hast',
                                inline=False)
                embed.add_field(name='irila!tempping + Nachricht',
                                value='Pingt die Nachricht, die du mit einem Leerzeichen nach irila!ping geschrieben hast für 10 Sekunden',
                                inline=False)
                abc = message.author
                await abc.send(embed=embed)
            if str(reaction.emoji) == '🅰':
                def is_me(m):
                    return m.author != client.user

                channel = message.channel
                await message.channel.purge(limit=2, check=is_not_pinned)
                embedmod = discord.Embed(
                    title='⚙ Einstellungen >> Moderation',
                    colour=discord.Colour.blue()

                )
                embedmod.set_footer(
                    text='Super! Du hast alles gelesen ! :) Hast du weitere Fragen oder Verbesserungsvorschläge? -> Wende dich an die Administratoren oder die Entwickler des Bot.')
                embedmod.set_author(name='Irila Bot')
                # embed.set_image(url='https://www.google.com/imgres?imgurl=https%3A%2F%2Ftechcrunch.com%2Fwp-content%2Fuploads%2F2017%2F04%2Fgettyimages-171206284.jpg%3Fw%3D730%26crop%3D1&imgrefurl=https%3A%2F%2Ftechcrunch.com%2F2017%2F04%2F05%2Ftalla-service-bot-lets-it-ease-into-ai%2F&tbnid=8yg_ws6WLBcvaM&vet=12ahUKEwj0_MLO-PnoAhUOr6QKHZ5tA90QMygAegUIARDvAQ..i&docid=idcsntOA3supAM&w=730&h=730&q=bot%20help&ved=2ahUKEwj0_MLO-PnoAhUOr6QKHZ5tA90QMygAegUIARDvAQ')
                embedmod.add_field(name='🔧 Commands', value='Schickt dir die Hilfe mit allen Commands', inline=False)
                embedmod.add_field(name='🅰 ->  🚪 KICK', value='-', inline=False)
                messmod = await message.channel.send(embed=embedmod)
                await messmod.add_reaction('◀')
                await messmod.add_reaction('🅰')

                def check(reaction, user):
                    return user == message.author and (str(reaction.emoji) == '◀' or (str(reaction.emoji) == '🅰')
                                                       )

                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await message.author.send('Zeitlimit für Reaktion abgelaufen')
                else:
                    if str(reaction.emoji) == '🅰':
                        await message.channel.purge(limit=1, check=is_not_pinned)
                        embedkick = discord.Embed(
                            title='⚙ Einstellungen >> Moderation >> 🚪 KICK',
                            description='Du kannst mit diesem Command und einem optionalen Grund einen User kicken. Natürlich sind Sicherheitsmaßnahmen eingebaut, dass nicht jeder Leute kicken kann.',
                            colour=discord.Colour.blue()

                        )
                        embedkick.set_author(name='Irila Bot')
                        embedkick.add_field(name='Benutzung', value='• irila!kick @User\r\n'
                                                                    '• irila!kick @User <Reason>',
                                            inline=True)
                        embedkick.add_field(name='Beispiele', value='• irila!kick @Irila\r\n'
                                                                    '• irila!kick @Irila Shut up!',
                                            inline=True)
                        messkick = await message.channel.send(embed=embedkick)
                        await messkick.add_reaction('◀')

    if 'irila!embedprivatehelp' in message.content:
        embed = discord.Embed(
            title='Embed-Hilfe',
            description='Hier ist die Embed-Hilfe von Irila',
            colour=discord.Colour.red()

        )
        embed.set_footer(
            text='Super! Du hast die ganze Hilfe gelesen ! :) Hast du weitere Fragen oder Verbesserungsvorschläge? -> Wende dich an die Administratoren oder die Entwickler des Bot.')
        embed.set_author(name='Irila Bot')
        embed.add_field(name='irila!help', value='Zeigt die Text-Hilfe an', inline=False)
        embed.add_field(name='irila!embedhelp', value='Zeigt diese Hilfe an', inline=False)
        embed.add_field(name='irila!privatehelp', value='Du bekommst die Text-Hilfe per DM zugesendet', inline=False)
        embed.add_field(name='irila!embedprivatehelp', value='Du bekommst die Embed-Hilfe per DM zugesendet',
                        inline=False)
        embed.add_field(name='irila!userinfo + Name des gewünschten Users', value='Zeigt Infos zu dem User an',
                        inline=False)
        embed.add_field(name='irila!8ball + Frage',
                        value='Der Bot kontaktiert das Orakel und schickt dir die Antwort des Orakels', inline=False)
        embed.add_field(name='irila!clear + Anzahl der Nachrichten, die gelöscht werden sollen',
                        value='Löscht die angegebene Anzahl von Nachrichten', inline=False)
        embed.add_field(name='irila!ping + Nachricht',
                        value='Pingt die Nachricht, die du mit einem Leerzeichen nach irila!ping geschrieben hast',
                        inline=False)
        embed.add_field(name='irila!tempping + Nachricht',
                        value='Pingt die Nachricht, die du mit einem Leerzeichen nach irila!ping geschrieben hast für 10 Sekunden',
                        inline=False)
        await message.channel.send('Du hast die Embed-Hilfe per DM erhalten.:thumbsup:')
        await message.author.send(embed=embed)
    if message.content.startswith('irila!3'):
        await help_menu(message=message)

    if 'irila!privatehelp' in message.content:
        await message.channel.send('Du hast die Hilfe per DM erhalten.:thumbsup:')
        await message.author.send('> **Hilfe zum PyBot**\r\n'
                                  '> **irila!help** - Zeigt diese Hilfe an\r\n'
                                  '> **irila!userinfo** + Name des gewünschten Users - Zeigt Infos zu dem User an\r\n'
                                  '> **irila!8ball + Frage** - Der Bot kontaktiert das Orakel und schickt dir die Antwort des Orakels\r\n'
                                  '> **irila!clear + Anzahl der Nachrichten, die gelöscht werden sollen** - Löscht die angegebene Anzahl von Nachrichten\r\n'
                                  '> **irila!privatehelp** - Du bekommst die Hilfe per DM zugesendet\r\n'
                                  '> **irila!ping + Nachricht** - Pingt die Nachricht, die du mit einem Leerzeichen nach irila!ping geschrieben hast\r\n'
                                  '> **irila!tempping + Nachricht** - Pingt die Nachricht, die du mit einem Leerzeichen nach irila!ping geschrieben hast für 10 Sekunden\r\n'
                                  '**irila!embedhelp** - Zeigt die Embed-Hilfe an\r\n'
                                  '**irila!embedprivatehelp** - Du bekommst die Embed-Hilfe per DM zugesendet\r\n'

                                  )
    if message.content.startswith('irila!pin'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) == 2:
                Pin = str(args[1])
                Autor = message.author
                autormention = Autor.mention
                await message.author.send('{} Deine Nachricht: {} wurde angepinnt'.format(autormention, args[1]))
                message = await message.channel.send('{}'.format(args[1]))
                await message.pin()
        if not message.author.permissions_in(message.channel).manage_messages:
            autormention = Autor.mention
            await message.channel.send(
                '{} Dir fehlen leider die Berechtigungen, um diesen Befehl auszuführen!'.format(autormention))
        if not len(args) == 2:
            aa = message.author.mention
            await message.channel.send('{} Fehler! Du hast keine Nachricht angegeben'.format(aa))
    if message.content.startswith('irila!temppin'):
        args = message.content.split(' ')
        if len(args) == 2:
            aa = message.author.mention
            await message.author.send('{} Deine Nachricht: "{}" wird für 10 Sekunden angepinnt'.format(aa, args[1]))
            message = await message.channel.send('{}'.format(args[1]))
            await message.pin()
            time.sleep(10)
            await message.unpin()
        if not len(args) == 2:
            aa = message.author.mention
            await message.channel.send('{} Fehler! Du hast keine Nachricht angegeben'.format(aa))
    if message.content.startswith('irila!clear'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit=count, check=is_not_pinned)
                    await message.channel.send('{} Nachrichten gelöscht.'.format(len(deleted) - 1))
            if not len(args) == 2:
                await message.channel.send('Du hast leider keine oder zuviele Zahlen angegeben.')
        if not message.author.permissions_in(message.channel).manage_messages:
            await message.channel.send(
                '{} Dir fehlen leider die Berechtigungen, um diesen Befehl auszuführen!'.format(message.author.mention))
    if message.content.startswith('irila!8ball'):
        args = message.content.split(' ')
        if len(args) >= 2:
            frage = ' '.join(args[1:])
            mess = await message.channel.send('Ich versuche deine Frage `{0}` zu beantworten.'.format(frage))
            await asyncio.sleep(2)
            await mess.edit(content='Ich kontaktiere das Orakel...')
            await asyncio.sleep(2)
            await mess.edit(content='Deine Antwort zur Frage `{0}` lautet: `{1}`'
                            .format(frage, random.choice(antworten)))
    if message.content.startswith('irila!ban') and message.author.guild_permissions.ban_members:
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                await member.ban()
                await message.channel.send(f'Member {member.name} gebannt.')
            else:
                await message.channel.send(f'Kein user mit dem Namen {args[1]} gefunden.')
    if message.content.startswith('irila!unban') and message.author.guild_permissions.ban_members:
        args = message.content.split(' ')
        if len(args) == 2:
            user: User = discord.utils.find(lambda m: args[1] in m.user.name, await message.guild.bans()).user
            if user:
                await message.guild.unban(user)
                await message.channel.send(f'User {user.name} entbannt.')
            else:
                await message.channel.send(f'Kein user mit dem Namen {args[1]} gefunden.')
    if message.content.startswith('irila!kick') and message.author.guild_permissions.kick_members:
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                await member.kick()
                await message.channel.send(f'Member {member.name} gekickt.')
            else:
                await message.channel.send(f'Kein user mit dem Namen {args[1]} gefunden.')

    #if message.content.startswith('irila!kick') and message.author.permissions_in(message.channel).administrator:
        #args = message.content.split(' ')
        #if len(args) == 2:
            #member: Member = discord.utils.find(Lamba m: args[1] in m.name , message.guild.members)
            #if member:
                #await member.kick()

    #if message.content.startswith('irila!kick'):
        #if message.author.permissions_in(message.channel).administrator:
            #args = message.content.split(' ')
            #if len(args) >= 2:
                #print('lenargs >=2')
                #if args[1] == client.user:
                    #name = args[1]
                    #reason = args[2]
                    #print(args[1])
                    #await kick(user=name, reason=reason)
                #if args[1] != client.user:
                    #await message.author.send("Du kannst keinen Bot Kicken")
            #if len(args) < 2:
                #await message.channel.send("Fehler kein zu kickendes Mitglied angegeben.")
    if message.content.startswith('irila!setmessageupdatechannel'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) >= 2:
                idd = len(args[1])
                if args[1].isdigit() and len(args[1]) == 18:
                    filesize = os.path.getsize('on_member_update_id.txt')
                    if filesize == 0:
                        global memberupdateid
                        memberupdateid = args[1]
                        print(memberupdateid)
                        with open('on_member_update_id.txt', 'w') as f:
                            if filesize == 0:
                                print(filesize)
                                f.writelines(memberupdateid)
                                print('ausgeführt')
                    if filesize == 18:
                        global neueid2
                        neueid2 = args[1]
                        memberupdateid = neueid2
                        await message.channel.send(
                            'Du hast bereits eine Id angegeben möchtest du diese ändern? Dann antworte mit yes. Du hast 20 Sekunden Zeit.')
                    if filesize != 0:
                        print('Fehler Textfile hat schon eine Variable')
                    await message.channel.send('Du hast erfolgreich die ID eingestellt:{}'.format(memberupdateid))
                    channel = client.get_channel(int(memberupdateid))
                    # await channel.send('Hier ist ab jetzt dein Log-Channel')

                if args[1].isdigit() and len(args[1]) != 18:
                    await message.channel.send(
                        'Du hast leider keine Id angegeben, diese hätte 18 Stellen. Deine Angabe hatte {} Stellen'.format(
                            idd))
                if not args[1].isdigit():
                    await message.channel.send('Du hast keine Zahlen angegeben. Deine Eingabe war: {}'.format(args[1]))
            if len(args) == 1:
                await message.channel.send('Fehler: Keine Id angegeben.')
            if len(args) > 2:
                await message.channel.send('Fehler: Zuviele Zahlen.')
        else:
            await message.channel.send('Fehler: Du hast die benötigten Rechte (Nachrichten verwalten) nicht')
    if message.content.startswith('irila!showmessageupdatechannelid'):
        # global logchannelid
        await message.channel.send('Die Id des aktuellen message_update ist:{}'.format(memberupdateid))

    if message.content.startswith('irila!setlogchannel'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) >= 2:
                idd = len(args[1])
                if args[1].isdigit() and len(args[1]) == 18:
                    filesize = os.path.getsize('next244.txt')
                    if filesize == 0:
                        global logchannelid
                        logchannelid = args[1]
                        print(logchannelid)
                        with open('next244.txt', 'w') as f:
                            if filesize == 0:
                                print(filesize)
                                f.writelines(logchannelid)
                                print('ausgeführt')
                    if filesize == 18:
                        global neueid
                        neueid = args[1]
                        logchannelid = neueid
                        await message.channel.send(
                            'Du hast bereits eine Id angegeben möchtest du diese ändern? Dann antworte mit yes. Du hast 20 Sekunden Zeit.')
                    if filesize != 0:
                        print('Fehler Textfile hat schon eine Variable')
                    await message.channel.send('Du hast erfolgreich die ID eingestellt:{}'.format(logchannelid))
                    channel = client.get_channel(int(logchannelid))
                    await channel.send('Hier ist ab jetzt dein Log-Channel')

                if args[1].isdigit() and len(args[1]) != 18:
                    await message.channel.send(
                        'Du hast leider keine Id angegeben, diese hätte 18 Stellen. Deine Angabe hatte {} Stellen'.format(
                            idd))
                if not args[1].isdigit():
                    await message.channel.send('Du hast keine Zahlen angegeben. Deine Eingabe war: {}'.format(args[1]))
            if len(args) == 1:
                await message.channel.send('Fehler: Keine Id angegeben.')
            if len(args) > 2:
                await message.channel.send('Fehler: Zuviele Zahlen.')
        else:
            await message.channel.send('Fehler: Du hast die benötigten Rechte (Nachrichten verwalten) nicht')
    if message.content.startswith('irila!showlogchannelid'):
        # global logchannelid
        await message.channel.send('Die Id des aktuellen Logchannels ist:{}'.format(logchannelid))
    if message.content.startswith("irila!rainbow"):
        await message.channel.purge(limit=1)
        nachricht = await message.channel.send(":green_circle:")
        await asyncio.sleep(1)
        await nachricht.edit(content=":red_circle:")
        await asyncio.sleep(1)
        await nachricht.edit(content=":blue_circle:")
        await asyncio.sleep(1)
        await nachricht.edit(content=":purple_circle:")
        await asyncio.sleep(1)
        await nachricht.edit(content=":brown_circle:")
        await message.channel.purge(limit=1)
    if message.content.startswith("irila!randomemoji"):
        emojis = [":boom:", ":grinning:", ":space_invader:", ":green_heart:", ":love_letter:", ":fist:", ":brain:",
                  ":man_bald_tone3:", ":woman_bowing:", ":man_firefighter_tone1:", ":mrs_claus_tone4:", ":bell:",
                  ":anger_right:", ":put_litter_in_its_place:", ":closed_lock_with_key:", ":mailbox_with_no_mail:",
                  ":soap:", ":moneybag:", ":iphone:", ":house_with_garden:", ":red_car:"]
        embed = discord.Embed(title="Randomemoji:")
        randomemoji = await message.channel.send(embed=embed)
        await randomemoji.add_reaction(random.choice(emojis))
    if message.content.startswith("irila!selbstzerstoerung"):
        selbstzer = await message.channel.send("__***SELBSTZERSTÖRUNG IN:***__")
        #await selbstzer.add_reaction(':three: ')
        await message.channel.send('Drei')
        await asyncio.sleep(1)
        await message.channel.purge(limit=1)
        await message.channel.send('Zwei')
        #await selbstzer.add_reaction(':two:')
        await asyncio.sleep(1)
        await message.channel.purge(limit=1)
        await message.channel.send('Eins')
        #await selbstzer.add_reaction(':one:')
        await asyncio.sleep(1)
        await message.channel.purge(limit=1)
        await selbstzer.edit(content=":boom::boom::boom: BOOM :boom::boom::boom:")
    if message.content.startswith("irila!serverinfo"):
        embed = discord.Embed(title="Serverinfo")
        embed.add_field(name="Name:", value=message.guild.name)
        embed.add_field(name="Member:", value=message.guild.member_count)
        embed.add_field(name="ID:", value=message.guild.id)
        await message.channel.send(embed=embed)
    if message.channel.name.lower() == global_chat_channel_name.lower():
        # Nachicht wurde in einem GlobalChat geschrieben
        for guild in client.guilds:
            # Geht durch alle Server in denen der Bot ist
            for channel in guild.channels:
                # Geht durch alle Channels von den Servern
                if channel.name.lower() == global_chat_channel_name.lower():
                    # Checkt ob der channel GlobalChat heißt
                    if channel.type == discord.ChannelType.text and message.channel.id != channel.id:
                        # Checkt ob der channel ein TextChannel ist
                        # und ob es nicht der ist in den die nachicht geschrieben würde
                        embed = discord.Embed(title=str(message.author), description=str(message.content),
                                              color=0x99ccff)
                        embed.set_thumbnail(url=message.author.avatar_url)
                        await channel.send(embed=embed)
                        # sendet einen Embed mit Name, Nachicht und Profielbild


@client.event
async def on_message_delete(message):
    if message.author.bot:
        return
    print("Gelöschte Nachricht " + message.content + " von " + str(message.author))
    global logchannelid
    # print(logchannelid)
    channel = client.get_channel(int(logchannelid))
    # print(channel)
    await channel.send("Gelöschte Nachricht: " + message.content + " von " + str(message.author))

@client.event
async def on_member_join(member):
    with open('users.json','r') as f:
        global users
        users = json.load(f)
    await update_data(users, member)
    with open('users.json','w') as f:
        json.dump(users, f)

@client.event
async def on_message_edit(before, after):
    print("Nachricht von " + str(before.author) + " geändert von " + before.content + " zu " + after.content)
    global logchannelid
    # print(logchannelid)
    channel = client.get_channel(int(logchannelid))
    # print(channel)
    await channel.send(
        "Nachricht von " + str(before.author) + "geändert von " + before.content + " zu " + after.content)
async def update_daten(mitglieder, user):
    if not user.id in mitglieder:
        mitglieder[user.id]= {}
        mitglieder[user.id]['experience'] = 0
        mitglieder[user.id]['level'] = 1
async def update_data(users, user):
    if not user.id in users:
        users[user.id]= {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 1
async def add_experience (users, user, exp):
    users[user.id]['experience'] += exp
async def level_up(users, user, channel):
    experience = users[user.id]['experience']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end :
        await client.send_message(channel, '{} ist zum Level {} aufgestiegen'.format(user.mention, lvl_end))
        users[user.id]['level']= lvl_end

# später für heroku client.run(viel azhelen) rausnehmen komplett und den Token in secrets bei heroku eingeben. Davor noch das # vor client.run(os.getenv('Token')) wegmachen
# client.run(os.getenv('Token'))
client.run('NzAyMTg1OTgxNzc5OTAyNTg0.Xp8Xrg.5x8dfdk1WBWD0pp506pm3__pe2s')
