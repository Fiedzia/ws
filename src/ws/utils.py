import sys


def quit(msg='Bye', exitcode=0):
    """
    Terminate application.
    :param msg: message to print.
    :param exitcode: process exit code

    if exitcode is 0, msg will be printed to stdout,
    otherwise to stderr.
    """
    if msg:
        if exitcode != 0:
            print(msg, file=sys.stderr)
        else:
            print(msg)
    sys.exit(exitcode)
