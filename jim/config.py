import configparser
import os

_parser = None


def _conf_parser():
    global _parser

    if not _parser:
        _parser = configparser.RawConfigParser()

        if 'JIM_CONFIG' in os.environ:
            path = os.environ.get('JIM_CONFIG')
        else:
            path = "/etc/jim.conf"
        _parser.read(path)

    return _parser


def config_get(section, option):
    return _conf_parser().get(section, option)


def config_get_boolean(section, option):
    return _conf_parser().getboolean(section, option)


def config_get_int(section, option):
    return _conf_parser().getint(section, option)
