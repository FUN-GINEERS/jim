from jim import cmd_funcs
from jim.util.util import register_cmd, register_pattern, ADMINISTRATOR_PERM, MODERATOR_PERM


def register_cmds():
    register_cmd("8ball", "Ask the magic 8 ball.", None, 2, cmd_funcs.eight_ball, False)
    register_cmd("addcom", "Adds a custom command.", ADMINISTRATOR_PERM|MODERATOR_PERM, 3, cmd_funcs.addcom, False)
    register_cmd("about", "Gets general bot information.", None, 1, cmd_funcs.about, False)
    register_cmd("archive", "Archives a channel.", ADMINISTRATOR_PERM, 2, cmd_funcs.archive, False)
    register_cmd("delcom", "Deletes a custom command.", ADMINISTRATOR_PERM|MODERATOR_PERM, 2, cmd_funcs.delcom, False)
    register_cmd("help", "Prints this help.", None, 1, cmd_funcs.help, True)
    register_cmd("mcinfo", "Get information on the Minecraft server", None, 1, cmd_funcs.mcinfo, False)
    register_cmd("murder", "Murders a person.", None, 2, cmd_funcs.murder, False)
    register_cmd("namechange", "Change my nickname on that server.", ADMINISTRATOR_PERM, 2, cmd_funcs.namechange, False)
    register_cmd("roll", "Roll a die.", None, 2, cmd_funcs.roll, False)
    register_cmd("ping", "Ping the bot.", None, 1, cmd_funcs.ping, False)
    register_cmd("willie", "Ask Willie a question.", None, 2, cmd_funcs.wolfram, False)


def register_patterns():
    # TODO: Write documentation on how to make patterns and what all can be done here.
    register_pattern(r'%%name%%.*\?', cmd_funcs.eight_ball)
    register_pattern(r'hi %%name%%!', cmd_funcs.hello_jim)
