import unittest

from textnode import TextNode
from ssg_functions import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_eq(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes[0].text_type, "text")
        self.assertEqual(nodes[1].text_type, "bold")
        self.assertEqual(nodes[2].text_type, "text")
        self.assertEqual(nodes[3].text_type, "italic")
        self.assertEqual(nodes[4].text_type, "text")
        self.assertEqual(nodes[5].text_type, "code")
        self.assertEqual(nodes[6].text_type, "text")
        self.assertEqual(nodes[7].text_type, "image")
        self.assertEqual(nodes[8].text_type, "text")
        self.assertEqual(nodes[9].text_type, "link")