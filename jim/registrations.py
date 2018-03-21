from jim import cmd_funcs, util


def register_cmds():
    std_perms = ['Administrator', 'Moderator', 'Fungineer+']
    util.register_cmd("8ball", "Ask the magic 8 ball.", None, 2, cmd_funcs.eight_ball)
    util.register_cmd("addcom", "Adds a custom command.", std_perms, 3, cmd_funcs.addcom)
    util.register_cmd("about", "Gets general bot information.", None, 1, cmd_funcs.about)
    util.register_cmd("archive", "Archives a channel.", std_perms, 2, cmd_funcs.archive)
    util.register_cmd("delcom", "Deletes a custom command.", std_perms, 2, cmd_funcs.delcom)
    util.register_cmd("mcinfo", "Get information on the Minecraft server", None, 1, cmd_funcs.mcinfo)
    util.register_cmd("murder", "Murders a person.", None, 2, cmd_funcs.murder)
    util.register_cmd("namechange", "Change my nickname on that server.", std_perms, 2, cmd_funcs.namechange)
    util.register_cmd("roll", "Roll a die.", None, 2, cmd_funcs.roll)
    util.register_cmd("ping", "Ping the bot.", None, 1, cmd_funcs.ping)
    util.register_cmd("willie", "Ask Willie a question.", None, 2, cmd_funcs.willie)


def register_patterns():
    util.register_pattern(r'%%name%%.*\?', cmd_funcs.eight_ball)
    util.register_pattern(r'hi %%name%%!', cmd_funcs.hello_jim)
