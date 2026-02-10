from __future__ import annotations


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        final = ""
        if self.props == None:
            return final
        for key, val in self.props.items():
            final += f' {key}="{val}"'
        return final

    def __repr__(self) -> str:
        return f"HTMLNode: \ntag={self.tag},\nvalue={self.value},\nchildren{self.children},\nprops{self.props}\n"
