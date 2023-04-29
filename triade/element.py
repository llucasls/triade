from typing import List, Dict, Type

from magic_repr import make_repr


class Element(dict):
    tag: str
    attributes: Dict[str, str]
    children: List["Element"]
    text: str

    def __init__(
        self, element=None, /, attributes=None, children=None, text=None, *, tag=None
    ):
        if isinstance(element, dict):
            if tag or attributes or children or text:
                raise ValueError(
                    "Combining dictionary and named arguments is not allowed"
                )
            if "tag" not in element.keys():
                raise ValueError("The tag name was not provided")

            for key, value in element.items():
                if key not in ["tag", "attributes", "children", "text"]:
                    raise ValueError(f"Unrecognized dictionary key: {key}")

                self[key] = value

            return

        elif isinstance(element, str) and tag is None:
            tag = element

        self["tag"] = tag
        if attributes:
            self["attributes"] = attributes
        if children:
            self["children"] = children
        if text:
            self["text"] = text

        if children and text:
            raise ValueError("Element cannot have children and text at the same time")

        if not self.is_element(self):
            raise ValueError("The given object is not a valid element")

    @property
    def tag(self):
        return self.get("tag")

    @property
    def attributes(self):
        return self.get("attributes")

    @property
    def children(self):
        return self.get("children")

    @property
    def text(self):
        return self.get("text")

    @classmethod
    def is_element(cls: Type["Element"], obj: dict) -> bool:
        tag = obj.get("tag")
        attributes = obj.get("attributes")
        children = obj.get("children")
        text = obj.get("text")

        if not isinstance(tag, str):
            return False

        if attributes is not None and not isinstance(attributes, dict):
            return False
        elif isinstance(attributes, dict):
            for value in attributes.values():
                if not isinstance(value, str):
                    return False

        if children is not None and text is not None:
            return False

        if children is not None:
            if not isinstance(children, list):
                return False
            for child in children:
                if not cls.is_element(child):
                    return False

        if text is not None and not isinstance(text, str):
            return False

        for key in obj.keys():
            if key not in ["tag", "attributes", "children", "text"]:
                return False

        return True

    def get_children_str(self, parent: Type["Element"]) -> str:
        return [str(child) + "\n" for child in parent.children]

    def clean(self, value: str) -> str:
        return (
            value.replace("u'", "'")
            .replace("'<", "<")
            .replace(">'", ">")
            .replace("']", "]")
        )

    def __str__(self):
        if self.attributes and self.children:
            return self.clean(
                make_repr("tag", "attributes", children=self.get_children_str)(self)
            )
        elif self.attributes and self.text:
            return self.clean(make_repr("tag", "attributes", "text")(self))
        elif self.attributes:
            return self.clean(make_repr("tag", "attributes")(self))
        elif self.children:
            return self.clean(make_repr("tag", children=self.get_children_str)(self))
        elif self.text:
            return self.clean(make_repr("tag", "text")(self))

        return make_repr("tag")(self)

    def __repr__(self):
        tag = self.tag
        attributes = self.attributes
        children = self.children
        text = self.text

        args = [f"tag={tag}"]
        args.append(f"attributes={attributes}") if attributes else None
        args.append(f"children={children}") if children else None
        args.append(f"text={text}") if text else None

        arg_list = ", ".join(args)

        return f"Element({arg_list})"
