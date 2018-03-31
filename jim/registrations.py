from jim import cmd_funcs
from jim.util import util


def register_cmds():
    std_perms = ['Administrator', 'Moderator', 'Botgineer+']
    util.register_cmd("8ball", "Ask the magic 8 ball.", None, 2, cmd_funcs.eight_ball, False)
    util.register_cmd("addcom", "Adds a custom command.", std_perms, 3, cmd_funcs.addcom, False)
    util.register_cmd("about", "Gets general bot information.", None, 1, cmd_funcs.about, False)
    util.register_cmd("archive", "Archives a channel.", std_perms, 2, cmd_funcs.archive, False)
    util.register_cmd("delcom", "Deletes a custom command.", std_perms, 2, cmd_funcs.delcom, False)
    util.register_cmd("help", "Prints this help.", None, 1, cmd_funcs.help, True)
    util.register_cmd("mcinfo", "Get information on the Minecraft server", None, 1, cmd_funcs.mcinfo, False)
    util.register_cmd("murder", "Murders a person.", None, 2, cmd_funcs.murder, False)
    util.register_cmd("namechange", "Change my nickname on that server.", std_perms, 2, cmd_funcs.namechange, False)
    util.register_cmd("roll", "Roll a die.", None, 2, cmd_funcs.roll, False)
    util.register_cmd("ping", "Ping the bot.", None, 1, cmd_funcs.ping, False)
    util.register_cmd("willie", "Ask Willie a question.", None, 2, cmd_funcs.wolfram, False)


def register_patterns():
    # TODO: Write documentation on how to make patterns and what all can be done here.
    util.register_pattern(r'%%name%%.*\?', cmd_funcs.eight_ball)
    util.register_pattern(r'hi %%name%%!', cmd_funcs.hello_jim)
