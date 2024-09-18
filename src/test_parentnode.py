import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class ParentLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_double_inseption(self):
        
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode("p", [LeafNode("b", "Bold text"), LeafNode("i", "italic text")]),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
    
    def test_to_html_double_inseption_with_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode("p", [LeafNode("b", "Bold text"), LeafNode("a", "click here!", {"href": "www.google.com"})]),
                LeafNode("i", "italic text"),
                ParentNode("p", [LeafNode("b", "Bold text"), LeafNode("i", "italic text")]),
                LeafNode(None, "Normal text"),
            ],
        )
        
        