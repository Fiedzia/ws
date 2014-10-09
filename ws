#!/usr/bin/env python3
#coding: utf8
"""
Imagine world where you can use all the webservices in the world via single
command. Here comes ws - single, generic command-line tool to access all kind of web services.

Add you service to ws service directory and let anyone use it without 
the need to create or deploy any software or installing anything beyond ws client.


Examples:


    ws example/cowsay say hello


     ------
    < hello >
     -------
     \ ^__^
      \ (oo)\_______
        (__)\ )\/\
             ||----w |
             ||     ||


    ws example/cowsay help

        Welcome to cow-as-as-service. We support following commands:

            help
                display help info

            say TEXT
                draw a cow saying TEXT



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
    ./ws --list-services
    ./ws service_provider/service_name command options


Creating your own service:

    You can find example service here:
    https://github.com/Fiedzia/cow-as-as-service

    Note that this is only an example. You can create your service
    with any language or framework you choose,
    as long as it speaks http.
    
Adding your service to service directory:

    See https://github.com/Fiedzia/servicedirectory.
    Add simple json file and make a pull request,
    and it should be soon added there.

"""


import argparse
import json
import os
import re
import sys


BASEDIR = os.path.dirname((os.path.realpath(__file__)))
SERVICE_DIRECTORY = 'https://raw.githubusercontent.com/Fiedzia/servicedirectory/master/services/'
VERSION = (0, 0, 0) #mino


missing_request=False
try:
    import requests
except ImportError:
    #try to use virtualenv
    if os.path.exists(os.path.join(BASEDIR, 'venv')):
        sys.path.append(os.path.join(BASEDIR, 'venv', 'bin'))
        import activate_this
        try:
            import requests
        except ImportError:
            missing_request=True
    else:
        missing_request=True

if missing_request:
    print('Cannot find requests library. Please install it, its awesome. Aborting.', file=sys.stderr)
    sys.exit(1)


class WebServiceCli:

    @staticmethod
    def set_up_cache_dir():
        homedir = os.path.expanduser('~/.ws/cache/services')
        os.makedirs(homedir, exist_ok=True)

    @staticmethod
    def valid_service_name(service_name):
        return bool(re.match(r'[a-z0-9_-]+\/[a-z0-9_-]+', service_name))

    def __init__(self, name):
        if not self.valid_service_name(name):
            raise Exception('Invalid service name: "{}"'.format(name))
        self.name = name
        self.description = self.get_service_description(self.name)

    @staticmethod
    def get_service_description(service_name, use_cache=True):
        """
        Obtain json file with service description.
        Return parsed data.
        """
        cached_name = os.path.expanduser('~/.ws/cache/services/' + service_name + '.json')
        if os.path.exists(cached_name):
            with open(cached_name) as cached_file:
                data = json.load(cached_file)
                return data

        url = os.path.join(SERVICE_DIRECTORY, service_name + '.json')
        response = requests.get(url)
        if not response.ok:
            raise Exception('Command error: '+ response.reason)
        raw = requests.get(url).content.decode('utf8')
        data = json.loads(raw)
        os.makedirs(os.path.dirname(cached_name), exist_ok=True)
        with open(cached_name, 'w') as cached_file:
            cached_file.write(raw)
        return data

    def _call_http_get(self, command, params, files=None):
        url = 'http://{}'.format(self.description['uri']['http/GET'])
        get_params={
            'command': command,
        }
        if params:
            get_params['arg'] = params
        response = requests.get(url, params=get_params)
        return response.content

    def _call_http_post(self, command, params, files=None):
        url = 'http://{}'.format(self.description['uri']['http/POST'])
        post_params={
            'command': command,
        }
        if params:
            post_params['arg'] = params
        response = requests.post(url, params=post_params, files=files)
        return response.content

    def call(self, command, params, files=None):
        for protocol in self.description['protocols']:
            if protocol == 'http/GET':
                if files: #can't send files via GET request
                    continue
                else:
                    return self._call_http_get(command, params, files=files)
            elif protocol == 'http/POST':
                return self._call_http_post(command, params, files=files)
        raise(Exception('None of service protocols is known: {}'.format(self.description['protocols'])))


def extract_params():
    """
    :returns: tuple(ws_params, service_name_and_params) with two lists
    """
    cmd_args = []
    remaining_args = sys.argv[1:]
    while remaining_args:
        arg = remaining_args.pop(0)
        if arg in ('-h', '--help', '-l', '--list-services', '-v', '--verbose'):
            cmd_args.append(arg)
        #elif arg in ('--search',):
        #    my_args.append(arg)
        #    if len(all_args) > 1:
        #        my_args.append(all_args.pop(0))
        #    else:
        #        break
        elif arg in ('-f', ):
            cmd_args.append(arg)
            if len(remaining_args) == 0:
                break
            elif len(remaining_args) == 1:
                cmd_args.append(remaining_args.pop(0))
                break
            else:
                cmd_args.append(remaining_args.pop(0))
                cmd_args.append(remaining_args.pop(0))
        else:
            remaining_args.insert(0, arg)
            break
    return (cmd_args, remaining_args)



def run():
    cmd_args, service_args = extract_params()

    parser = argparse.ArgumentParser(description='ws')
    parser.add_argument('-l', '--list-services',  dest='list_services', action='store_true',
                        help='display list of available services')
    parser.add_argument('-v', '--verbose',  dest='verbose', action='store_true',
                        help='be verbose')
    parser.add_argument('-f', '--file',  dest='file', nargs=2, action='append',
                        help='send file')
    #parser.add_argument('--seach',  dest='search',
    #                    help='search services')
    #TODO: handle loading files (-f reference_name path)
    cmd_args = parser.parse_args(args=cmd_args)
    if not service_args or not WebServiceCli.valid_service_name(service_args[0]):
        print('Service name is missing or invalid', file=sys.stderr)
        sys.exit(2)
    if len(service_args) < 2:
        print("No arguments passed to service. I don't know what to do.", file=sys.stderr)
        sys.exit(3)
    files = []
    if cmd_args.file:
        for remotename, localname in cmd_args.file:
            if localname == '-':
                fileobj = sys.stdin
            else:
                fileobj = open(localname)
            files.append((remotename, fileobj))
    service_name = service_args[0]
    service_command = service_args[1]
    service_command_args = service_args[2:]
    WebServiceCli.set_up_cache_dir()
    wscli = WebServiceCli(service_name)
    result = wscli.call(service_command, service_command_args, files=files)
    os.write(sys.stdout.fileno(), result)


if __name__ == '__main__':
    run()
