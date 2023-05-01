from typing import List, Dict, Type
import re

from magic_repr import make_repr


class Element(dict):
    tag: str
    attributes: Dict[str, str]
    children: List["Element"]
    text: str

    def __init__(
        self,
        element=None,
        /,
        attributes=None,
        children=None,
        text=None,
        *,
        tag=None,
        level=0,
    ):
        self._level = level

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

                if key == "children":
                    self["children"] = [
                        Element(child, level=(level + 1)) for child in value
                    ]
                else:
                    self[key] = value

            return

        elif isinstance(element, str) and tag is None:
            tag = element

        self["tag"] = tag
        if attributes:
            self["attributes"] = attributes
        if children:
            self["children"] = [
                Element(child, level=(level + 1)) for child in children
            ]
        if text:
            self["text"] = text

        if children and text:
            raise ValueError("Element cannot have children and text at the same time")

        if not self.is_element(self):
            raise ValueError("The given object is not a valid element")

    @property
    def tag(self):
        "Returns the element's tag name"
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

    @property
    def level(self):
        return self._level

    @tag.setter
    def tag(self, value):
        self["tag"] = value

    @attributes.setter
    def attributes(self, value):
        self["attributes"] = value

    @children.setter
    def children(self, value):
        self["children"] = value

    @text.setter
    def text(self, value):
        self["text"] = value

    @attributes.deleter
    def attributes(self):
        del self["attributes"]

    @children.deleter
    def children(self):
        del self["children"]

    @text.deleter
    def text(self):
        del self["text"]

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

    def _get_children_str(self, parent: Type["Element"]) -> str:
        return [str(child) for child in parent.children]

    def _get_attr_str(self):
        if not self.attributes:
            return ""
        return " ".join([f'{key}="{value}"' for key, value in self.attributes.items()])

    def _clean(self, value: str) -> str:
        return value.replace("u'", "'").replace("'<", "<").replace(">'", ">")

    # def __str__(self):
    #    if self.attributes and self.children:
    #        return self._clean(
    #            make_repr("tag", "attributes", children=self._get_children_str)(self)
    #        )
    #    elif self.attributes and self.text:
    #        return self._clean(make_repr("tag", "attributes", "text")(self))
    #    elif self.attributes:
    #        return self._clean(make_repr("tag", "attributes")(self))
    #    elif self.children:
    #        return self._clean(make_repr("tag", children=self._get_children_str)(self))
    #    elif self.text:
    #        return self._clean(make_repr("tag", "text")(self))

    #    return make_repr("tag")(self)

    def __repr__(self):
        tag = self.tag
        attributes = self.attributes
        children = self.children
        text = self.text

        args = [f'tag="{tag}"']

        if attributes:
            attr = str(attributes).replace("'", '"')
            args.append(f"attributes={attr}")
        args.append(f"children={children}") if children else None
        args.append(f'text="{text}"') if text else None

        arg_list = ", ".join(args)

        return f"Element({arg_list})"

    def to_xml(self):
        is_self_closed = not self.children and not self.text

        if self.children:
            content = [child.to_xml() for child in self.children]
            content = (
                str(content)
                .replace("'", "")
                .replace("[", "")
                .replace("]", "")
                .replace(", ", "")
            )
        elif self.text:
            content = self.text
        else:
            content = ""

        if self.attributes:
            open_tag_content = " ".join([self.tag, self._get_attr_str()])
        else:
            open_tag_content = self.tag

        if is_self_closed:
            open_tag = f"<{open_tag_content} />"
            close_tag = ""
        else:
            open_tag = f"<{open_tag_content}>"
            close_tag = f"</{self.tag}>"

        return f"{open_tag}{content}{close_tag}"

    def __str__(self):
        result = self.to_xml()

        return result
