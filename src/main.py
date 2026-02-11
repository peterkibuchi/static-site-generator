from textnode import TextNode, TextType
from utils import split_nodes_image


def main():
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    print(f"split_nodes_image node:", node)
    print(f"split_nodes_image result:", split_nodes_image([node]))


if __name__ == "__main__":
    main()
