from textnode import TextNode, TextType

def main():
    tst = TextNode("This is some anchor text",TextType.LINK,"https://www.boot.dev")
    print(tst.__repr__())

if __name__ == "__main__":
    main()