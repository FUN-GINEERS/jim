import discord

import jim.config as config
from jim import registrations
from jim.util import util

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as %s (%s)' % (client.user.name, client.user.id,))
    registrations.register_cmds()
    registrations.register_patterns()


# @client.event
# async def on_member_update(_, after):
#     await twitch.notify(client, after)


@client.event
async def on_message(message):
    if (message.guild is not None and message.author == message.guild.me) or len(message.content) < 1:
        return

    if util.is_command(message):
        print("%s sent command %s" % (message.author.name, message.content,))
        if util.check_permissions(message):
            response = await util.run_command(client, message)
            if util.send_to_pm(message):
                await message.author.send(response)
            else:
                await message.channel.send(response)
        else:
            await message.channel.send("You do not have permission to use this command.")

    res = await util.check_patterns(client, message)
    if res is not None:
        await message.channel.send(res)


def main():
    client.run(config.config_get("general", "user_token"))


if __name__ == "__main__":
    main()
