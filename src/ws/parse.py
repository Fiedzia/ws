from .tokenize import TokenType


class Command:
    """
    Command definition
    """
    name = ''
    aliases = ()
    description = ''  # one-line description

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

    def argument_definition(self):
        return None

    def run(self):
        if self.command:
            return self.command.run()
        raise NotImplementedError

    def is_valid_flag(self, token):
        flags = self.available_flags()
        for flag in flags:
            if token.text.startswith('--') and flag.longname == token.text[2:]:
                return flag
            elif token.text.startswith('-') and flag.shortname == token.text[1:]:
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

    def get_command(self, cmdname):
        """
        return Command class if cmd represents valid command name,
        otherwise return None
        """
        for cmd in self.available_commands():
            if cmd.name == cmdname or cmdname in cmd.aliases:
                return cmd
        return None

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
        also set tokentype on all parsed tokens
        """
        _tokens = tokens[:]
        while _tokens:
            token = _tokens[0]
            if token.text.startswith('-'):
                flag = self.is_valid_flag(token)
                if flag:
                    self.flags[flag.canonical] = True
                    token.tokentype = TokenType.Flag
                    _tokens.pop(0)
                    continue

                if len(_tokens) > 1:
                    option = self.is_valid_option(_tokens[0].text, _tokens[1].text)
                    if option:
                        self.options[option.canonical] = _tokens[1].text
                        _tokens[0].tokentype = TokenType.OptionName
                        _tokens[1].tokentype = TokenType.OptionValue
                        _tokens.pop(0)
                        _tokens.pop(0)
                        continue
                else:
                    raise Exception('missing option value')
            else:
                command = self.get_command(token.text)
                if command:
                    self.command = command(self)
                    token.tokentype = TokenType.Command
                    _tokens.pop(0)
                    self.command.parse(_tokens)
                    return
                elif self.argument_definition():
                    arg_def = self.argument_definition()
                    if arg_def.min_amount:
                        if len(_tokens) < arg_def.min_amount:
                            raise Exception('Not enough arguments. Expected at least {}, got {}'.format(arg_def.min_amount, len(_tokens)))
                    if arg_def.max_amount:
                        argument_tokens = _tokens[:arg_def.max_amount]
                    else:
                        argument_tokens = _tokens[:]
                    for argument_token in argument_tokens:
                        argument_token.tokentype = TokenType.Argument
                        _tokens.pop(0)
                    self.arguments = [argument_token.text for argument_token in argument_tokens]
                if _tokens:
                    self.parse_unknown(_tokens)
                    _tokens.clear()
        # check if there are any missing required options or arguments
        for option in self.available_options():
            if option.required and option.canonical not in self.options:
                raise Exception('required option missing: ' + option.canonical)
        if self.argument_definition() and self.argument_definition().min_amount is not None:
            if not self.arguments:
                raise Exception('Command {} is missing required arguments.'.format(self.name))


class Flag:
    def __init__(self, shortname, longname, canonical=None, default=False, help=None, description=None):
        self.shortname = shortname
        self.longname = longname
        self.canonical = canonical or self.longname or self.shortname
        self.default = default
        self.help = help
        self.description = description


class Option:
    def __init__(self, shortname, longname, canonical=None, default=None, help=None, description=None, type=str, required=False):
        self.shortname = shortname
        self.longname = longname
        self.canonical = canonical or self.longname or self.shortname
        self.default = default
        self.help = help
        self.description = description
        self.type = type
        self.required = required


class ArgumentDefinition:
    def __init__(self, help=None, description=None, min_amount=None, max_amount=None):
        self.help = help
        self.description = description
        self.min_amount = min_amount
        self.max_amount = max_amount


class Result:
    """
    Command result
    """
    def __init__(self, value):
        """
        value can be one of:
            string
            bytes
            generator returning strings or bytes
        """
        pass
