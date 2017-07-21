import pytest

from src.tools.topologydesigner import TopologyDesigner, Topology


def filename(file):
    return "../test_topologies/" + file


input = [("test_topology_all.ini", ["test_broker1", "test_broker2"])]


@pytest.mark.parametrize(argnames="file, expected", argvalues=input)
def test_topology_designer_broker_section(file, expected):
    designer = TopologyDesigner(filename(file))
    assert designer.brokers == expected


input = [("test_topology_all.ini", ["test_router1", "test_router2", "test_router3", "test_router4"])]


@pytest.mark.parametrize(argnames="file, expected", argvalues=input)
def test_topology_designer_router_section(file, expected):
    designer = TopologyDesigner(filename(file))
    assert designer.routers == expected


input = [("test_topology_all.ini", ["test_router2"])]


@pytest.mark.parametrize(argnames="file, expected", argvalues=input)
def test_topology_designer_facades_section(file, expected):
    designer = TopologyDesigner(filename(file))
    assert designer.facades == expected


input = [("test_topology_all.ini", ['s1'])]


@pytest.mark.parametrize(argnames="file, expected", argvalues=input)
def test_topology_designer_senders_section(file, expected):
    designer = TopologyDesigner(filename(file))
    assert designer.senders == expected


input = [("test_topology_all.ini", ['r1'])]


@pytest.mark.parametrize(argnames="file, expected", argvalues=input)
def test_topology_designer_receivers_section(file, expected):
    designer = TopologyDesigner(filename(file))
    assert designer.receivers == expected


input = [("test_topology_all.ini", ["test_router2", "test_router4"])]


@pytest.mark.parametrize(argnames="file, expected", argvalues=input)
def test_topology_designer_indifferent_section(file, expected):
    designer = TopologyDesigner(filename(file))
    assert designer.indifferent == expected


input = [("test_topology_all.ini", ["test_router1", "test_router3"])]


@pytest.mark.parametrize(argnames="file, expected", argvalues=input)
def test_topology_designer_structural_section(file, expected):
    designer = TopologyDesigner(filename(file))
    assert designer.structural == expected


product = [
    Topology(brokers=('test_broker1', 'test_broker2'), routers=('test_router1', 'test_router2', 'test_router3')),
    Topology(brokers=('test_broker1', 'test_broker2'), routers=('test_router1', 'test_router3', 'test_router2')),
    Topology(brokers=('test_broker1', 'test_broker2'), routers=('test_router2', 'test_router1', 'test_router3')),
    Topology(brokers=('test_broker1', 'test_broker2'), routers=('test_router2', 'test_router3', 'test_router1')),
    Topology(brokers=('test_broker1', 'test_broker2'), routers=('test_router3', 'test_router1', 'test_router2')),
    Topology(brokers=('test_broker1', 'test_broker2'), routers=('test_router3', 'test_router2', 'test_router1')),
    Topology(brokers=('test_broker2', 'test_broker1'), routers=('test_router1', 'test_router2', 'test_router3')),
    Topology(brokers=('test_broker2', 'test_broker1'), routers=('test_router1', 'test_router3', 'test_router2')),
    Topology(brokers=('test_broker2', 'test_broker1'), routers=('test_router2', 'test_router1', 'test_router3')),
    Topology(brokers=('test_broker2', 'test_broker1'), routers=('test_router2', 'test_router3', 'test_router1')),
    Topology(brokers=('test_broker2', 'test_broker1'), routers=('test_router3', 'test_router1', 'test_router2')),
    Topology(brokers=('test_broker2', 'test_broker1'), routers=('test_router3', 'test_router2', 'test_router1'))
]
input = [("test_topology_combinations_1.ini", product)]


@pytest.mark.parametrize(argnames="file, expected", argvalues=input)
def test_topology_designer_generate_topologies_router_broker(file, expected):
    designer = TopologyDesigner(filename(file))
    assert designer.topologies == expected


product = [
    Topology(routers=('127.0.0.1', '127.0.0.2', '127.0.0.3'), senders=("127.0.0.2",), receivers=("127.0.0.3",)),
    Topology(routers=('127.0.0.1', '127.0.0.3', '127.0.0.2'), senders=("127.0.0.2",), receivers=("127.0.0.3",)),
    Topology(routers=('127.0.0.2', '127.0.0.1', '127.0.0.3'), senders=("127.0.0.2",), receivers=("127.0.0.3",)),
    Topology(routers=('127.0.0.2', '127.0.0.3', '127.0.0.1'), senders=("127.0.0.2",), receivers=("127.0.0.3",)),
    Topology(routers=('127.0.0.3', '127.0.0.1', '127.0.0.2'), senders=("127.0.0.2",), receivers=("127.0.0.3",)),
    Topology(routers=('127.0.0.3', '127.0.0.2', '127.0.0.1'), senders=("127.0.0.2",), receivers=("127.0.0.3",))
]
input = [("test_topology_combinations_2.ini", product)]


@pytest.mark.parametrize(argnames="file, expected", argvalues=input)
def test_topology_designer_generate_topologies_router_broker(file, expected):
    designer = TopologyDesigner(filename(file))
    assert designer.topologies == expected
