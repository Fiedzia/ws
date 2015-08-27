#!/usr/bin/env python3
import sys

from ws import WsCommand
from ws.services import ServiceManager
from ws.tokenize import Token


def run():
    service_manager = ServiceManager()
    wscmd = WsCommand(parent=None, service_manager=service_manager)
    wscmd.parse(list(map(Token, sys.argv[1:])))
    wscmd.run()


if __name__ == '__main__':
    run()
