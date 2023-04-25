from triade.lib import parse, write


class TestYAML:
    "Test YAML format"

    def test_write(self):
        "return YAML string from Python object"

        input_data = [
            {
                "sandwich": "Big Mac",
                "drink": "Coca Cola",
                "dessert": "vanilla ice cream",
            },
            {
                "sandwich": "Mc Chicken",
                "drink": "vanilla McShake",
                "dessert": "apple pie",
            },
        ]
        output_data = write(input_data, "yaml")
        expected_output = """- dessert: vanilla ice cream
  drink: Coca Cola
  sandwich: Big Mac
- dessert: apple pie
  drink: vanilla McShake
  sandwich: Mc Chicken"""

        assert output_data == expected_output

    def test_parse(self):
        "return Python object from YAML string"

        input_data = """- dessert: vanilla ice cream
  drink: Coca Cola
  sandwich: Big Mac
- dessert: apple pie
  drink: vanilla McShake
  sandwich: Mc Chicken"""
        output_data = parse(input_data, "yaml")
        expected_output = [
            {
                "sandwich": "Big Mac",
                "drink": "Coca Cola",
                "dessert": "vanilla ice cream",
            },
            {
                "sandwich": "Mc Chicken",
                "drink": "vanilla McShake",
                "dessert": "apple pie",
            },
        ]

        assert output_data == expected_output
