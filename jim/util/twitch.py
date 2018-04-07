import datetime

stream = {}


# this only will run on the FUN-GINEERS discord. If this needs to be changed, more needs to be done
async def notify(client, member):
    if not member.server.id == '234149610652696577':
        if member.game is not None and member.game.type == 1:
            if member.id not in stream or datetime.datetime.now() > stream[member.id]:
                tc = client.get_channel('348820905688039444')
                if tc is not None:
                    await client.send_message(tc, "%s is streaming! %s. Check it out here: %s" %
                                              (member.name, member.game.name, member.game.url,))
            stream[member.id] = datetime.datetime.now() + datetime.timedelta(hours=1)
