from triade.lib import parse, write


class TestJSON:
    "Test JSON format"

    def test_write(self):
        "test_write :: return JSON string from Python object"

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
        output_data = write(input_data, "json")

        expected_output = '[{"sandwich": "Big Mac", "drink": "Coca Cola", "dessert": "vanilla ice cream"}, {"sandwich": "Mc Chicken", "drink": "vanilla McShake", "dessert": "apple pie"}]'

        assert output_data == expected_output

    def test_write_utf_8(self):
        "test_write :: return JSON with unicode characters"

        input_data = [
            {"material": "ônix"},
            {"material": "âmbar"},
            {"material": "topázio"}
        ]
        output_data = write(input_data, "json")

        expected_output = '[{"material": "ônix"}, {"material": "âmbar"}, {"material": "topázio"}]'

        assert output_data == expected_output

    def test_parse(self):
        "test_parse :: return Python object from JSON string"

        input_data = '[{"sandwich": "Big Mac", "drink": "Coca Cola", "dessert": "vanilla ice cream"}, {"sandwich": "Mc Chicken", "drink": "vanilla McShake", "dessert": "apple pie"}]'
        output_data = parse(input_data, "json")

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
