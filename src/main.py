from textnode import TextNode, TextType
from htmlnode import HTMLNode

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


if __name__ == "__main__":
    main()