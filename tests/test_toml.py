from triade.lib import parse, write


class TestTOML:
    "Test TOML format"

    def test_write(self):
        "return TOML string from Python object"

        input_data = {"order": [
            {
                "sandwich": "Big Mac",
                "drink": "Coca Cola",
                "dessert": "vanilla ice cream"
            },
            {
                "sandwich": "Mc Chicken",
                "drink": "vanilla McShake",
                "dessert": "apple pie"
            }]
        }
        output_data = write(input_data, "toml")

        expected_output = '''[[order]]
sandwich = "Big Mac"
drink = "Coca Cola"
dessert = "vanilla ice cream"

[[order]]
sandwich = "Mc Chicken"
drink = "vanilla McShake"
dessert = "apple pie"'''

        assert output_data == expected_output

    def test_parse(self):
        "return Python object from TOML string"

        input_data = '''[[order]]
sandwich = "Big Mac"
drink = "Coca Cola"
dessert = "vanilla ice cream"

[[order]]
sandwich = "Mc Chicken"
drink = "vanilla McShake"
dessert = "apple pie"'''
        output_data = parse(input_data, "toml")

        expected_output = {"order": [
            {
                "sandwich": "Big Mac",
                "drink": "Coca Cola",
                "dessert": "vanilla ice cream"
            },
            {
                "sandwich": "Mc Chicken",
                "drink": "vanilla McShake",
                "dessert": "apple pie"
            }]
        }
