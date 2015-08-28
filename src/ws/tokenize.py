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

    def __init__(self, text, position, tokentype=TokenType.Unknown):
        self.text = text
        self.tokentype = tokentype
        self.position = position


def tokenize(text):
    """
    Split text into tokens
    """
    tokens = []
    if not text:
        return tokens
    in_space = text[0].isspace()
    start = 0
    for idx, ch in enumerate(text):
        if ch.isspace() != in_space:
            if not in_space:
                tokens.append(Token(text[start:idx], start))
            in_space = ch.isspace()
            start = idx
    if not in_space:
        tokens.append(Token(text[start:], start))
    # TODO: handle quotes and double quotes and escape sequences
    return tokens
