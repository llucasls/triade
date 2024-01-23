import triade.xml_lib as xml


class TestDocument:
    """Test the TriadeDocument class"""

    def test_create_new_instance(self):
        """test_class :: return object from a dictionary"""

        input_data = {
            "tagName": "distributions",
            "childNodes": [
                {
                    "tagName": "Debian",
                    "attributes": {"packageManager": "apt"}
                },
                {
                    "tagName": "Arch Linux",
                    "attributes": {"packageManager": "pacman"}
                }
            ]
        }

        with xml.TriadeDocument(input_data) as document:
            assert document

    def test_create_document_with_int_input(self):
        """test_class ::
        return object with int values as child nodes"""

        input_data = {
            "tagName": "commodities",
            "childNodes": [
                {
                    "tagName": "commodity",
                    "attributes": {"name": "petroleum"},
                    "childNodes": [78]
                },
                {
                    "tagName": "commodity",
                    "attributes": {"name": "coffee"},
                    "childNodes": [185]
                },
                {
                    "tagName": "commodity",
                    "attributes": {"name": "gold"},
                    "childNodes": [2_023]
                },
                {
                    "tagName": "commodity",
                    "attributes": {"name": "cocoa"},
                    "childNodes": [4_603]
                }
            ]
        }

        with xml.TriadeDocument(input_data) as document:
            assert document

    def test_create_document_with_float_input(self):
        """test_class ::
        return object with float values as child nodes"""

        input_data = {
            "tagName": "programmingLanguages",
            "childNodes": [
                {
                    "tagName": "language",
                    "attributes": {"name": "Python"},
                    "childNodes": [13.97]
                },
                {
                    "tagName": "language",
                    "attributes": {"name": "C"},
                    "childNodes": [11.44]
                },
                {
                    "tagName": "language",
                    "attributes": {"name": "PHP"},
                    "childNodes": [1.79]
                },
                {
                    "tagName": "language",
                    "attributes": {"name": "Rust"},
                    "childNodes": [0.79]
                }
            ]
        }

        with xml.TriadeDocument(input_data) as document:
            assert document

    def test_create_document_with_int_attributes(self):
        """test_class ::
        return object with int values as attribute values"""

        input_data = {
            "tagName": "nationalTeam",
            "childNodes": [
                {
                    "tagName": "team",
                    "attributes": {"name": "Argentina", "ranking": 1},
                },
                {
                    "tagName": "team",
                    "attributes": {"name": "France", "ranking": 2},
                },
                {
                    "tagName": "team",
                    "attributes": {"name": "Brazil", "ranking": 5},
                },
                {
                    "tagName": "team",
                    "attributes": {"name": "Germany", "ranking": 16},
                }
            ]
        }

        with xml.TriadeDocument(input_data) as document:
            assert document

    def test_create_document_with_float_attributes(self):
        """test_class ::
        return object with float values as attribute values"""

        input_data = {
            "tagName": "nationalTeam",
            "childNodes": [
                {
                    "tagName": "team",
                    "attributes": {"name": "Argentina", "totalPoints": 1855.2},
                },
                {
                    "tagName": "team",
                    "attributes": {"name": "France", "totalPoints": 1845.44},
                },
                {
                    "tagName": "team",
                    "attributes": {"name": "Brazil", "totalPoints": 1784.09},
                },
                {
                    "tagName": "team",
                    "attributes": {"name": "Germany", "totalPoints": 1631.22},
                }
            ]
        }

        with xml.TriadeDocument(input_data) as document:
            assert document

    def test_create_document_with_null_list_of_child_nodes(self):
        """test_class ::
        return object with None as list of child nodes"""

        input_data = {"tagName": "GameConfig", "childNodes": None}

        with xml.TriadeDocument(input_data) as document:
            assert document

    def test_create_document_with_null_child_nodes(self):
        """test_class ::
        return object with None as child nodes"""

        input_data = {"tagName": "GameConfig", "childNodes": [None, None]}

        with xml.TriadeDocument(input_data) as document:
            assert document

    def test_create_document_with_null_attribute_list(self):
        """test_class ::
        return object with None as attribute list"""

        input_data = {"tagName": "GameConfig", "attributes": None}

        with xml.TriadeDocument(input_data) as document:
            assert document

    def test_create_document_with_null_attributes(self):
        """test_class ::
        return object with None as attribute values"""

        input_data = {"tagName": "GameConfig", "attributes": {"comment": None}}

        with xml.TriadeDocument(input_data) as document:
            assert document
