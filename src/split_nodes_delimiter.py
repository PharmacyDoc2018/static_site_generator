from textnode import TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    old_nodes_copy = old_nodes
    new_nodes = []
    compatible_text_types = ["bold", "italic", "code"]
    if text_type not in compatible_text_types:
        raise Exception("Invalid text_type")
    for node in old_nodes_copy:
        if delimiter not in node.text:
            new_nodes.append(node)
        else:
            temp_list = node.text.split(delimiter)
            alternating_bool = True
            for item in temp_list:
                if alternating_bool == True:
                    item = TextNode(item, "text")
                elif alternating_bool == False:
                    item = TextNode(item, text_type)
                alternating_bool = (alternating_bool == False)
            new_nodes.extend(temp_list)
    return new_nodes