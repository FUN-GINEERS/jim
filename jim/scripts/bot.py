import discord
import time
import datetime

import jim.config as config
from jim import registrations, util

client = discord.Client()
stream = {}


@client.event
async def on_ready():
    print('Logged in as %s (%s)' % (client.user.name, client.user.id,))
    registrations.register_cmds()


@client.event
async def on_member_update(before, after):
    # Maybe later break this off.
    if after.game is not None and after.game.type == 1:
        if after.id not in stream or datetime.datetime.now() > stream[after.id]:
            tc = client.get_channel('348820905688039444')
            await client.send_message(tc, "%s is streaming! Check it out here: %s" % (after.name, after.game.url,))
        stream[after.id] = datetime.datetime.now() + datetime.timedelta(hours=1)


@client.event
async def on_message(message):
    if message.author == message.server.me:
        return

    if util.is_command(message):
        if util.check_permissions(message):
            response = await util.run_command(client, message)
            await client.send_message(message.channel, response)
        else:
            await client.send_message(message.channel, "You do not have permission to use this command.")

    name = util.get_bot_name(message).lower()

    if None:
        pass

    elif message.content.lower() == "hi " + name + "!":
        await client.send_message(message.channel, "Hello " + message.author.mention + "!")

    elif message.content.lower() == "how are you " + name + "?":
        await client.send_message(message.channel, "I wouldn't know. I am just a robot.")
        time.sleep(0.5)
        await client.send_message(message.channel, "How are you, " + message.author.mention + "?")


def main():
    client.run(config.config_get("general", "user_token"))


if __name__ == "__main__":
    main()
