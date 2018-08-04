from jim.util import DB, util

class Command:
    def __init__(self, name='', desc='', perms=None, numargs=1, func=None, pm=False):
        self.name = name
        self.desc = desc
        self.perms = perms
        self.numargs = numargs
        self.func = func
        self.pm = pm

    def __str__(self):
        return self.name

    def check_permissions(self, member):
        if self.perms is not None:
            if (self.perms & util.MODERATOR_PERM) > 0:
                res = DB.query("SELECT * FROM perms WHERE server_id = '%s' AND perm_type = 2" % (member.server.id,))

                for row in res:
                    if not row[3] and row[2] in list(map(lambda x: x.id, member.roles)):
                        return True

                    if row[3] and row[2] == member.id:
                        return True

                    return False

            if (self.perms & util.ADMINISTRATOR_PERM) > 0:
                res = DB.query("SELECT * FROM perms WHERE server_id = '%s' AND perm_type = 1" % (member.server.id,))

                for row in res:
                    if not row[3] and row[2] in list(map(lambda x: x.id, member.roles)):
                        return True

                    if row[3] and row[2] == member.id:
                        return True

                    return False

        return True

    def check_args(self, message):
        if self.numargs == 0:
            return True

        if len(message.content.split(" ")) < self.numargs:
            return False
        else:
            return True

    async def run(self, client, message):
        if self.func is None:
            return None

        else:
            if self.check_args(message):
                return await self.func(client, message)
            else:
                return "Command requires %d parameters." % (self.numargs-1,)
