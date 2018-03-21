import discord
import time
import datetime

import jim.config as config
from jim import cmd_funcs, util

client = discord.Client()
stream = {}


@client.event
async def on_ready():
    print('Logged in as %s (%s)' % (client.user.name, client.user.id,))

    std_perms = ['Administrator', 'Moderator', 'Fungineer+']
    util.register_cmd("8ball", "Ask the magic 8 ball.", None, 2, cmd_funcs.eight_ball)
    util.register_cmd("addcom", "Adds a custom command.", std_perms, 3, cmd_funcs.addcom)
    util.register_cmd("about", "Gets general bot information.", None, 1, cmd_funcs.about)
    util.register_cmd("archive", "Archives a channel.", std_perms, 2, cmd_funcs.archive)
    util.register_cmd("delcom", "Deletes a custom command.", std_perms, 2, cmd_funcs.delcom)
    util.register_cmd("murder", "Murders a person.", None, 2, cmd_funcs.murder)
    util.register_cmd("namechange", "Change my nickname on that server.", std_perms, 2, cmd_funcs.namechange)
    util.register_cmd("roll", "Roll a die.", None, 2, cmd_funcs.roll)
    util.register_cmd("ping", "Ping the bot.", None, 1, cmd_funcs.ping)


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
    if util.is_command(message):
        if util.check_permissions(message):
            await client.send_message(message.channel, await util.run_command(message))
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
