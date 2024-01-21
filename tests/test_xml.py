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
