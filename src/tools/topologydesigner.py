import configparser
import itertools
import collections


class Topology(object):
    """
    Topology in this context is a unique combination of all nodes of different types (routers, brokers ...)
    It is an exact map for specific scenario, Topology is a unique in every case. This means that
    when a test is run there is no possibility tu have a redundant message flow for two different test runs
    """

    def __init__(self, brokers=None, routers=None, facades=None, senders=None, receivers=None, indifferent=None,
                 structural=None):
        self.brokers = brokers
        self.routers = routers
        self.facades = facades
        self.senders = senders
        self.receivers = receivers
        self.indifferent = indifferent  # nodes which can be shut down or restarted and it won't influence stability of a network
        self.structural = structural  # nodes which are crucial for a network stability, failure of one of these would invalidate whole network

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
    """
    TopologyDesigner is simply said a factory for non-redundant list of topologies.
    The whole idea is that written QA tests should be scalable. It means e.g. send & receive
    test should work same on topology with 1 node or with 10 nodes without any code change or execution redefinition.
    Designer makes top-down look on such topology and its partial inputs are provided in the logical execution sequence to the
    pytest test.
    Note:
        For better idea what TopologyDesigner should do, see provided unit tests
    """
    # Sequence of sections in the document needs to be the same as listed
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
        self.topologies = self._generate_topologies()  # list of topologies, from a topology is possible to get in_node out_node etc ...

    def _get_perm_(self, items=[]):  # return all permutations for specific list of items
        """
        :param items: list of hostnames, ip addresses etc. Necessary for different positions of nodes in the topology
        :return: list if lists
        :rtype: list
        """
        if items is not None:
            return list(itertools.permutations(items, len(items)))  # iterator is destroyed after the call
        return None

    def __read_file(self, file):
        parser = configparser.ConfigParser(
            allow_no_value=True)  # it accepts empty fields (e.g. missing BROKERS section)
        parser.read(file)
        return parser

    def __get_data_section(self, section):  # gets a specific section from the input file
        """
        :param section: name of the section to parse
        :type section: str
        :return: parsed data
        :rtype: list | None
        """
        try:
            data = self._parsed_data[section]
            data = list(data)
        except KeyError:  # there is no such section, no data are provided
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
        """
        :param product: sequence from cartesian product of different sections data are provided as [[x1,x2], [y1,y2,y3], ...]
        :type product: iterator of lists
        :param t_map: a template which indicates which sections are and aren't actively used for a particular configuration
        :type t_map: dict
        :return: dictionary with keys from t_map and filled data from product list
        """
        product = list(product)  # THIS is very important in python 3 (everywhere are iterators)
        p_map = {}
        for name in t_map:
            if t_map[name] is not False:  # again, we nee to have all ordered, otherwise XXX if statements would occur
                p_map[name] = product.pop()  # this section is used, so pop it up
        assert product == []  # if there is something left, we have a serious bug here mate
        return p_map

    def _generate_topologies(self):
        """
        Generates all topologies from the file provided during TopologyDesigner initialization
        :return: list of topologies
        :rtype: list
        """
        topologies = []
        # t_map is dictionary (ordered!!) with mapped sections and its data, by default t_map contains information if
        # mentioned section (key) is used or not, if it is used, later in the code it is used as a template
        # meaning -> it kills two flies by one hand. there is a meta information together with section name and values together at once
        # this does not mean it should not be revisited or done differently, concept is hardly understandable to speak the truth
        t_map = collections.OrderedDict((
            ("structural", False if self.permutated_structural is None else True),
            ("indifferent", False if self.permutated_indifferent is None else True),
            ("receivers", False if self.permutated_receivers is None else True),
            ("senders", False if self.permutated_senders is None else True),
            ("facades", False if self.permutated_facades is None else True),
            ("routers", False if self.permutated_routers is None else True),
            ("brokers", False if self.permutated_brokers is None else True)
        ))
        # partial_product_list is a list of all permuted values for every available section from the provided file
        partial_product_list = [
            self.permutated_brokers, self.permutated_routers, self.permutated_facades,
            self.permutated_senders, self.permutated_receivers,
            self.permutated_indifferent, self.permutated_structural]
        # filter all none value fields -- THIS is why we need order in section and ordered dictionary, we need to know which parts
        # were filtered to skip numerous if statements later
        partial_product_list = filter(lambda x: x is not None, partial_product_list)  # returns iterator!!!!

        # to better understand this section about products, see test_topology_designer_generate_topologies_router_broker in test_topology.py
        for topology in itertools.product(
                *partial_product_list):  # cartesian product - mind we need to pass lists as separate parameters --> see '*' before parameter
            # topologies.append(Topology(*topology)) #this won't work correctly because sections can be empty = None
            p_map = self.__generate_map(topology, t_map)
            # AGAIN!! note '**' .. we are giving a dictionary - means there are passed values x=y as parameters!!! This is why we need t_map dict too
            topologies.append(Topology(**p_map))

        return topologies
