import re

from textnode import TextNode

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    old_nodes_copy = old_nodes
    new_nodes = []
    compatible_text_types = ["bold", "italic", "code"]
    if text_type not in compatible_text_types:
        raise Exception("Invalid text_type")
    for node in old_nodes_copy:
        if delimiter not in node.text:
            new_nodes.append(node)
        if node.url != None:
            new_nodes.append(node)
        else:
            temp_list = node.text.split(delimiter)
            if temp_list[0] == "":
                temp_list.pop(0)
            if temp_list[-1] == "":
                temp_list.pop(-1)
            if (node.text[:1] == delimiter) or (node.text[:2] == delimiter):
                alternating_bool = False
            else:
                alternating_bool = True
            for i in range(0, len(temp_list)):
                if alternating_bool == True:
                    temp_list[i] = TextNode(temp_list[i], "text")
                elif alternating_bool == False:
                    temp_list[i] = TextNode(temp_list[i], text_type)
                alternating_bool = (alternating_bool == False)
            new_nodes.extend(temp_list)
    return new_nodes

def split_nodes_image(old_nodes):
    old_nodes_copy = old_nodes
    new_nodes = []
    
def split_nodes_link(old_nodes):
    pass