import discord

import jim.config as config
from jim import registrations
from jim.util import util, twitch

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as %s (%s)' % (client.user.name, client.user.id,))
    await client.change_presence(game=discord.Game(name="&help"))
    registrations.register_cmds()
    registrations.register_patterns()


@client.event
async def on_member_update(_, after):
    await twitch.notify(client, after)


@client.event
async def on_message(message):
    if message.author == message.server.me or len(message.content) < 1:
        return

    if util.is_command(message):
        if util.check_permissions(message):
            response = await util.run_command(client, message)
            if util.send_to_pm(message):
                await client.send_message(message.author, response)
            else:
                await client.send_message(message.channel, response)
        else:
            await client.send_message(message.channel, "You do not have permission to use this command.")

    res = await util.check_patterns(client, message)
    if res is not None:
        await client.send_message(message.channel, res)


def main():
    client.run(config.config_get("general", "user_token"))


if __name__ == "__main__":
    main()
