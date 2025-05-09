from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if re.match(r"^#{1,6} (.*?)$", block):
        return BlockType.HEADING
    if re.match(r"^'''(.*?)'''$", block, re.DOTALL):
        return BlockType.CODE
    if re.match(r"^(?:>.*(?:\n|$))+", block, re.MULTILINE):
        return BlockType.QUOTE
    if re.match(r"^(?:- .*(?:\n|$))+", block, re.MULTILINE):
        return BlockType.UNORDERED_LIST

    numbered_list = re.findall(r"^(\d+)\. .*(?:\n|$)", block, re.MULTILINE)
    numbers = [int(num) for num in numbered_list]

    if len(numbers) >= 2 and numbers[0] == 1 and is_sequential(numbers):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def is_sequential(nums):
    return all(b == a + 1 for a, b in zip(nums, nums[1:]))