from typing import Dict, Any


def remove_ellipsis_fields(data: Dict[Any, Any]) -> Dict[Any, Any]:
    new_data = {}
    for key, value in list(data.items()):
        if value != ...:
            new_data[key] = value
    return new_data
