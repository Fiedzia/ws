import os

from importlib import import_module

from ws.service_utils import Service


class ServiceManager:
    """
    Handle service loading and discovery
    """

    def load_service_module(self, service_name):
        return import_module('ws.services.{}.service'.format(service_name))

    def load_service(self, service_name):
        service_module = self.load_service_module(service_name)
        if hasattr(service_module, 'SERVICE'):
            return getattr(service_module, 'SERVICE')
        else:
            for item in dir(service_module):
                obj = getattr(service_module, item)
                if issubclass(obj, Service):
                    return obj
        raise Exception('Service not found: ' + service_name)

    def has_service(self, service_name):
        if service_name in self.service_dict:
            return True
        elif os.path.exists(os.path.join(os.path.dirname(__file__), service_name)):
            return True
        return False

    def all_services(self):
        return []

    def get_service(self, service_name):
        if service_name in self.service_dict:
            return self.service_dict[service_name]
        else:
            service = self.load_service(service_name)
            self.service_dict[service_name] = service
            return service

    def __init__(self):
        self.service_dict = {}
