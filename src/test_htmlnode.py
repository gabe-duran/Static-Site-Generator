import unittest

from htmlnode import HTMLNode,LeafNode

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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_title(self):
        node = LeafNode("title", "Hello, world!")
        self.assertEqual(node.to_html(), "<title>Hello, world!</title>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")