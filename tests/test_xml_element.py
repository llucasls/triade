import triade.xml_lib as xml


class TestElement:
    """Test the TriadeElement class"""

    def test_create_new_instance(self):
        """test_class :: create element from a dictionary"""

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
            file.readline()
            expected_output = file.read()

        with xml.TriadeDocument({"tagName": "distributions"}) as document:
            element = xml.TriadeElement(input_data, document=document)
            assert element
            assert element.toprettyxml() == expected_output

    def test_create_element_without_document_object(self):
        """test_class ::
        create element without passing the correspondent
        TriadeDocument object"""

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
            file.readline()
            expected_output = file.read()

        element = xml.TriadeElement(input_data)
        assert element
        assert element.toprettyxml() == expected_output
