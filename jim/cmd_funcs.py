import json
from os import path, makedirs
import pickle
from random import randint
import urllib.request

import wolframalpha

from jim import config, minecraft
from jim.util import util, DB


async def _get_log(client, channel):
    logs = client.logs_from(channel, limit=2 ** 32)
    log = []
    async for m in logs:
        attments = []
        for a in m.attachments:
            print("[INFO] Pulling file from <" + a["url"] + ">")
            savepath = "archives/" + channel.guild.name + "/" + channel.name + "/" + m.id + "/"
            attments.append(savepath + a["filename"])

            try:
                makedirs(savepath, mode=493)  # this mode is 0755
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

    with open(channel.guild.name + "-" + channel.name + ".json", "w") as f:
        json.dump(log, f)


async def addadmin(client, message):
    splitmsg = message.content.split(" ")

    if message.guild is None:
        return "Command must be run on a server."

    for x in message.mentions:
        DB.exec("INSERT INTO perms (server_id, perm_type, role_id, is_user) "
                "VALUES (%s, %d, %s, TRUE)" % (message.guild.id, util.ADMINISTRATOR_PERM, x.id))

    for x in message.role_mentions:
        DB.exec("INSERT INTO perms (server_id, perm_type, role_id, is_user) "
                "VALUES (%s, %s, %s, FALSE)" % (message.guild.id, util.ADMINISTRATOR_PERM, x.id))

    return "Granted permission to use administrator bot commands..."


async def addcom(client, message):
    if message.guild is None:
        return "Command must be ran on a server..."

    splitmsg = message.content.split(" ", 2)
    reserved = util.get_command_list()

    if len(splitmsg) < 3:
        return "Invalid usage. Use format `&addcom command Response`"

    if splitmsg[1] in reserved:
        return "Cannot add a reserved command..."

    res = DB.query("SELECT command FROM commands WHERE server_id = '%s' AND command = '%s'" %
                   (message.guild.id, splitmsg[1],))

    if len(res) > 0:
        return "Command already exists..."

    DB.exec("INSERT INTO commands (server_id, command, response) "
            "VALUES ('%s', '%s', '%s')" % (message.guild.id, splitmsg[1], splitmsg[2],))

    return "Command added..."


async def addmod(client, message):
    if message.guild is None:
        return "Command must be run on a server."

    for x in message.mentions:
        DB.exec("INSERT INTO perms (server_id, perm_type, role_id, is_user) "
                "VALUES ('%s', %d, '%s', TRUE)" % (message.guild.id, util.MODERATOR_PERM, x.id))

    for x in message.role_mentions:
        DB.exec("INSERT INTO perms (server_id, perm_type, role_id, is_user) "
                "VALUES ('%s', %s, '%s', FALSE)" % (message.guild.id, util.MODERATOR_PERM, x.id))

    return "Granted permission to use moderator bot commands..."


async def about(client, message):
    name = util.get_bot_name(message)

    if message.guild is None:
        s = "you"
    else:
        s = message.guild.name

    return "I am %s! A bot created by markzz specially for %s!" % (name, s,)


async def archive(client, message):
    try:
        channel = client.get_channel(message.content.split(" ")[1][2:-1])
        await _get_log(client, channel)
        return "Done."

    except IndexError:
        return "I'm sorry, I could not do it..."


async def deladmin(client, message):
    splitmsg = message.content.split(" ")

    if message.guild is None:
        return "Command must be run on a server."

    for x in message.mentions + message.role_mentions:
        DB.exec("DELETE FROM perms WHERE server_id = '%s' AND role_id = '%d'" %
                (message.guild.id, x.id))

    return "Revoked permission to use administrator bot commands..."


async def delcom(client, message):
    if message.guild is None:
        return "Message must be run on server."

    splitmsg = message.content.split(" ")

    DB.exec("DELETE FROM commands WHERE server_id = '%d' AND command = '%s'" %
            (message.guild.id, splitmsg[1],))

    return "Deleted command..."


async def delmod(client, message):
    _ = await deladmin(client, message)
    return "Revoked permission to use moderator bot commands..."


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
        await message.guild.me.edit(nick=splitmsg[1])
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


async def prefix(client, message):
    splitmsg = message.content.split(" ")
    if len(splitmsg) < 2:
        return "You need to provide a prefix..."

    DB.exec("UPDATE servers SET prefix = '%s' WHERE id = '%s'" % (splitmsg[1][0], message.guild.id,))
    return "Updated prefix to %s" % (splitmsg[1][0],)


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
