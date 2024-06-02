import os
import re
from anytree import Node, RenderTree


def create_directory_tree(directory, parent_node):
    for item in sorted(os.listdir(directory)):
        item_path = os.path.join(directory, item)
        node = Node(item, parent=parent_node)
        if os.path.isdir(item_path):
            create_directory_tree(item_path, node)


def get_directory_tree_list(root_directory, root_name):
    directory_tree_list = []

    root_node = Node(root_name)
    create_directory_tree(root_directory, root_node)

    for pre, fill, node in RenderTree(root_node):
        directory_tree_list.append(f"{pre}{node.name}")

    return directory_tree_list


def get_updated_readme(readme_path, replace_string, regex_pattern=None):
    with open(readme_path, "r", encoding="utf-8") as file:
        content = file.read()

    if regex_pattern is None:
        regex_pattern = r"(<!-- PROJECT_DIR_TREE_START -->)(.*?)(<!-- PROJECT_DIR_TREE_END -->)"

    updated_content = re.sub(regex_pattern, replace_string, content, flags=re.DOTALL)

    return updated_content


if __name__ == "__main__":
    directory_tree_list = "\n".join(get_directory_tree_list("../app", "app"))
    updated_readme = get_updated_readme(
        "../readme_format/README.md", directory_tree_list
    )
    with open("../README.md", "w", encoding="utf-8") as file:
        file.write(updated_readme)
