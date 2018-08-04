import json
from os import path, makedirs
import pickle
from random import randint
import urllib.request

import wolframalpha

from jim import config, minecraft
from jim.util import util


async def _get_log(client, channel):
    logs = client.logs_from(channel, limit=2 ** 32)
    log = []
    async for m in logs:
        attments = []
        for a in m.attachments:
            print("[INFO] Pulling file from <" + a["url"] + ">")
            savepath = "archives/" + channel.server.name + "/" + channel.name + "/" + m.id + "/"
            attments.append(savepath + a["filename"])

            try:
                makedirs(savepath, mode=493) # this mode is 0755
            except FileExistsError:
                pass

            if not path.exists(savepath + a["filename"]):
                req = urllib.request.Request(a["url"], data=None, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"})
                with open(savepath + a["filename"], "wb") as f:
                    f.write(urllib.request.urlopen(req).read())

        output = {
            "timestamp": m.timestamp.timestamp(),
            "name": m.author.name,
            "uid": m.author.id,
            "id": m.id,
            "message": m.clean_content,
            "attachments": attments,
        }
        log.append(output)

    with open(channel.server.name + "-" + channel.name + ".json", "w") as f:
        json.dump(log, f)


async def addcom(client, message):
    splitmsg = message.content.split(" ", 2)
    reserved = util.get_command_list()
    custom_commands = util.get_custom_commands()

    if len(splitmsg) < 3:
        return "Invalid usage. Use format `&addcom command Response`"

    if message.server is not None and message.server.id not in custom_commands:
        custom_commands[message.server.id] = {}

    if splitmsg[1].lower() in custom_commands[message.server.id] or splitmsg[1].lower() in reserved:
        return "Command already exists."
    else:
        custom_commands[message.server.id][splitmsg[1].lower()] = splitmsg[2]
        with open(config.config_get("general", "command_file"), "wb") as f:
            pickle.dump(custom_commands, f)

        return "Command added!"


async def about(client, message):
    name = util.get_bot_name(message)

    if message.server is None:
        s = "you"
    else:
        s = message.server.name

    return "I am %s! A bot created by markzz specially for %s!" % (name, s,)


async def archive(client, message):
    try:
        channel = client.get_channel(message.content.split(" ")[1][2:-1])
        await _get_log(client, channel)
        return "Done."

    except IndexError:
        return "I'm sorry, I could not do it..."


async def delcom(client, message):
    splitmsg = message.content.split(" ")
    reserved = util.get_command_list()
    custom_commands = util.get_custom_commands()

    if splitmsg[1].lower() in reserved:
        return "I cannot remove that command."
    else:
        if splitmsg[1].lower() not in custom_commands[message.server.id]:
            return "I cannot remove a command that doesn't exist."
        else:
            del custom_commands[message.server.id][splitmsg[1].lower()]
            with open(config.config_get("general", "command_file"), "wb") as f:
                pickle.dump(custom_commands, f)

            return "Command deleted."


async def eight_ball(client, message):
    responses = [
        "It is certain!",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes, definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy... try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again later.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful.",
        util.WILLIE_SHRUG,
    ]

    return responses[randint(0, len(responses)-1)]


async def hello_jim(client, message):
    return "Hello %s!" % (message.author.mention,)


async def help(client, message):
    ret = "```\n"
    ret += "I am Jim! "

    if util.get_bot_name(message).lower() != "jim":
        ret += "You may know me by the name %s and you requested me to give you " \
               "information on how to use my functions.\n" \
               % (util.get_bot_name(message),)
    else:
        ret += "You requested me to give you information on how to use my functions.\n"

    ret += "Commands:\n"
    for k, v in util.registered_commands.items():
        ret += "    &%s: %s (takes %d parameter%s)\n" % (k, v.desc, v.numargs - 1, '' if v.numargs - 1 == 1 else 's')

    ret += "```"

    return ret


async def mcinfo(client, message):
    return minecraft.get_minecraft_info()


async def murder(client, message):
    return "I am not capable of murder."


async def namechange(client, message):
    splitmsg = message.content.split(" ")
    if len(splitmsg) != 2:
        return "Invalid usage. Use format `&namechange new_name`"
    else:
        await client.change_nickname(message.server.me, splitmsg[1])
        return "I am now known as " + splitmsg[1] + " here."


async def roll(client, message):
    try:
        splitmsg = message.content.split(' ')
        dice = int(splitmsg[1][1:] if splitmsg[1][0] == 'd' else splitmsg[1])
        if dice < 1:
            return "You can't roll less than a one sided die!"
        elif dice > 1000:
            return "That's too many sides for one die."
        else:
            roll = randint(1, dice)
            if roll == 1:
                return str(roll) + " - critical fail!"
            elif roll == dice:
                return str(roll) + " - CRIT!"
            else:
                return str(roll) + "!"
    except ValueError:
        return "That's not a number!"
    except IndexError:
        return "Invalid usage. Use format `&roll d<number>`"


async def ping(client, message):
    return "Pong!"


async def wolfram(client, message):
    app_id = config.config_get('alpha', 'app_id')
    alpha_client = wolframalpha.Client(app_id)
    res = alpha_client.query(message.content.split(' ', 1)[1])

    results = []
    try:
        for x in res.results:
            for y in x.subpod:
                results.append(y.plaintext)
    except AttributeError:
        return "Not even %s knows." % (util.get_bot_name(message),)

    return '```\n' + '\n'.join(results) + '\n```'
