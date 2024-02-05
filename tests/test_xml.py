import triade.xml_lib as xml


class TestDocument:
    """Test the TriadeDocument class"""

    def test_create_new_instance(self):
        """test_class :: create document from a dictionary"""

        input_data = {
            "tagName": "distributions",
            "childNodes": [
                {
                    "tagName": "distro",
                    "attributes": {"name": "Debian", "packageManager": "apt"}
                },
                {
                    "tagName": "distro",
                    "attributes": {"name": "Arch Linux", "packageManager": "pacman"}
                }
            ]
        }

        with open("tests/fixtures/test_xml/doc01.xml", "r") as file:
            expected_output = file.read()

        with xml.TriadeDocument(input_data) as document:
            assert document
            assert document.toprettyxml() == expected_output

    def test_create_new_instance_with_aliases(self):
        """test_class ::
        create document using tag_name and child_nodes as aliases"""

        input_data = {
            "tag_name": "distributions",
            "child_nodes": [
                {
                    "tag_name": "distro",
                    "attributes": {"name": "Ubuntu", "packageManager": "apt"}
                },
                {
                    "tag_name": "distro",
                    "attributes": {"name": "Manjaro", "packageManager": "pacman"}
                }
            ]
        }

        with open("tests/fixtures/test_xml/doc02.xml", "r") as file:
            expected_output = file.read()

        with xml.TriadeDocument(input_data) as document:
            assert document
            assert document.toprettyxml() == expected_output

    def test_create_document_with_int_input(self):
        """test_class ::
        create document with int values as child nodes"""

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

        with open("tests/fixtures/test_xml/doc03.xml", "r") as file:
            expected_output = file.read()

        with xml.TriadeDocument(input_data) as document:
            assert document
            assert document.toprettyxml() == expected_output

    def test_create_document_with_float_input(self):
        """test_class ::
        create document with float values as child nodes"""

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

        with open("tests/fixtures/test_xml/doc04.xml", "r") as file:
            expected_output = file.read()

        with xml.TriadeDocument(input_data) as document:
            assert document
            assert document.toprettyxml() == expected_output

    def test_create_document_with_int_attributes(self):
        """test_class ::
        create document with int values as attribute values"""

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

        with open("tests/fixtures/test_xml/doc05.xml", "r") as file:
            expected_output = file.read()

        with xml.TriadeDocument(input_data) as document:
            assert document
            assert document.toprettyxml() == expected_output

    def test_create_document_with_float_attributes(self):
        """test_class ::
        create document with float values as attribute values"""

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

        with open("tests/fixtures/test_xml/doc06.xml", "r") as file:
            expected_output = file.read()

        with xml.TriadeDocument(input_data) as document:
            assert document
            assert document.toprettyxml() == expected_output

    def test_create_document_with_null_list_of_child_nodes(self):
        """test_class ::
        create document with None as list of child nodes"""

        input_data = {"tagName": "GameConfig", "childNodes": None}

        with open("tests/fixtures/test_xml/doc07.xml", "r") as file:
            expected_output = file.read()

        with xml.TriadeDocument(input_data) as document:
            assert document
            assert document.toprettyxml() == expected_output

    def test_create_document_with_null_child_nodes(self):
        """test_class ::
        create document with None as child nodes"""

        input_data = {"tagName": "GameConfig", "childNodes": [None, None]}

        with open("tests/fixtures/test_xml/doc08.xml", "r") as file:
            expected_output = file.read()

        with xml.TriadeDocument(input_data) as document:
            assert document
            assert document.toprettyxml() == expected_output

    def test_create_document_with_null_attribute_list(self):
        """test_class ::
        create document with None as attribute list"""

        input_data = {"tagName": "GameConfig", "attributes": None}

        with open("tests/fixtures/test_xml/doc09.xml", "r") as file:
            expected_output = file.read()

        with xml.TriadeDocument(input_data) as document:
            assert document
            assert document.toprettyxml() == expected_output

    def test_create_document_with_null_attributes(self):
        """test_class ::
        create document with None as attribute values"""

        input_data = {"tagName": "GameConfig", "attributes": {"comment": None}}

        with open("tests/fixtures/test_xml/doc10.xml", "r") as file:
            expected_output = file.read()

        with xml.TriadeDocument(input_data) as document:
            assert document
            assert document.toprettyxml() == expected_output

    def test_create_object_from_document(self):
        """test_class :: create dictionary from an XML document"""

        with open("tests/fixtures/test_xml/doc11.xml", "r") as file:
            intput_data = file.read()

        expected_output = {
            "tagName": "distributions",
            "childNodes": [
                {
                    "tagName": "distro",
                    "attributes": {"name": "Linux Mint", "packageManager": "apt"}
                },
                {
                    "tagName": "distro",
                    "attributes": {"name": "EndeavourOS", "packageManager": "pacman"}
                }
            ]
        }

        with xml.TriadeDocument.fromxml(intput_data) as document:
            assert document.data == expected_output
            assert isinstance(document, xml.TriadeDocument)
