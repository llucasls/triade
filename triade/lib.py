import sys
import json

import yaml
import toml


parsers = {
    "json": json.loads,
    "yaml": yaml.safe_load,
    "toml": toml.loads,
}

writers = {
    "json": json.dumps,
    "yaml": yaml.safe_dump,
    "toml": toml.dumps,
}


def parse(input_data: str, data_format: str) -> object:
    if data_format not in parsers:
        raise ValueError("format not recognized")

    output_data = parsers[data_format](input_data)

    if data_format != "json":
        output_data = json.loads(json.dumps(output_data))

    return output_data


def write(data: object, data_format: str) -> str:
    if data_format not in writers:
        raise ValueError("format not recognized")

    return writers[data_format](data).strip()
