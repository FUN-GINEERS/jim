import discord
import time
import datetime

client = discord.Client()
stream = {}


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
    print('Logged in as %s (%s)' % (client.user.name, client.user.id,))


@client.event
async def on_member_update(before, after):
    if after.game is not None and after.game.type == 1:
        if after.id not in stream or datetime.datetime.now() > stream[after.id]:
            tc = client.get_channel('348820905688039444')
            await client.send_message(tc, "%s is streaming! Check it out here: %s" % (after.name, after.game.url,))
        stream[after.id] = datetime.datetime.now() + datetime.timedelta(hours=1)

@client.event
async def on_message(message):
    if message.content.startswith('&ping'):
        await client.send_message(message.channel, "Pong!")

    elif message.content.startswith('&about'):
        await client.send_message(message.channel, "I am Jim! A bot created specially for " + message.server.name + "!")

    elif message.content.startswith("&murder"):
        await client.send_message(message.channel, "I am not capable of murder.")

    elif message.content.startswith("&archive"):
        if any(x in ['Administrator', 'Moderator', 'Fungineer+'] for x in list(map(lambda x: x.name, message.author.roles))):
            try:
                channel = client.get_channel(message.content.split(" ")[1][2:-1])
                await get_log(channel)
                await client.send_message(message.channel, "Done.")

            except IndexError:
                await client.send_message(message.channel, "I'm sorry, I could not do it...")
        else:
            await client.send_message(message.channel, "You do not have permission.")

    elif "<@423906836866007060>" in message.content:
        pass

    elif message.content.lower() == "hi jim!":
        await client.send_message(message.channel, "Hello " + message.author.mention + "!")

    elif message.content.lower() == "how are you jim?":
        await client.send_message(message.channel, "I wouldn't know. I am just a robot.")
        time.sleep(0.5)
        await client.send_message(message.channel, "How are you, " + message.author.mention + "?")

client.run("INSERT_CLIENT_KEY_HERE")
