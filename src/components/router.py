from src.components import *

from sultan.api import Sultan

from src.components.node import Node


class Router(Node):
    def __init__(self, configuration=None, configuration_path=DEFAULT_CONFIG_PATH):
        self.configuration = configuration
        self.configuration_path = configuration_path
        self.sultan = Sultan()

    def start(self):
        self.sultan.qdrouterd.run("-c %s -d" % self.configuration_path)
