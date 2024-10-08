import unittest

from ssg_functions import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def tests(self):
        s = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""

        test_blocks = markdown_to_blocks(s)
        for block in test_blocks:
            self.assertNotEqual(block,"")
            self.assertNotEqual(block[0]," ")
            self.assertNotEqual(block[-1]," ")