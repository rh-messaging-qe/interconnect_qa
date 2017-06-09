import configparser
import itertools
import collections


class Topology(object):
    def __init__(self, brokers=None, routers=None, facades=None, senders=None, receivers=None, indifferent=None,
                 structural=None):
        self.brokers = brokers
        self.routers = routers
        self.facades = facades
        self.senders = senders
        self.receivers = receivers
        self.indifferent = indifferent
        self.structural = structural

    def __cmp__(self, other):
        if self.brokers == other.brokers and self.routers == other.routers and self.facades == other.facades and \
                self.senders == other.senders and self.receivers == other.receivers and self.indifferent == other.indifferent and \
                self.structural == other.structural:
            return True
        return False

    def __eq__(self, other):
        if self.brokers == other.brokers and self.routers == other.routers and self.facades == other.facades and \
                self.senders == other.senders and self.receivers == other.receivers and self.indifferent == other.indifferent and \
                self.structural == other.structural:
            return True
        return False


class TopologyDesigner(object):
    BROKER_SECTION = "BROKERS"
    ROUTERS_SECTION = "ROUTERS"
    SENDERS_SECTION = "SENDERS"
    RECEIVERS_SECTION = "RECEIVERS"
    FACADES_SECTION = "FACADES"
    INDIFFERENT_SECTION = "INDIFFERENT"
    STRUCTURAL_SECTION = "STRUCTURAL"

    def __init__(self, file):
        self._parsed_data = self.__read_file(file)
        self.brokers = self._get_brokers()
        self.routers = self._get_routers()
        self.senders = self._get_senders()
        self.receivers = self._get_receivers()
        self.facades = self._get_facades()
        self.indifferent = self._get_indifferent()  # ones that can be shutdown and do not influence flow of messages
        self.structural = self._get_structural()  # ones that after a shutdown do influence flow of messages
        self.permutated_brokers = self._get_perm_(self.brokers)
        self.permutated_routers = self._get_perm_(self.routers)
        self.permutated_facades = self._get_perm_(self.facades)
        self.permutated_senders = self._get_perm_(self.senders)
        self.permutated_receivers = self._get_perm_(self.receivers)
        self.permutated_indifferent = self._get_perm_(self.indifferent)
        self.permutated_structural = self._get_perm_(self.structural)
        self.topologies = self._generate_topologies()

    def _get_perm_(self, items=[]):
        if items is not None:
            return list(itertools.permutations(items, len(items)))  # iterator is destroyed after the call
        return None

    def __read_file(self, file):
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(file)
        return parser

    def __get_data_section(self, section):
        try:
            data = self._parsed_data[section]
            data = list(data)
        except KeyError:
            data = None
        return data

    def _get_brokers(self):
        return self.__get_data_section(self.BROKER_SECTION)

    def _get_routers(self):
        return self.__get_data_section(self.ROUTERS_SECTION)

    def _get_senders(self):
        return self.__get_data_section(self.SENDERS_SECTION)

    def _get_receivers(self):
        return self.__get_data_section(self.RECEIVERS_SECTION)

    def _get_facades(self):
        return self.__get_data_section(self.FACADES_SECTION)

    def _get_indifferent(self):
        return self.__get_data_section(self.INDIFFERENT_SECTION)

    def _get_structural(self):
        return self.__get_data_section(self.STRUCTURAL_SECTION)

    def __generate_map(self, product=[], t_map={}):
        product = list(product)
        p_map = {}
        for name in t_map:
            if t_map[name] is not False:
                p_map[name] = product.pop()
        assert product == []
        return p_map

    def _generate_topologies(self):
        topologies = []
        t_map = collections.OrderedDict((
            ("structural", False if self.permutated_structural is None else True),
            ("indifferent", False if self.permutated_indifferent is None else True),
            ("receivers", False if self.permutated_receivers is None else True),
            ("senders", False if self.permutated_senders is None else True),
            ("facades", False if self.permutated_facades is None else True),
            ("routers", False if self.permutated_routers is None else True),
            ("brokers", False if self.permutated_brokers is None else True)
        ))
        partial_product_list = [
            self.permutated_brokers, self.permutated_routers, self.permutated_facades,
            self.permutated_senders, self.permutated_receivers,
            self.permutated_indifferent, self.permutated_structural]
        partial_product_list = filter(lambda x: x is not None, partial_product_list)  # returns iterator!!!!

        for topology in itertools.product(*partial_product_list):
            # topologies.append(Topology(*topology)) #this won't work correctly because sections can be empty = None
            p_map = self.__generate_map(topology, t_map)
            topologies.append(Topology(**p_map))

        return topologies
