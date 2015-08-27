from .parse import Command


class Dummy:
    pass


class Service(Command):

    """
    Base class for all services
    """

    def __init__(self, env, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.meta = Dummy()
        self.env = env
