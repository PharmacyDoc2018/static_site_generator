import unittest

from ssg_functions import extract_markdown_images, extract_markdown_links

class TestExtractLinks(unittest.TestCase):
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text)[0], ("rick roll", "https://i.imgur.com/aKaOqIh.gif"))
        self.assertEqual(extract_markdown_images(text)[1], ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"))

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text)[0], ("to boot dev", "https://www.boot.dev"))
        self.assertEqual(extract_markdown_links(text)[1], ("to youtube", "https://www.youtube.com/@bootdotdev"))

    def test_extract_images_not_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_links_not_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_links(text), [])
