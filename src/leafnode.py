from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        self.tag = tag
        self.value = value
        self.props = props
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        
    def to_html(self):
        if self.tag == None:
            return self.value
        else:
            return "<" + self.tag + self.props_to_html() + ">" + self.value + "</" + self.tag + ">"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

