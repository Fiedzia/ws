#!/usr/bin/env python3
import sys

from ws import WsCommand
from ws.services import ServiceManager
from ws.tokenize import Token


def run():
    service_manager = ServiceManager()
    wscmd = WsCommand(parent=None, service_manager=service_manager)
    tokens = []
    idx = 0
    for arg in sys.argv[1:]:
        tokens.append(Token(arg, idx))
        idx += len(arg) + 1
    wscmd.parse(tokens)
    wscmd.run()


if __name__ == '__main__':
    run()
