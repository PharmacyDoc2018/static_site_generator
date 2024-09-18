import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("a", "Click here!", {"href": "www.google.com"})
        self.assertEqual(node.to_html(), '<a href="www.google.com">Click here!</a>')

    def test_value_required(self):
        #node = LeafNode("p", None, {"href": "www.google.com"})
        self.assertRaises(ValueError, LeafNode, "p", None)

    def test_no_children(self):
        node = LeafNode("a", "Click here!", {"href": "www.google.com"})
        self.assertEqual(node.children, None)