import unittest

from htmlnode import HTMLNode,LeafNode, ParentNode

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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_multiple_children(self):
        child_node_span = LeafNode("span", "child_span")
        child_node_bold = LeafNode("b", "child_bold")
        child_node_italic = LeafNode("i", "child_italic")
        parent_node = ParentNode("div", [child_node_span, child_node_bold, child_node_italic])
        self.assertEqual(parent_node.to_html(), "<div><span>child_span</span><b>child_bold</b><i>child_italic</i></div>")

    def test_parent_empty_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [])

    def test_parent_no_children(self):
        with self.assertRaises(TypeError):
            ParentNode("div", None)