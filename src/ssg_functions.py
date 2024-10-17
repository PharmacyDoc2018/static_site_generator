import re
import shutil
import os

from textnode import TextNode
from leafnode import LeafNode
from parentnode import ParentNode

def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text, None)
    elif text_node.text_type == "bold":
        return LeafNode("b", text_node.text, None)
    elif text_node.text_type == "italic":
        return LeafNode("i", text_node.text, None)
    elif text_node.text_type == "code":
        return LeafNode("code", text_node.text, None)
    elif text_node.text_type == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Invalid text type")

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
        elif node.url != None:
            new_nodes.append(node)
        elif node.text.count(delimiter) < 2:
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
    
    def merge_text_img_nodes(img_list, node_text):
        if img_list == []:
            return [TextNode(node_text, "text")]
        
        temp_list = []
        img = img_list.pop(0)
        node_text_split = node_text.split(f"![{img[0]}]({img[1]})")
        temp_list.append(TextNode(node_text_split[0], "text"))
        temp_list.append(TextNode(img[0], "image", img[1]))
        temp_list.extend(merge_text_img_nodes(img_list, node_text_split[1]))
        return temp_list

    
    old_nodes_copy = old_nodes
    new_nodes = []
    for node in old_nodes_copy:
        img_list = extract_markdown_images(node.text)
        node_text = node.text
        if img_list == []:
            new_nodes.append(node)
        else:
            new_nodes.extend(merge_text_img_nodes(img_list, node_text))

    for node in new_nodes:
        if node.text == "":
            new_nodes.remove(node)

    return new_nodes

def split_nodes_link(old_nodes):
    
    def merge_text_link_nodes(link_list, node_text):
        if link_list == []:
            return [TextNode(node_text, "text")]
        
        temp_list = []
        link = link_list.pop(0)
        node_text_split = node_text.split(f"[{link[0]}]({link[1]})")
        temp_list.append(TextNode(node_text_split[0], "text"))
        temp_list.append(TextNode(link[0], "link", link[1]))
        temp_list.extend(merge_text_link_nodes(link_list, node_text_split[1]))
        return temp_list

    
    old_nodes_copy = old_nodes
    new_nodes = []
    for node in old_nodes_copy:
        link_list = extract_markdown_links(node.text)
        node_text = node.text
        if link_list == []:
            new_nodes.append(node)
        else:
            new_nodes.extend(merge_text_link_nodes(link_list, node_text))

    for node in new_nodes:
        if node.text == "":
            new_nodes.remove(node)

    return new_nodes

def split_bold_nodes(old_nodes):
    return split_nodes_delimiter(old_nodes, "**", "bold")

def split_italic_nodes(old_nodes):
    return split_nodes_delimiter(old_nodes, "*", "italic")

def split_code_nodes(old_nodes):
    return split_nodes_delimiter(old_nodes, "`", "code")

def text_to_textnodes(text):
    nodes = [TextNode(text, "text")]
    function_list = [split_bold_nodes, split_italic_nodes, split_code_nodes, split_nodes_image, split_nodes_link]
    for fxn in function_list:
        nodes = fxn(nodes)
    return nodes

def markdown_to_blocks(markdown):
    block_list = markdown.split("\n\n")
    filtered_list_1 = []
    filtered_list_2 = []
    for block in block_list:
        if block == "":
            pass
        else:
            filtered_list_1.append(block.strip())
    for item in filtered_list_1:
        item_split = item.split("\n")
        if len(item_split) > 1:
            items_joined = []
            for i in item_split:
                items_joined.append(i.strip())
            filtered_list_2.append("\n".join(items_joined))
        else:
            filtered_list_2.append(item)
    return filtered_list_2

