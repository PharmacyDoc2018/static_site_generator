import unittest

from textnode import TextNode
from ssg_functions import split_nodes_delimiter


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_eq_bold_middle(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", "text")
        split_node = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(split_node[0].text_type, "text")
        self.assertEqual(split_node[1].text_type, "bold")

    def test_eq_bold_start(self):
        node = TextNode("**The start of this** message is bold", "text")
        split_node = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(split_node[0].text_type, "bold")
        self.assertEqual(split_node[1].text_type, "text")
        self.assertNotEqual(split_node[0].text, "")

    def test_eq_bold_end(self):
        node = TextNode("The end of this message is **bold**", "text")
        split_node = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(split_node[0].text_type, "text")
        self.assertEqual(split_node[1].text_type, "bold")
        self.assertNotEqual(split_node[1].text, "")

    def test_eq_italic(self):
        node = TextNode("This is text with an *italic phrase* in the middle", "text")
        split_node = split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(split_node[0].text_type, "text")
        self.assertEqual(split_node[1].text_type, "italic")
        
        node = TextNode("*Italic* part at the start this time", "text")
        split_node = split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(split_node[0].text_type, "italic")
        self.assertEqual(split_node[1].text_type, "text")
        self.assertNotEqual(split_node[0].text, "")

        node = TextNode("This time the last word is *italic*", "text")
        split_node = split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(split_node[0].text_type, "text")
        self.assertEqual(split_node[1].text_type, "italic")
        self.assertNotEqual(split_node[1].text, "")
        
    def test_multinodes(self):
        nodes = [
            TextNode("**Boldly** we are starting", "text"),
            TextNode("Then we will have a **bold** and *italic* to see it find the **bold**", "text"),
            TextNode("This one will just return as is", "text"),
            TextNode("This on will also return but has an *italic* character", "text"),
            TextNode("How will it handle **bold** and url?", "text", "www.google.com")
        ]
        split_node = split_nodes_delimiter(nodes, "**", "bold")
        self.assertEqual(split_node[0].text_type, "bold")
        self.assertEqual(split_node[3].text_type, "bold")