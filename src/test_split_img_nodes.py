import unittest

from textnode import TextNode
from ssg_functions import split_nodes_image

class TestSplitImgNodes(unittest.TestCase):
    def test_simple(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            "test",
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes[0].text_type, "text")
        self.assertEqual(new_nodes[1].text_type, "image")
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[2].text_type, "text")
        self.assertEqual(new_nodes[3].text_type, "image")
        self.assertEqual(new_nodes[3].url, "https://www.youtube.com/@bootdotdev")

    def test_complex(self):
        old_nodes = [
            TextNode("This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)","test"),
            TextNode("This is only plain text", "text"),
            TextNode("![image at start](/image in your face from the start.png) lets see what happens", "text"),
            TextNode("lastly a middle pic ![middle pic](/middle.jpeg) right in the middle", "text")
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes[1].text_type, "image")
        self.assertEqual(new_nodes[3].text_type, "image")
        self.assertEqual(new_nodes[4].text_type, "text")
        self.assertEqual(new_nodes[5].text_type, "image")
