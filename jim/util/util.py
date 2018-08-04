import pickle
import re

from jim.command import Command
from jim.config import config_get

WILLIE_SHRUG = "<:willie_Left:387252988835790858> <:willie_head:387252451260235776> <:Willie_Right:387252999745044480>"

ADMINISTRATOR_PERM = 1
MODERATOR_PERM = 2

registered_commands = {}
registered_patterns = []
custom_commands = None


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
    if message.server is not None and message.server.me.nick is not None:
        name = message.server.me.nick
    else:
        name = "Jim"

    return name


def get_command_list():
    global registered_commands
    return list(registered_commands.keys())


def get_custom_commands():
    global custom_commands

    if custom_commands is None:
        with open(config_get("general", "command_file"), "rb") as f:
            custom_commands = pickle.load(f)

    return custom_commands


def is_command(message):
    return message.content[0] == '&'


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
    ccmds = get_custom_commands()

    if message.server.id in ccmds and cmd in ccmds[message.server.id]:
        return ccmds[message.server.id][cmd]
    elif cmd in registered_commands:
        return await registered_commands[cmd].run(client, message)
    else:
        return WILLIE_SHRUG
