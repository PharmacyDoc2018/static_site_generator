import unittest

from textnode import TextNode
from leafnode import LeafNode
from ssg_functions import text_node_to_html_node


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_eq(self):
        text_node = TextNode("This is a text block", "text")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "This is a text block")

    def test_bold_eq(self):
        text_node = TextNode("This is bold text", "bold")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>This is bold text</b>")
        
    def test_link_eq(self):
        text_node = TextNode("Click here!", "link", "www.google.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="www.google.com">Click here!</a>')
        
    def test_img_eq(self):
        text_node = TextNode("Look at these moutains!", "image", "/image/mtn.jpeg")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<img src="/image/mtn.jpeg" alt="Look at these moutains!"></img>')
        