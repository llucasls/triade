import xml.dom


def create_document(name):
    impl = xml.dom.getDOMImplementation()
    return impl.createDocument(xml.dom.EMPTY_NAMESPACE, name, None)


def create_attribute(name, value):
    with create_document("temp_doc") as doc:
        attr = doc.createAttribute(name)
        attr.value = value
        return attr


def create_text_node(data):
    with create_document("temp_doc") as doc:
        return doc.createTextNode(data)


def create_element(tag_name):
    with create_document("temp_doc") as doc:
        return doc.createElement(tag_name)


# triade.xml_element.Thesaurus
class Thesaurus(dict):
    """A dictionary that exhaustively searches a value from a list of keys."""
    def get(self, key, default=None):
        """Retrieves a value that matches a given key, like in a regular
        dictionary, or the default value if the key is not present. If the key
        is a list, then it will iterate through all the values one by one and
        return the first match found or the default value if not. Any other
        unhashable type will simply return the default value, unlike a
        dictonary that would raise a TypeError."""
        if isinstance(key, list):
            for index in range(len(key)):
                if key[index] in self:
                    return self[key[index]]

        elif self._is_hashable(key):
            try:
                return self[key]
            except KeyError:
                return default

        return default

    def __repr__(self):
        cls = type(self).__name__
        text = ", ".join("%s: %s" % (repr(k), repr(v)) for k, v in self.items())
        return "%s({%s})" % (cls, text)

    def __contains__(self, item):
        """This method allows for the use of:
            key_list in T
        where key_list is a list and T is a Thesaurus object. It returns True
        if any of the keys found in key_list is found in T and False otherwise.
        A key of a hashable type will work as normal and any other unhashable
        types will raise a TypeError."""
        if isinstance(item, list):
            for key in item:
                if key in self.keys():
                    return True
            return False
        elif self._is_hashable(item):
            return item in self.keys()
        else:
            raise TypeError("unhashable type: '%s'" % type(item).__name__)

    def _is_hashable(self, value):
        try:
            hash(value)
            return True
        except TypeError:
            return False


# triade.xml_element.TriadeDocument
class TriadeDocument:
    def __init__(self, root_element):
        self._document = create_document(root_element.tag)
        self._root_element = self._document.documentElement


# triade.xml_element.TriadeElement
class TriadeElement:
    def __init__(self, data, *, level=0):
        data = Thesaurus(data)
        self._validate(data)

        tag_name = data.get(["tagName", "tag_name"])
        self._elem = create_element(tag_name)

        child_nodes = data.get(["childNodes", "child_nodes"])
        if child_nodes is not None:
            self._children = TriadeNodeList(child_nodes)

    def __getitem__(self, key):
        if key in ["tagName", "tag_name"]:
            return self._elem.tagName
        elif key in ["childNodes", "child_nodes"]:
            return self._elem.childNodes

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    @property
    def tagName(self):
        """The element's tag name."""
        return self._elem.tagName

    @tagName.setter
    def tagName(self, value):
        if not isinstance(value, str):
            raise TriadeNodeTypeError('"tagName" value must be a string.')
        self._elem.tagName = value

    @tagName.deleter
    def tagName(self):
        raise TriadeXMLException("Deleting tagName is not allowed.")

    tag_name = property(tagName.fget, tagName.fset, tagName.fdel)

    @property
    def childNodes(self):
        """The element's child nodes."""

    def toxml(self):
        return self._elem.toxml()

    def _validate(self, data):
        if not isinstance(data, dict):
            raise TriadeNodeTypeError('"data" should be a dictionary.')

        if ["tagName", "tag_name"] not in data:
            raise TriadeNodeValueError('"tagName" not found in "data".')


# triade.xml_element.TriadeNodeList
class TriadeNodeList:
    def __init__(self, data):
        self._validate(data)

        self._elems = []
        for elem in data:
            self._elems.append(TriadeElement(elem))

    def __len__(self):
        return len(self._elems)

    def __iter__(self):
        return iter(self._elems)

    def _validate(self, data):
        if not isinstance(data, list):
            raise TriadeNodeTypeError('"data" should be a list.')

        for node in data:
            if not isinstance(node, dict):
                msg = 'Every value in "data" should be a dictionary.'
                raise TriadeNodeValueError(msg)


# triade.xml_element.TriadeAttribute
class TriadeAttribute:
    def __init__(self, name, value):
        if name.count(":") > 1:
            msg = "Attribute name should contain at most one colon."
            raise TriadeNodeValueError(msg)
        self._node = create_attribute(name, value)

    def __str__(self):
        return '<?attr %s="%s" ?>' % (self._node.name, self._node.value)

    def __repr__(self):
        cls = type(self).__name__
        return "%s(%s, %s)" % (cls, repr(self._node.name), repr(self._node.value))

    def __getitem__(self, key):
        if key not in ["name", "value"]:
            msg = "The key %s is not present in TriadeAttribute." % (key,)
            raise KeyError(msg)

        if key == "name":
            return self._node.name
        elif key == "value":
            return self._node.value

    def __setitem__(self, key, value):
        if key not in ["name", "value"]:
            msg = 'The only keys allowed for TriadeAttribute are "name" and "value".'
            raise TriadeNodeValueError(msg)

        if key == "name":
            self._node.name = value
        elif key == "value":
            self._node.value = value

    def __delitem__(self, key):
        NotImplementedError("deletion not allowed")

    @property
    def name(self):
        """The attribute's name."""
        return self._node.name

    @name.setter
    def name(self, new_name):
        self._node.name = new_name

    @name.deleter
    def name(self):
        NotImplementedError("deletion not allowed")

    @property
    def value(self):
        """The attribute's value."""
        return self._node.value

    @value.setter
    def value(self, new_value):
        self._node.value = new_value

    @value.deleter
    def value(self):
        NotImplementedError("deletion not allowed")

    @property
    def node(self):
        """The XML DOM Attr object associated with this object."""
        return self._node

    @property
    def localName(self):
        parts = self.name.split(":")
        return parts[1] if len(parts) > 1 else self.name

    @property
    def prefix(self):
        parts = self.name.split(":")
        return parts[0] if len(parts) > 1 else ""

    @property
    def namespaceURI(self):
        return self._node.namespaceURI

    nodeName = property(name.fget, name.fset, name.fdel)
    nodeValue = property(value.fget, value.fset, value.fdel)


