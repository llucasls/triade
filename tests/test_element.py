from triade.element import Element


class TestElement:
    "Test Element class"

    def test_create_with_dictionary(self):
        "create Element object with a dictionary"

        Element({"tag": "span", "text": "some text"})

        Element({"tag": "div",
                 "children": [
                     {"tag": "span", "text": "first span"},
                     {"tag": "span", "text": "second span"}]})

    def test_create_with_positional_args(self):
        "create Element object with positional arguments"

        Element("span", None, None, "some text")

        Element("main", {"class": "content"},
                [Element("span", None, None, "first span"),
                 Element("span", None, None, "second span")])

    def test_create_with_named_args(self):
        "create Element object with named arguments"

        Element(tag="span", text="some text")

        Element(tag="main", attributes={"class": "content"},
                children=[Element(tag="span", text="first span"),
                          Element(tag="span", text="second span")])

    def test_create_with_positional_and_named_args(self):
        "create Element with both positional and named arguments"

        Element("div", {"class": "container"},
                children=[Element("p", text="This is the first paragraph"),
                          Element("p", text="This is the second one")])

        Element("span", text="some text")
