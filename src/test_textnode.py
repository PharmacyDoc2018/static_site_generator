import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode("This is another text node", "italic", "www.boot.dev")
        node2 = TextNode("This is another text node", "italic", "www.boot.dev")
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is some text", "bold")
        node2 = TextNode("This is not the same text", "bold")
        self.assertNotEqual(node, node2)

    def test_text_type_not_eq(self):
        node = TextNode("This is some text", "bold")
        node2 = TextNode("This is some text", "italic")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()