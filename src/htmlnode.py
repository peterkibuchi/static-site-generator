# Defers evaluation of type hints so forward references
# (e.g. ParentNode | LeafNode in HTMLNode) resolve correctly
from __future__ import annotations


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[ParentNode | LeafNode] | None = None,
        props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        # Each attribute is prefixed with a space so the result
        # can be inserted directly after the tag name: <tag {props}>
        final = ""
        if self.props == None:
            return final
        for key, val in self.props.items():
            final += f' {key}="{val}"'
        return final

    def __repr__(self) -> str:
        return f"HTMLNode: \ntag={self.tag},\nvalue={self.value},\nchildren={self.children},\nprops={self.props}\n"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("invalid HTML: all leaf nodes must have a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"HTMLNode: \ntag={self.tag},\nvalue={self.value},\nprops={self.props}\n"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[ParentNode | LeafNode],
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("invalid HTML: all parent nodes must have a tag")
        if self.children == None:
            raise ValueError(
                "invalid HTML: all parent nodes must have child nodes")
        # Recursively render children — supports arbitrary nesting of ParentNode and LeafNode
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"

    def __repr__(self) -> str:
        return f"HTMLNode: \ntag={self.tag},\nvalue={self.value},\nprops={self.props}\n"
