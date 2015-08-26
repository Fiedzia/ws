from parse import Command
from utils import quit


class Quit(Command):
    name = ':quit'
    aliases = (':q',)
    description = 'quit ws'

    def run(self):
        quit()


class Help(Command):
    name = ':help'
    description = 'display help info'


class Alias(Command):
    name = ':alias'
    description = ''


class BinAlias(Command):
    name = ':binalias'


class Commands(Command):
    name = ':commands'

    def run(self):
        commands = self.parent.available_commands()
        commands.sort(key=lambda cmd: cmd.name)
        for command in commands:
            print(command.name, command.description)
