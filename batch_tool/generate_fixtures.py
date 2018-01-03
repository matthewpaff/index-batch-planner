"""Original case templates with independently supplied expected results."""
import copy
import re

TEMPLATES = [('split batches at the supplied record-count limit', {'records': [{'id': 'a{n}', 'bytes': 2}, {'id': 'b{n}', 'bytes': 3}], 'max_records': 1, 'max_bytes': 5}, {'batches': [{'ids': ['a{n}'], 'bytes': 2}, {'ids': ['b{n}'], 'bytes': 3}]}), ('accept an exact supplied byte-budget boundary', {'records': [{'id': 'a{n}', 'bytes': 2}, {'id': 'b{n}', 'bytes': 3}], 'max_records': 5, 'max_bytes': 5}, {'batches': [{'ids': ['a{n}', 'b{n}'], 'bytes': 5}]}), ('flush before a record exceeds the remaining byte budget', {'records': [{'id': 'a{n}', 'bytes': 4}, {'id': 'b{n}', 'bytes': 4}], 'max_records': 5, 'max_bytes': 5}, {'batches': [{'ids': ['a{n}'], 'bytes': 4}, {'ids': ['b{n}'], 'bytes': 4}]}), ('reject a single record larger than the budget', {'records': [{'id': 'a{n}', 'bytes': 6}], 'max_records': 5, 'max_bytes': 5}, None), ('return no batches for empty input', {'records': [], 'max_records': 1, 'max_bytes': 1}, {'batches': []})]


def make_case(index):
    description, source, expected = copy.deepcopy(TEMPLATES[index % len(TEMPLATES)])
    def fill(value):
        if isinstance(value, str):
            if re.fullmatch(r"@i[+]\d+", value):
                return index + int(value[3:])
            return value.replace("{n}", str(index))
        if isinstance(value, list):
            return [fill(item) for item in value]
        if isinstance(value, dict):
            return {fill(key): fill(item) for key, item in value.items()}
        return value
    case = {"id": "batch-{:04d}".format(index), "description": description, "input": fill(source)}
    case.update({"expected_error": True} if expected is None else {"expected": fill(expected)})
    return case
