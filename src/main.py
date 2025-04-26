from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utilities import split_nodes_delimiter

def main():

    '''
    tst = TextNode("This is some anchor text",TextType.LINK,"https://www.boot.dev")
    print(tst.__repr__())
    tst_prop = {
    "href": "https://www.google.com",
    "target": "_blank",
}
    tst2 = HTMLNode("p", "some value", None ,tst_prop)
    print(tst2.props_to_html())
    print(repr(tst2))

    tst3 = LeafNode("p", "This is a paragraph of text.")
    print(tst3.to_html())

    tst4 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(tst4.to_html())

    tst5 = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)

    print(tst5.to_html())
    '''

    tst_splitter_node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([tst_splitter_node], "`", TextType.CODE)





if __name__ == "__main__":
    main()