# triade.xml_element.TriadeAttributeList
class TriadeAttributeList:
    def __init__(self, attributes, element=None):
        self._attrs = {}
        self._len = 0
        self._element = element

        for name, value in attributes.items():
            self._attrs[name] = TriadeAttribute(name, value)
            self._len += 1

    def __str__(self):
        text = " ".join('%s="%s"' % (attr.name, attr.value)
                        for attr in self._attrs.values())
        return " ".join(["<?attributeList", text, "?>"])

    def __repr__(self):
        cls = type(self).__name__
        text = ", ".join("%s: %s" % (repr(attr.name), repr(attr.value))
                         for attr in self._attrs.values())

        if self._element is not None:
            return "%s({%s}, %s)" % (cls, text, repr(self._element))

        return "%s({%s})" % (cls, text)

    def __iter__(self):
        return iter(self._attrs.values())

    def __contains__(self, name):
        return name in self._attrs

    def __getitem__(self, name):
        return self._attrs[name]

    def __setitem__(self, name, value):
        if name in self._attrs:
            self._change_value(name, value)
        else:
            self._add_value(name, value)

    def __delitem__(self, name):
        del self._attrs[name]
        self._len -= 1

    def __len__(self):
        return self._len

    def get(self, name, default=None):
        self._attrs.get(name, default)

    def getNamedItem(self, name):
        pass

    def item(self, index):
        pass

    def items(self):
        pass

    def keys(self):
        pass

    def removeNamedItem(self, name):
        pass

    def setNamedItem(self, node):
        pass

    def values(self):
        pass

    def _add_value(self, name, value):
        if isinstance(value, (list, tuple)):
            new_name  = value[0]
            new_value = value[1]
        elif isinstance(value, dict):
            new_name  = value["name"]
            new_value = value["value"]
        elif isinstance(value, str):
            new_name  = name
            new_value = value
        else:
            msg = ("You can't assign a value of type %s to the \"%s\" attribute" %
                   (type(value).__name__, name))
            raise TriadeNodeTypeError(msg)

        self._attrs[name] = TriadeAttribute(new_name, new_value)
        self._len += 1

    def _change_value(self, name, value):
        if isinstance(value, (list, tuple)):
            new_name  = value[0]
            new_value = value[1]

            self._attrs[name].name  = new_name
            self._attrs[name].value = new_value

            self._attrs[new_name] = self._attrs[name]
            del self._attrs[name]
        elif isinstance(value, dict):
            new_name  = value["name"]
            new_value = value["value"]

            self._attrs[name].name  = new_name
            self._attrs[name].value = new_value

            self._attrs[new_name] = self._attrs[name]
            del self._attrs[name]
        elif isinstance(value, str):
            self._attrs[name].value = value
        else:
            msg = ("You can't assign a value of type %s to the \"%s\" key." %
                   (type(value).__name__, name))
            raise TriadeNodeTypeError(msg)

# triade.xml_element.TriadeTextNode
class TriadeTextNode:
    def __init__(self, data):
        self._node = create_text_node(data)

    def __str__(self):
        return self._node.data

    def __repr__(self):
        cls = type(self).__name__
        return "%s(%s)" % (cls, repr(self._node.data))

    @property
    def data(self):
        """The content of the text node as a string."""
        return self._node.data

    @data.setter
    def data(self, value):
        self._node.data = value

    @data.deleter
    def data(self):
        raise NotImplementedError("deleting not allowed.")


# triade.xml_element.TriadeXMLException
class TriadeXMLException(Exception): pass


# triade.xml_element.TriadeNodeTypeError
class TriadeNodeTypeError(TriadeXMLException, TypeError): pass
# triade.xml_element.TriadeNodeValueError
class TriadeNodeValueError(TriadeXMLException, ValueError): pass

# xml.dom.minidom.NamedNodeMap
# xml.dom.minidom.AttributeList

color = create_attribute("color", "green")
#attr2 = create_attribute("tres", "quatro")
size = TriadeAttribute("size", "12")

attribute_list = (xml.dom.minidom.AttributeList(
    {"color": color, "size": size}, None, None)
)

# print("color" in attribute_list)
# del attribute_list["color"]
# print("color" in attribute_list)

attribute_list = TriadeAttributeList({"font": "monospace", "color": "white"}, "xablau")

node_list = TriadeNodeList([{"tag_name": "burger"}, {"tagName": "sandwich"}])
# elem = TriadeElement({"tag_name": "burger"})
# print(elem)
