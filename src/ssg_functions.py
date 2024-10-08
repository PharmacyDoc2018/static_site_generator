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
        elif node.url != None:
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