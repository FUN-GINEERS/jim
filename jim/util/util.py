import pickle
import re

from jim.command import Command
from jim.config import config_get
from jim.util.DB import query, exec
from jim.util import util

WILLIE_SHRUG = "<:willie_Left:387252988835790858> <:willie_head:387252451260235776> <:Willie_Right:387252999745044480>"

ADMINISTRATOR_PERM = 1
MODERATOR_PERM = 2

registered_commands = {}
registered_patterns = []


def check_server_in_db(message):
    if message.guild is None:
        return False

    res = query("SELECT id FROM servers WHERE id = '%s'" % (message.guild.id,))

    if len(res) == 0:
        exec("INSERT INTO servers VALUES ('%s', '!')" % (message.guild.id,))

    return True


async def check_patterns(client, message):
    global registered_patterns
    name = get_bot_name(message).lower()

    for x in registered_patterns:
        a = x[0].replace("%%name%%", name)

        if re.match(a, message.content, re.IGNORECASE):
            return await x[1](client, message)

    return None


def check_permissions(message):
    global registered_commands
    cmd = extract_command(message)

    if cmd not in registered_commands:
        return True

    return registered_commands[cmd].check_permissions(message.author)


def extract_command(message):
    return message.content.split(' ')[0][1:]


def get_bot_name(message):
    if message.guild is not None and message.guild.me.nick is not None:
        name = message.guild.me.nick
    elif message.guild is None:
        name = message.channel.me.name
    else:
        name = message.guild.me.name

    return name


def get_command_list():
    global registered_commands
    return list(registered_commands.keys())


def custom_command(message):
    res = query("SELECT response FROM commands WHERE server_id = '%s' AND command = '%s'" %
                (message.guild.id, message.content.split(" ")[0][1:]))

    if len(res) == 0:
        return None

    return res[0][0]


def is_command(message):
    is_server = util.check_server_in_db(message)

    if is_server:
        res = query("SELECT prefix FROM servers WHERE id = '%s'" % (message.guild.id,))
        return message.content[0] == res[0][0]
    else:
        return message.content[0] == '!'


def register_cmd(cmd, desc, perms, numargs, func, pm):
    global registered_commands
    c = Command(cmd, desc, perms, numargs, func, pm)
    registered_commands[cmd] = c


def register_pattern(pattern, func):
    global registered_patterns
    registered_patterns.append([pattern, func])


def send_to_pm(message):
    global registered_commands
    cmd = extract_command(message)

    if cmd in registered_commands:
        return registered_commands[cmd].pm
    else:
        return False


async def run_command(client, message):
    global registered_commands
    global WILLIE_SHRUG
    cmd = extract_command(message)
    res = custom_command(message)

    if res is not None:
        return res
    elif cmd in registered_commands:
        return await registered_commands[cmd].run(client, message)
    else:
        return WILLIE_SHRUG
