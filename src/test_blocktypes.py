import unittest

from blocktypes import BlockType, block_to_block_type

class TestBlockTypes(unittest.TestCase):
    def test_block_to_block_type_headings(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = f"```this is a code block.\nThis is another line in the code block```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = f">this is a quote block.\n>This is another line in the quote block"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_ul(self):
        block = f"- item one unordered list.\n- item two unordered list.\n- item three unordered list."
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ol(self):
        block = f"1. item one unordered list.\n2. item two unordered list.\n3. item three unordered list."
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        block = f"This is just any old paragraph.  Nothing to see here.  Move along."
        block_2 = f"1. This isn't a list. It's a paragraph about item 1."

        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block_2), BlockType.PARAGRAPH)