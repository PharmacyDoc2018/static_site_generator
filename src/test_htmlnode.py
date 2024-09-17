import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_initial_space(self):
        node = HTMLNode(
            "a",
            "value text",
            ["child1", "child2"],
            {"href": "www.google.com", "target": "_blank"}
        )
        #print(node.props_to_html())
        self.assertEqual(node.props_to_html()[:1], " ")

    def test_props_to_html_eq(self):
        node = HTMLNode(
            "a",
            "value text",
            ["child1", "child2"],
            {"href": "www.google.com", "target": "_blank"}
        )
        node2 = HTMLNode(
            "a",
            "value text",
            ["child1", "child2"],
            {"href": "www.google.com", "target": "_blank"}
        )
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_correct_spaces(self):
        node = HTMLNode(
            "a",
            "value text",
            ["child1", "child2"],
            {"href": "www.google.com", "target": "_blank"}
        )
        self.assertEqual(node.props_to_html().count(" "), len(node.props.keys()))

    def test_blank_props(self):
        node = HTMLNode(
            "a",
            "value text",
            ["child1", "child2"]
        )
        self.assertEqual(node.props_to_html(), "")