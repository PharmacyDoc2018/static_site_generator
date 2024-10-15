import unittest

from ssg_functions import markdown_to_html_node

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_all(self):
        markdown = """# This is a heading

                        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                        * This is the first list item in a list block
                        * This is a list item
                        * This is another list item

                        1. one
                        2. two
                        3. three

                        This is text with a link [to boot dev](https://www.boot.dev)

                        This is an image ![Tree Pic](/tree.png)"""
        #print(markdown_to_html_node(markdown))