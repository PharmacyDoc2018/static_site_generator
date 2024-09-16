class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        
        def build_str(lst):
            if lst == []:
                return ""
            items = lst.pop(0)
            s =  (f" {items[0]}={items[1]}") + build_str(lst)
            return s
        
        return build_str(self.props.items())
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    