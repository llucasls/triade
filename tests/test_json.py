from triade.lib import parse, write


class TestJSON:
    "Test JSON format"

    def test_write(self):
        "return JSON string from Python object"

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
