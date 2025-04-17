import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_tag_eq(self):
        node = HTMLNode("div")
        node2 = HTMLNode("div")
        self.assertEqual(node.tag, node2.tag)

    def test_tag_diff(self):
        node = HTMLNode("div")
        node2 = HTMLNode("p")
        self.assertNotEqual(node.tag, node2.tag)

    def test_value_eq(self):
        node = HTMLNode("div","This is some text")
        node2 = HTMLNode("div","This is some text")
        self.assertEqual(node.value, node2.value)

    def test_value_diff(self):
        node = HTMLNode("div","This is some text")
        node2 = HTMLNode("div","This is some different text")
        self.assertNotEqual(node.value, node2.value)

    def test_props_to_html(self):
        tst_prop = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("div","This is some text", None, tst_prop)
        prop_str = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), prop_str)