import unittest

from ssg_functions import block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), "heading")
        block = "###### This is also a heading"
        self.assertEqual(block_to_block_type(block), "heading")

    def test_code(self):
        block = "```Here is some code```"
        self.assertEqual(block_to_block_type(block), "code")
        block = "``` will spaces mess it up? ```"
        self.assertEqual(block_to_block_type(block), "code")