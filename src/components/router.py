from src.components import *

from sultan.api import Sultan

from src.components.node import Node


class Router(Node):
    def __init__(self, hostname="localhost", configuration=None, configuration_path=DEFAULT_CONFIG_PATH):
        super(Router, self).__init__(hostname)
        self.configuration = configuration
        self.configuration_path = configuration_path
        self.sultan = Sultan()

    def start(self):
        self.sultan.qdrouterd.run("-c %s -d" % self.configuration_path)
