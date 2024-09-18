from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)
        self.tag = tag
        self.children = children
        self.props = props
        if self.tag == None:
            raise ValueError("tag required for ParentNode")
        if self.children == None:
            raise ValueError("children required for ParentNode")
        
    def to_html(self):
        children_copy = self.children
        def build_children_html(children_list):
            s = ""
            for child in children_list:
                if isinstance(child, ParentNode):
                    s += "<" + child.tag + child.props_to_html() + ">" + build_children_html(child.children) + "</" + child.tag + ">"
                else:
                    s += child.to_html()
            return s
        return "<" + self.tag + self.props_to_html() + ">" + build_children_html(children_copy) + "</" + self.tag + ">"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"