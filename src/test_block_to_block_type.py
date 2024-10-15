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

    def test_quote(self):
        block = ">To be or not to be"
        self.assertEqual(block_to_block_type(block), "quote")
        block = ">To be or not to be\n>That is the question"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_unordered_list(self):
        block = "* list item in no particular order"
        self.assertEqual(block_to_block_type(block), "unordered_list")
        block = "* list item in no particular order\n* second item in the list"
        self.assertEqual(block_to_block_type(block), "unordered_list")
        block = "*invalid unordered list attempt"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_ordered_list(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), "ordered_list")
        block = "1. one\n3. three\n 2. two"
        self.assertEqual(block_to_block_type(block), "paragraph")