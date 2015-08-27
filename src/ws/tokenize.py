from enum import Enum

class TokenType(Enum):
    Flag = 1
    OptionName = 2
    OptionValue = 3
    Command = 4
    Service = 5
    Argument = 6
    Unknown = 7  # default value
    Invalid = 8  # this means unrecognized token


class Token:

    def __init__(self, text, tokentype=TokenType.Unknown):
        self.text = text
        self.tokentype = tokentype


def tokenize(text):
    """
    Split text into tokens
    """
    # TODO: handle quotes and double quotes
    return [Token(t) for t in text.strip().split()]
