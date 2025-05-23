class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_string = ""
        if self.props is not None:
            for key, value in self.props.items():
                html_string += f' {key}="{value}"'
        return html_string

    def __repr__(self):
        tag = f"tag: {self.tag}"
        value = f"value: {self.value}"
        children = f"children: {str(self.children)}"
        props = f"props: {self.props_to_html()}"

        return f"{tag}\n{value}\n{children}\n{props}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not isinstance(children, list):
            raise TypeError("children must be a list of LeafNode instances")
        if not children:
            raise ValueError("children list cannot be empty")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None:
            raise ValueError("All parent nodes must have children")
        html_string = ""
        for child in self.children:
            html_string += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{html_string}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"