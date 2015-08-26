#!/usr/bin/env python3
"""
Imagine world where you can use all the websites and webservices in the world
via single command. Here comes ws - single, generic command-line tool
to access all kind of web services, including restful APIs and classic
websites. Ws simplifies complex and verbose web requests
to simple commands, which are easy to discover, use and tab-complete.


Here is how it works:


    ws google search bananas
    ws github search node

Lets make it even easier:

    ws :alias github gh
    ws gh search node

    (note that internal commands are prefixed with ":", to distinguish them from webservice calls)

Still we can do better:

    ws :binalias github gh

    gh search node
    #no need to append ws, as long as you have ~/.ws/bin added to your PATH


Want more services? Here they come:

    # list all supported sites and services
    ws :services

    # download or update facebook service definition
    ws :get facebook

    # download service definition stored outside of ws repository:

    ws :get github://username/repository/path
    ws :get file:///home/joe/services/joewebsite

Want to use features that require authentication? We got it covered:

    ws :account github --user joe --password *******
    ws github notifications
    # if you have more than one account, you can specify which one you want to use:

    ws joe@github notifications

Multiple variants of service:

    Your service may be available on staging and production.
    You may list available variants:

    ws :variants yourservice

    and select which want to use:

    ws yourservice/staging command
    ws yourservice/production command





Installation:

    You will need ws client. Its a simple python script, depending only on
    requests library. You can install it from you distribution repository,
    or use virtualenv to create local copy.

    To get it in debian or ubuntu, run:
        sudo apt-get install python3-requests

    Alternatively, you can set up virtualenv:

        sudo aptitude install virtualenv
        virtualenv -p python3 venv
        ./venv/bin/pip install requests

Usage:

    ./ws -h
    ./ws --help
    ./ws :services
    ./ws :update


Creating your own service:

    You can find example service here:

Adding your service to service directory:

    See https://github.com/Fiedzia/ws.
    Make a pull request,
    and it should be soon added there.

"""
import atexit
import json
import os
import re
import readline
import sys

import commands

from parse import ArgumentDescription, Command, Flag, Option
from utils import quit

try:
    import requests
except ImportError:
    quit('Cannot find requests library. Please install it, its awesome. Aborting.', exitcode=1)


try:
    from prompt_toolkit.shortcuts import get_input
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.validation import Validator, ValidationError
except ImportError:
    quit('Cannot import prompt_toolkit. Please install it.', exitcode=1)

BASEDIR = os.path.dirname((os.path.realpath(__file__)))
VERSION = (0, 0, 1)  # major, minor, release
VERSION_STR = '.'.join([str(v) for v in VERSION])


def tokenize(text):
    """
    Split text into tokens
    """
    # TODO: handle quotes and double quotes
    return text.strip().split()


def setup_user_directories():
    for dname in ('~/.ws/cache', '~/.ws/services', '~/.ws/bin', '~/.ws/aliases'):
        _dname = os.path.expanduser(dname)
    if not os.path.exists(_dname):
        os.makedirs(_dname, exist_ok=True)


def complete(text, state):
    if state < 3:
        return '(' + text + ')'
    else:
        return None


class WsCmdValidator(Validator):

    def validate(self, document):
        try:
            wscmd = WsCommand(None)
            wscmd.parse(tokenize(line))
        except Exception as e:
            raise ValidationError(message=str(e), index=0)

def run_shell():
    """
    Run interactive shell
    """
    print('Welcome to ws shell (v{}) '.format(VERSION_STR))
    print('type :help for help, type :q or press ^D to quit')
    setup_user_directories()
    histfile = os.path.join(os.path.expanduser("~/.ws"), "history")
    history = FileHistory(histfile)
    prompt = 'ws: '

    while True:
        try:
            line = get_input(prompt, history=history, validator=WsCmdValidator()).strip()
        except EOFError:
            quit()
        wscmd = WsCommand(None)
        try:
            wscmd.parse(tokenize(line))
            wscmd.run()
        except Exception as e:
            print('error: ' + str(e), file=sys.stderr)


def run():

    wscmd = WsCommand(None)
    wscmd.parse(sys.argv[1:])
    wscmd.run()

    # TODO: use only in interactive mode
    run_shell()

    cmd_args, service_args = extract_params()


class Env:

    def __init__(self, username=None, variant=None):
        self.username = username
        self.variant = variant


class WsCommand(Command):

    def available_flags(self):
        return [
            Flag('h', 'help', help='display help'),
            Flag('V', 'version', help='display version number'),
        ]

    def available_commands(self):
        return [commands.Help, commands.Quit, commands.Commands]

    def run(self):
        if self.flags['help']:
            print('help')
            quit(msg=None)
        elif self.flags['version']:
            print('.'.join([str(v) for v in VERSION]))
            quit(msg=None)
        elif self.command:
            self.command.run()


class Dummy:
    pass


class Service:

    """
    One line service description

    More detailed info
    """

    name = 'unnamed'

    def __init__(self, env, flags=None, options=None, arguments=None):
        self._meta = Dummy()
        self._env = env
        self._meta.endpoint = None
        self._meta.flags = flags
        self._meta.options = options
        self._meta.arguments = arguments

    def help(self):
        pass

    def available_commands(self):
        return []

    def available_flags(self):
        return {}

    def available_options(self):
        return {}

    def argument_info(self):
        return None


if __name__ == '__main__':
    run()
