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

    You will need ws client.

    You can install it from you distribution repository,
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
import json
import os
import re
import readline
import sys

from . import commands

from .parse import ArgumentDefinition, Command, Flag, Option
from .tokenize import tokenize
from .utils import quit

try:
    import requests
except ImportError:
    quit('Cannot find requests library. Please install it,'
         ' its awesome. Aborting.', exitcode=1)

try:
    from prompt_toolkit.shortcuts import get_input
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.validation import Validator, ValidationError
except ImportError:
    quit('Cannot import prompt_toolkit. Please install it.', exitcode=1)

BASEDIR = os.path.dirname((os.path.realpath(__file__)))
VERSION = (0, 0, 1)  # major, minor, release
VERSION_STR = '.'.join([str(v) for v in VERSION])


def setup_user_directories():
    for dname in ('~/.ws/cache', '~/.ws/services',
                  '~/.ws/bin', '~/.ws/aliases'):
        expanded_name = os.path.expanduser(dname)
    if not os.path.exists(expanded_name):
        os.makedirs(expanded_name, exist_ok=True)


class WsCmdValidator(Validator):

    def __init__(self, service_manager):
        self.service_manager = service_manager
        super().__init__()

    def validate(self, document):
        try:
            wscmd = WsCommand(None, service_manager=self.service_manager)
            wscmd.parse(tokenize(document.text))
        except Exception as e:
            #raise ValidationError(message=repr(e), index=0)
            raise


class Env:

    def __init__(self, username=None, variant=None):
        self.username = username
        self.variant = variant


class WsCommand(Command):

    def __init__(self, *args, service_manager=None, **kwargs):
        self.service_manager = service_manager
        self.service = None
        super().__init__(*args, **kwargs)

    def available_flags(self):
        return [
            Flag('h', 'help', help='display help'),
            Flag('V', 'version', help='display version number'),
        ]

    def available_commands(self):
        return commands.top_level_commands

    def parse_unknown(self, tokens):
        if self.service_manager.has_service(tokens[0].text):
            service_class = self.service_manager.get_service(tokens[0].text)
            self.service = service_class(env=None)
            if len(tokens) > 1:
                self.service.parse(tokens[1:])

    def run(self):
        if self.flags['help']:
            print('help')
            quit(msg=None)
        elif self.flags['version']:
            print(VERSION_STR)
            quit(msg=None)
        elif self.command:
            self.command.run()
        elif self.service:
            self.service.run()
        else:
            self.run_shell()

    def run_shell(self):
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
                line = get_input(prompt, history=history, validator=WsCmdValidator(self.service_manager)).strip()
            except EOFError:
                quit()
            wscmd = WsCommand(None, service_manager=self.service_manager)
            try:
                wscmd.parse(tokenize(line))
                wscmd.run()
            except Exception as e:
                print('error: ' + repr(e), file=sys.stderr)
