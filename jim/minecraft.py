import pyalpm
import datetime
from dbus import SystemBus, Interface

from jim.config import config_get


def get_minecraft_info():
    bus = SystemBus()
    systemd = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
    manager = Interface(systemd, dbus_interface='org.freedesktop.systemd1.Manager')
    unit = manager.LoadUnit('spigot.service')
    uproxy = bus.get_object('org.freedesktop.systemd1', str(unit))
    state = Interface(uproxy, dbus_interface='org.freedesktop.DBus.Properties')
    active_state = str(state.Get('org.freedesktop.systemd1.Unit', 'ActiveState',
                                 dbus_interface='org.freedesktop.DBus.Properties'))

    if active_state == 'active':
        active_time = int(state.Get('org.freedesktop.systemd1.Unit', 'ActiveEnterTimestamp',
                                    dbus_interface='org.freedesktop.DBus.Properties'))
    else:
        active_time = 0

    alpm_handle = pyalpm.Handle("/", "/var/lib/pacman")
    local_db = alpm_handle.get_localdb()
    spigot_pkg = local_db.get_pkg("spigot")
    ver = spigot_pkg.version

    if active_state == 'active':
        out = "Minecraft server is up!\nUptime: %s\nVersion: %s\nAddress: %s" % \
              (datetime.datetime.now() - datetime.datetime.fromtimestamp(int(active_time/1000000)),
               ver.split(":")[1].split("-")[0],
               config_get("minecraft", "address"))
    else:
        out = "Minecraft server is down!"

    return out


if __name__ == "__main__":
    print(get_minecraft_info())
