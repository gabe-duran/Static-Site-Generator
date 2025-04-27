import re

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    #print(f"old_nodes: {old_nodes}")
    #print(f"delimiter: {delimiter}")
    #print(f"text_type: {text_type}")
    #print(f"new_nodes: {new_nodes}")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_node_text = node.text.split(delimiter)
     #   print(f"split_node_text: {split_node_text}")

        if len(split_node_text) % 2 == 0:
            raise Exception(f"invalid Markdown syntax: missing {delimiter} pair")

        for i, item in enumerate(split_node_text):
            if item == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(item, TextType.TEXT))
            else:
                match delimiter:
                    case "`":
                        new_nodes.append(TextNode(item, TextType.CODE))
                    case "**":
                        new_nodes.append(TextNode(item, TextType.BOLD))
                    case "_":
                        new_nodes.append(TextNode(item, TextType.ITALIC))
                    case _:
                        raise Exception("Unsupported delimiter")
    return new_nodes


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

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)




