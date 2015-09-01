from .parse import Command, ArgumentDefinition
from .utils import quit


class Quit(Command):
    name = ':quit'
    aliases = (':q',)
    description = 'quit ws'

    def run(self):
        quit()


class Help(Command):
    name = ':help'
    description = 'display help info'
    aliases = (':h',)

    def argument_definition(self):
        return ArgumentDefinition(help='Show help note', max_amount=1)

    def option_help(self, option):
        line = ''
        if option.shortname:
            line += option.shortname
        else:
            line += option.longname
        line += ' ' + option.help
        line += ' defaults to: ' + option.default
        return line

    def flag_help(self, flag):
        line = ''
        if flag.shortname:
            line += flag.shortname
        else:
            line += flag.longname
        line += ' ' + flag.help
        return line

    def command_brief_help(self, command):
        line = '{}: {}'.format(command.name, command.description)
        return line

    def command_help(self, command):
        lines = []

        for flag in command.available_flags():
            lines.append(self.flag_help(flag))

        for option in command.available_options():
            lines.append(self.option_help(option))

        return '\n'.join(lines)

    def service_help(self, service):
        lines = ['{} - {}'.format(service.name, service.description)]

        for flag in service.available_flags():
            lines.append(self.flag_help(flag))

        for option in service.available_options():
            lines.append(self.option_help(option))

        for command in service.available_commands():
            command_instance = command(parent=service)
            lines.append(self.command_brief_help(command_instance))

        return '\n'.join(lines)

    def run(self):
        if not self.arguments:
            print('General help\n'
                  'type ":help cmd" to get help for specific command or service\n'
                  'type ":quit" to quit\n'
                  'type ":commands" to get list of commands\n'
                  'type ":services" to get list of services\n'
                  )
        else:
            print('Help for ' + self.arguments[0])
            if self.arguments[0].startswith(':'):
                for cmd in self.parent.available_commands():
                    if cmd.name.lower() == self.arguments[0].lower():
                        command_instance = cmd(parent=self.parent)
                        print(self.command_help(command_instance))
                        return
                print('unknown command')
            else:
                if self.parent.service_manager.has_service(self.arguments[0]):
                    service = self.parent.service_manager.get_service(self.arguments[0])(env=None)
                    print(self.service_help(service))
                else:
                    print('unknown service: {}'.format(self.arguments[0]))


class Alias(Command):
    name = ':alias'
    description = ''


class BinAlias(Command):
    name = ':binalias'


class Commands(Command):
    name = ':commands'
    description = 'list available commands'

    def argument_definition(self):
        return ArgumentDefinition(help='List only commands containing given phrase', max_amount=1)

    def run(self):
        commands = self.parent.available_commands()
        commands.sort(key=lambda cmd: cmd.name)
        if self.arguments:
            commands = [cmd for cmd in commands if self.arguments[0].lower() in cmd.name.lower()]
            print('Commands matching {}:'.format(self.arguments[0]))
        else:
            print('Available commands:')
        for command in commands:
            print('  ', command.name, command.description)


class Services(Command):
    name = ':services'
    description = 'list available services'

    def run(self):
        services = self.parent.service_manager.all_services()
        services.sort(key=lambda service: service.name)
        print('Available services:')
        for service in services:
            print('  ', service.name, service.description)

top_level_commands = [
    Quit, Help, Alias, BinAlias, Commands, Services
]
