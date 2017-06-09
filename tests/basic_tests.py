import pytest


def test_send_receive(in_node, out_node, sender_node, receiver_node):
    # if in_node pytest.skip
    sender_node.send(in_node)
    receiver_node.receive(out_node)
    assert sender_node.last_message == receiver_node.last_message
