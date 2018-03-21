class Command:
    def __init__(self, name='', desc='', perms=None, numargs=1, func=None):
        self.name = name
        self.desc = desc
        self.perms = perms
        self.numargs = numargs
        self.func = func

    def __str__(self):
        return self.name

    def check_permissions(self, member):
        if self.perms is None or len(self.perms) == 0:
            return True
        elif not any(x in self.perms for x in list(map(lambda x: x.name, member.roles))):
            return False
        else:
            return True

    def check_args(self, message):
        if self.numargs == 0:
            return True

        if len(message.split(" ")) < self.numargs:
            return False
        else:
            return True

    async def run(self, client, message):
        if self.func is None:
            return None

        else:
            await self.func(client, message)
