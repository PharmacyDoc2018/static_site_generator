import unittest

from textnode import TextNode
from ssg_functions import split_nodes_link

class TestSplitLinkNodes(unittest.TestCase):
    def test_simple(self):
        node = TextNode(
            "This is text with an link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            "text",
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes[0].text_type, "text")
        self.assertEqual(new_nodes[1].text_type, "link")
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[2].text_type, "text")
        self.assertEqual(new_nodes[3].text_type, "link")
        self.assertEqual(new_nodes[3].url, "https://www.youtube.com/@bootdotdev")

    def test_complex(self):
        old_nodes = [
            TextNode("This is text with an link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)","test"),
            TextNode("This is only plain text", "text"),
            TextNode("[link at start](www.starting_link.com) lets see what happens", "text"),
            TextNode("lastly a middle link [middle link](www.middle.com) right in the middle", "text")
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes[1].text_type, "link")
        self.assertEqual(new_nodes[3].text_type, "link")
        self.assertEqual(new_nodes[4].text_type, "text")
        self.assertEqual(new_nodes[5].text_type, "link")
