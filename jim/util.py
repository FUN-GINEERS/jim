import pickle

from jim.command import Command
from jim.config import config_get

WILLIE_SHRUG = "<:willie_Left:387252988835790858> <:willie_head:387252451260235776> <:Willie_Right:387252999745044480>"

registered_commands = {}
custom_commands = None


def check_permissions(message):
    global registered_commands
    cmd = extract_command(message)

    if cmd not in registered_commands:
        return True

    return registered_commands[cmd].check_permissions(message.author)


def extract_command(message):
    return message.content.split(' ')[1:]


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
    return True if message.content[0] == '&' else False


def register_cmd(cmd, desc, perms, numargs, func):
    global registered_commands
    c = Command(cmd, desc, perms, numargs, func)
    registered_commands[cmd] = c


async def run_command(client, message):
    global registered_commands
    global custom_commands
    global WILLIE_SHRUG
    cmd = extract_command(message)

    if cmd in custom_commands[message.server.id]:
        return custom_commands[message.server.id][cmd]
    elif cmd in registered_commands:
        await registered_commands[cmd].run(client, message)
    else:
        return WILLIE_SHRUG
