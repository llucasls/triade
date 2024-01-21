class TriadeXMLException(Exception): pass


class TriadeNodeTypeError(TriadeXMLException, TypeError): pass


class TriadeNodeValueError(TriadeXMLException, ValueError): pass
