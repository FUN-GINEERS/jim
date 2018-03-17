import discord
import time
import datetime
import pickle

import config

client = discord.Client()
stream = {}
custom_commands = {}

RESERVED_COMMANDS = ['ping', 'about', 'murder', 'addcom', 'delcom', 'archive', 'namechange']


async def get_log(channel):
    logs = client.logs_from(channel, limit=2 ** 32)
    log = []
    async for m in logs:
        log.append("%s: <%s> %s" % (m.timestamp, m.author, m.content,))

    with open(channel.name + ".txt", "w") as f:
        for x in log[-1::-1]:
            f.write(x + "\n")


@client.event
async def on_ready():
    global custom_commands
    print('Logged in as %s (%s)' % (client.user.name, client.user.id,))

    try:
        with open(config.custom_command_file, "rb") as f:
            custom_commands = pickle.load(f)
    except FileNotFoundError:
        custom_commands = {}
        with open(config.custom_command_file, "wb") as f:
            pickle.dump(custom_commands, f)

    print('Loaded custom command file')


@client.event
async def on_member_update(before, after):
    if after.game is not None and after.game.type == 1:
        if after.id not in stream or datetime.datetime.now() > stream[after.id]:
            tc = client.get_channel('348820905688039444')
            await client.send_message(tc, "%s is streaming! Check it out here: %s" % (after.name, after.game.url,))
        stream[after.id] = datetime.datetime.now() + datetime.timedelta(hours=1)

@client.event
async def on_message(message):
    if message.server.me.nick is not None:
        name = message.server.me.nick.lower()
    else:
        name = "jim"

    if message.content.startswith('&ping'):
        await client.send_message(message.channel, "Pong!")

    elif message.content.startswith('&about'):
        await client.send_message(message.channel, "I am Jim! A bot created specially for " + message.server.name + "!")

    elif message.content.startswith("&murder"):
        await client.send_message(message.channel, "I am not capable of murder.")

    elif message.content.startswith("&namechange"):
        try:
            if any(x in ['Administrator', 'Moderator', 'Fungineer+'] for x in list(map(lambda x: x.name, message.author.roles))):
                splitmsg = message.content.split(" ")
                if len(splitmsg) != 2:
                    await client.send_message(message.channel, "Invalid usage. Use format `&namechange new_name`")
                else:
                    await client.change_nickname(message.server.me, splitmsg[1])
                    await client.send_message(message.channel, "I am now known as " + splitmsg[1] + " here.")
            else:
                await client.send_message(message.channel, "You do not have permission.")

        except AttributeError:
            await client.send_message(message.channel, "I'm sorry, I cannot do that here.")


    elif message.content.startswith("&addcom"):
        try:
            if any(x in ['Administrator', 'Moderator', 'Fungineer+'] for x in list(map(lambda x: x.name, message.author.roles))):
                splitmsg = message.content.split(" ", 2)

                if len(splitmsg) < 3:
                    await client.send_message(message.channel, "Invalid usage. Use format `&addcom command Response`")

                if message.server is not None and message.server.id not in custom_commands:
                    custom_commands[message.server.id] = {}

                if splitmsg[1].lower() in custom_commands[message.server.id] or splitmsg[1].lower() in RESERVED_COMMANDS:
                    await client.send_message(message.channel, "Command already exists.")
                else:
                    custom_commands[message.server.id][splitmsg[1].lower()] = splitmsg[2]
                    with open(config.custom_command_file, "wb") as f:
                        pickle.dump(custom_commands, f)

                    await client.send_message(message.channel, "Command added!")

            else:
                await client.send_message(message.channel, "You do not have permission.")

        except AttributeError:
            await client.send_message(message.channel, "I'm sorry, I cannot do that here.")

    elif message.content.startswith("&delcom"):
        try:
            if any(x in ['Administrator', 'Moderator', 'Fungineer+'] for x in list(map(lambda x: x.name, message.author.roles))):
                splitmsg = message.content.split(" ")
                if len(splitmsg) < 2:
                    await client.send_message(message.channel, "Invalid usage. Use format `&delcom command`")

                if splitmsg[1].lower() in RESERVED_COMMANDS:
                    await client.send_message(message.channel, "I cannot remove that command.")
                else:
                    if splitmsg[1].lower() not in custom_commands[message.server.id]:
                        await client.send_message(message.channel, "I cannot remove a command that doesn't exist.")
                    else:
                        del custom_commands[message.server.id][splitmsg[1].lower()]
                        with open(config.custom_command_file, "wb") as f:
                            pickle.dump(custom_commands, f)

                        await client.send_message(message.channel, "Command deleted.")
            else:
                await client.send_message(message.channel, "You do not have permission.")

        except AttributeError:
            await client.send_message(message.channel, "I'm sorry, I cannot do that here.")


    elif message.content.startswith("&archive"):
        try:
            if any(x in ['Administrator', 'Moderator', 'Fungineer+'] for x in list(map(lambda x: x.name, message.author.roles))):
                try:
                    channel = client.get_channel(message.content.split(" ")[1][2:-1])
                    await get_log(channel)
                    await client.send_message(message.channel, "Done.")

                except IndexError:
                    await client.send_message(message.channel, "I'm sorry, I could not do it...")
            else:
                await client.send_message(message.channel, "You do not have permission.")

        except AttributeError:
            await client.send_message(message.channel, "I'm sorry, I cannot do that here.")

    elif "<@423906836866007060>" in message.content:
        pass

    elif message.content.lower() == "hi " + name + "!":
        await client.send_message(message.channel, "Hello " + message.author.mention + "!")

    elif message.content.lower() == "how are you " + name + "?":
        await client.send_message(message.channel, "I wouldn't know. I am just a robot.")
        time.sleep(0.5)
        await client.send_message(message.channel, "How are you, " + message.author.mention + "?")

    elif message.content.startswith("&"):
        command = message.content.split(" ")[0][1:]
        if message.server.id not in custom_commands or command not in custom_commands[message.server.id]:
            await client.send_message(message.channel, "<:willie_Left:387252988835790858> <:willie_head:387252451260235776> <:Willie_Right:387252999745044480>")
        else:
            await client.send_message(message.channel, custom_commands[message.server.id][command])

client.run(config.user_token)