def block_to_block_type(block):
    block_split = block.split("\n")
    
    is_quote = True                                    #
    for item in block_split:                           # identifies
        if re.fullmatch(r"\>(.*?)", item) == None:     # quotes
            is_quote = False                           #
    
    is_star_list = True                                #
    is_dash_list = True                                #
    for item in block_split:                           # identifies
        if re.fullmatch(r"\* (.*?)", item) == None:    # unordered
            is_star_list = False                       # lists
    for item in block_split:                           #
        if re.fullmatch(r"\- (.*?)", item) == None:    #
            is_dash_list = False                       #
    
    is_ordered_list = True
    num_list = re.findall(r"\d. ", block)
    if len(num_list) == 0:
        is_ordered_list = False
    else:
        i = 1
        for num in num_list:
            if num != f"{i}. ":
                is_ordered_list = False
            i += 1
            
    if re.findall(r"#{1,6} ", block) != []: #identifies headings
        block_type = "heading"
    elif re.findall(r"\`{3}(.*?)\`{3}", block) != []: #identifies code
        block_type = "code"
    elif is_quote == True:
        block_type = "quote"
    elif (is_star_list == True) or (is_dash_list == True):
        block_type = "unordered_list"
    elif is_ordered_list == True:
        block_type = "ordered_list"
    else:
        block_type = "paragraph"

    return block_type

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    HTML_node_list = []
    for block in markdown_blocks:
        HTML_node_list.append(block_to_html_node(block))
    return ParentNode("div", HTML_node_list)
        
def block_to_html_node(block):

    block_type = block_to_block_type(block)
    tag = None
    if block_type == "quote":
        node = ParentNode("blockquote", text_to_children(block, block_type))
    elif block_type == "unordered_list":
        node = ParentNode("ul",text_to_children(block, block_type))
    elif block_type == "ordered_list":
        node = ParentNode("ol",text_to_children(block, block_type))
    elif block_type == "code":
        node = ParentNode("pre", text_to_children(block, block_type))
    elif block_type == "heading":
        hash_num = block.count("#")
        node = ParentNode(f"h{hash_num}", text_to_children(block, block_type))
    elif block_type == "paragraph":
        node = ParentNode("p", text_to_children(block, block_type))
    else:
        raise Exception("Invalid block")
    
    return node

def text_to_children(text, block_type):
    child_list = []
    if block_type == "quote":
        text_node_list = text_to_textnodes(text)
        for node in text_node_list:
            child_list.append(text_node_to_html_node(node))

    elif block_type == "unordered_list":
        temp_list = text.split("\n")
        for item in temp_list:
            #text_node_list = text_to_textnodes(item[2:]) not sure about clipping the - or * 
            text_node_list = text_to_textnodes(item)
            html_node_list = []
            for node in text_node_list:
                html_node_list.append(text_node_to_html_node(node))
            child_list.append(ParentNode("li", html_node_list))

    elif block_type == "ordered_list":
        temp_list = text.split("\n")
        for item in temp_list:
            text_node_list = text_to_textnodes(item)
            html_node_list = []
            for node in text_node_list:
                html_node_list.append(text_node_to_html_node(node))
            child_list.append(ParentNode("li", html_node_list))

    elif block_type == "code":
        text_node_list = text_to_textnodes(text)
        for node in text_node_list:
            child_list.append(text_node_to_html_node(node))

    elif block_type == "heading":
        text_node_list = text_to_textnodes(text.lstrip("# "))
        for node in text_node_list:
            child_list.append(text_node_to_html_node(node))

    elif block_type == "paragraph":
        text_node_list = text_to_textnodes(text)
        for node in text_node_list:
            child_list.append(text_node_to_html_node(node))

    return child_list

def copy_static_to_public():
    if os.path.exists("public/"):
        shutil.rmtree("public/")
    os.mkdir("public/")
    
    def copy_files(path_copy, path_paste):
        for item in os.listdir(path_copy):
            if os.path.isfile(os.path.join(path_copy, item)):
                shutil.copy(os.path.join(path_copy, item), path_paste)
            elif os.path.isdir(os.path.join(path_copy, item )):
                os.mkdir(os.path.join(path_paste, item))
                copy_files(os.path.join(path_copy, item), os.path.join(path_paste, item))
            
    copy_files("static/", "public/")