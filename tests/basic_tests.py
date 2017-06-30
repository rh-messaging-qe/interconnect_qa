import pytest

from tests import get_func_name
from proton import Message

def test_send_receive(in_node, out_node, sender_node, receiver_node):
    message = Message()
    sender_node.send(node=in_node, address=get_func_name(), messages=[message])
    receiver_node.receive(node=out_node, address=get_func_name())
    assert sender_node.last_message._get_id() == receiver_node.last_message._get_id()
