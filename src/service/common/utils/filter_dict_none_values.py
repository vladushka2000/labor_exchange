from typing import Any


def filter_dict_none_values(values_to_update: dict[str, Any]) -> dict[str, Any]:
    keys = list(
        filter(
            lambda key: values_to_update[key] is not None,
            values_to_update
        )
    )

    filtered_values = {}

    for key in keys:
        filtered_values[key] = values_to_update[key]

    return filtered_values
