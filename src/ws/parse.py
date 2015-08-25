class Command:

    NAME = None

    def __init__(self, parent, flags=None, options=None, arguments=None, command=None):
        self.parent = parent
        self.flags = flags or {}
        self.options = options or {}
        self.arguments = arguments or []
        self.command = command
        for flag in self.available_flags():
            self.flags[flag.canonical] = flag.default
        for option in self.available_options():
            self.options[option.canonical] = option.default

    def help(self):
        pass

    def available_commands(self):
        return []

    def available_flags(self):
        return []

    def available_options(self):
        return []

    def argument_info(self):
        return None

    def run(self):
        raise NotImplementedError

    def is_valid_flag(self, token):
        flags = self.available_flags()
        for flag in flags:
            if token.startswith('--') and flag.longname == token[2:]:
                return flag
            elif token.startswith('-') and flag.shortname == token[1:]:
                return flag
        return False

    def is_valid_option(self, name, value):
        # TODO: add option value validation
        options = self.available_options()
        for option in options:
            if name.startswith('--') and option.longname == name[2:]:
                return option
            elif name.startswith('-') and option.shortname == name[1:]:
                return option
        return False

    def parse_unknown(self, tokens):
        """
        Fallback for parsing tokens not recognized as flags/commands/arguments/commands
        You can use it to delegate parsing
        """
        raise Exception('leftovers')

    def parse(self, tokens):
        """
        set options, flags, arguments and command according to own specification
        or raise an InvalidInput exception
        """
        _tokens = tokens[:]
        while _tokens:
            token = _tokens[0]
            if token.startswith('-'):
                flag = self.is_valid_flag(token)
                if flag:
                    self.flags[flag.canonical] = True
                    _tokens.pop(0)
                    continue

                if len(_tokens) > 1:
                    option = self.is_valid_option(_tokens[0], _tokens[1])
                    if option:
                        self.options[option.canonical] = _tokens[1]
                        _tokens.pop(0)
                        _tokens.pop(0)
                        continue
                else:
                    raise Exception('missing option value')
            else:
                command = self.is_valid_command(token)
                if command:
                    self.command = command(self)
                    _tokens.pop(0)
                    command.parse(_tokens)
                    continue
                #elif self._argument_info():
                #    #handle arguments
                self.parse_unknown(_tokens)


class Flag:
    def __init__(self, shortname, longname, canonical=None, default=False, help=None, description=None):
        self.shortname = shortname
        self.longname = longname
        self.canonical = canonical
        self.canonical = self.canonical or self.longname or self.shortname
        self.default = default
        self.help = help
        self.description = description


class Option:
    def __init__(self, shortname, longname, canonical=None, default=None, help=None, description=None, type=str, required=False):
        self.shortname = shortname
        self.longname = longname
        self.canonical = self.canonical or self.longname or self.shortname
        self.default = default
        self.help = help
        self.description = description
        self.type = type
        self.require = required


class ArgumentDescription:
    def __init__(self, help=None, description=None, amount=None, require=False):
        self.help = help
        self.description = description
        self.amount = amount
        self.require = require
