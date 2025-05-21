import re

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocktypes import BlockType, block_to_block_type

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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        image_data = extract_markdown_images(node.text)
        if not image_data:
            new_nodes.append(node)
            continue

        old_text = node.text
        for i, (alt, link) in enumerate(image_data):
            split_parts = old_text.split(f"![{alt}]({link})",1)

            before_image = split_parts[0]
            if before_image.strip():
                new_nodes.append(TextNode(before_image, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, link))
            old_text = split_parts[1]

        if old_text.strip():
            new_nodes.append(TextNode(old_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link_data = extract_markdown_links(node.text)
        if not link_data:
            new_nodes.append(node)
            continue

        old_text = node.text
        for i, (txt, link) in enumerate(link_data):
            split_parts = old_text.split(f"[{txt}]({link})", 1)

            before_link = split_parts[0]
            if before_link.strip():
                new_nodes.append(TextNode(before_link, TextType.TEXT))

            new_nodes.append(TextNode(txt, TextType.LINK, link))
            old_text = split_parts[1]

        if old_text.strip():
            new_nodes.append(TextNode(old_text, TextType.TEXT))

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

def text_to_textnodes(text):
    original_node = TextNode(text, TextType.TEXT)

    images_processed = split_nodes_image([original_node])
    links_processed = split_nodes_link(images_processed)
    bold_processed = split_nodes_delimiter(links_processed,"**", "Bold")
    code_processed = split_nodes_delimiter(bold_processed,"`", "Code")
    italic_processed = split_nodes_delimiter(code_processed,"_", "Italic")

    return italic_processed

def markdown_to_blocks(markdown):
    blocks = re.split(r'\n\s*\n', markdown.strip())
    return [block.strip() for block in blocks if block.strip()]


def text_to_children(block):
    return  list(map(text_node_to_html_node, text_to_textnodes(block.replace("\n", " "))))

def list_to_lines(block):
    lines = block.strip().split("\n")
    nodes = []

    for line in lines:
        clean = re.sub(r"^(- +|\d+\. +)", "", line).strip()
        children = text_to_children(clean)
        nodes.append(ParentNode("li", children))
    return nodes

def quote_to_lines(block):
    lines = block.strip().split("\n")
    cleaned = []

    for line in lines:
        clean = re.sub(r"^(>)", "", line).strip()
        cleaned.append(clean)

    children = text_to_children(" ".join(cleaned))

    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_blocks = []

    for block in blocks:
        block_type = block_to_block_type(block)
        match(block_type):
            case(BlockType.PARAGRAPH):
                 parent_blocks.append(ParentNode("p",text_to_children(block),None))
            case(BlockType.QUOTE):
                 parent_blocks.append(ParentNode("blockquote",quote_to_lines(block),None))
            case(BlockType.UNORDERED_LIST):
                 parent_blocks.append(ParentNode("ul",list_to_lines(block),None))
            case(BlockType.ORDERED_LIST):
                 parent_blocks.append(ParentNode("ol",list_to_lines(block),None))
            case(BlockType.CODE):
                code_content = block[4:-3]
                text_node = TextNode(code_content, TextType.CODE)
                html_node = text_node_to_html_node(text_node)
                parent_blocks.append(ParentNode("pre",[html_node],None))
            case(BlockType.HEADING):
                 match = re.match(r"^(#{1,6}) +(.*?)$", block)
                 level = len(match.group(1))
                 parent_blocks.append(ParentNode(f"h{level}",text_to_children(block[level+1:]),None))

    return ParentNode("div", parent_blocks, None)

def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line[2:]

    raise Exception("Markdown file missing title")