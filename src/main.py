from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
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

def text_node_to_html_node(textnode):
    match textnode.text_type:
        case(TextType.TEXT):
            return LeafNode(None,textnode.text)
        case(TextType.BOLD):
            return LeafNode("b", textnode.text)
        case(TextType.ITALIC):
            return LeafNode("i", textnode.text)
        case(TextType.NORMAL):
            return LeafNode(None, textnode.text)
        case(TextType.CODE):
            return LeafNode("code", textnode.text)
        case(TextType.LINK):
            return LeafNode("a", textnode.text,{"href":textnode.url})
        case(TextType.IMAGE):
            return LeafNode("img", "",{"src":textnode.url,"alt":textnode.text})
        case _:
            raise TypeError(f"Unsupported TextNode Type: {textnode.text_type}")



if __name__ == "__main__":
    main()