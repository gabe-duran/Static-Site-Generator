import os
import shutil
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utilities import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    markdown_to_html_node,
    extract_title
)

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


    tst_splitter_node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([tst_splitter_node], "`", TextType.CODE)


    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )

    print(split_nodes_image([node]))

    md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
    blocks = markdown_to_blocks(md)
    print(blocks)


    markdown = """ 
    This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    md_blocks = markdown_to_html_node(markdown)
    #print(f"from main: {md_blocks}")
    print(md_blocks.to_html())


    source = "./static/"
    target = "./public/"

    copytree(source, target)


    path = os.path.join("content", "index.md")

    with open(path) as f:
        file_contents = f.read()

    print(extract_title(file_contents))


    generate_page("content","./","./test")
'''

    source = os.path.join("static")
    target = os.path.join("public")

    copytree(source, target)

    frm = os.path.join("content", "index.md")
    to = os.path.join("public", "index.html")
    template = os.path.join("template.html")
    generate_page(frm, template, to)


def copytree(source, target):

    source = os.path.abspath(source)
    target = os.path.abspath(target)


    if os.path.exists(target):
        shutil.rmtree(target)

    os.mkdir(target)
    log_path = os.path.join(target, "copy_log.txt")

    with open(log_path, "w") as log:
        _copy_contents_with_log(source, target, log)

    print(f"Copied '{source}' → '{target}'")
    print(f"Log written to: {log_path}")


def _copy_contents_with_log(source, target, log):

    for entry in os.listdir(source):
        src_path = os.path.join(source, entry)
        tgt_path = os.path.join(target, entry)

        if os.path.isfile(src_path):
            shutil.copy(src_path, tgt_path)
            log.write(f"Copied: {src_path} → {tgt_path}\n")
        else:
            os.mkdir(tgt_path)
            _copy_contents_with_log(src_path, tgt_path, log)

def generate_page(from_path, template_path, dest_path):
    md_file = os.path.join(from_path)
    t_file = os.path.join(template_path)
    d_path = os.path.join(dest_path)

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(md_file) as md:
        markdown = md.read()

    with open(t_file) as t:
        template = t.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title).replace("{{ Content }}",content)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(d_path, "w") as d:
        d.write(template)

if __name__ == "__main__":
    main()