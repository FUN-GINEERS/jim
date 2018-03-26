import discord
import datetime

import jim.config as config
from jim import registrations
from jim.util import util

client = discord.Client()
stream = {}


@client.event
async def on_ready():
    print('Logged in as %s (%s)' % (client.user.name, client.user.id,))
    await client.change_status(discord.Game(name="&help"), False)
    registrations.register_cmds()
    registrations.register_patterns()


@client.event
async def on_member_update(before, after):
    # Maybe later break this off.
    if after.game is not None and after.game.type == 1:
        if after.id not in stream or datetime.datetime.now() > stream[after.id]:
            tc = client.get_channel('348820905688039444')
            await client.send_message(tc, "%s is streaming! %s. Check it out here: %s" %
                                      (after.name, after.game.name, after.game.url,))
        stream[after.id] = datetime.datetime.now() + datetime.timedelta(hours=1)


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
