import discord

client = discord.Client()


async def get_log(channel, c):
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
async def on_message(message):
    if message.content.startswith('&ping'):
        await client.send_message(message.channel, "Pong!")

    elif message.content.startswith("&murder"):
        await client.send_message(message.channel, "I am not capable of murder.")

    elif message.content.startswith("&archive"):
        if any(x in ['Administrator', 'Moderator', 'Fungineer+'] for x in list(map(lambda x: x.name, message.author.roles))):
            try:
                channel = client.get_channel(message.content.split(" ")[1][2:-1])
                await get_log(channel, message.channel)
                await client.send_message(message.channel, "Done.")

            except IndexError:
                await client.send_message(message.channel, "I'm sorry, I could not do it...")
        else:
            await client.send_message(message.channel, "You do not have permission.")


client.run("ENTER_TOKEN_HERE")
