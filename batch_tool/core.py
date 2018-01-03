"""Original bounded concept exercise with supplied synthetic data only."""


def fields(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= value.keys() or not value.keys() <= set(required) | set(optional):
        raise ValueError("Unexpected or missing object fields")


def integer(value, low=0, high=10**12):
    if type(value) is not int or not low <= value <= high:
        raise ValueError("Integer outside the supported range")
    return value


def label(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 80 or any(ord(c) < 32 for c in value):
        raise ValueError("Expected a nonblank label of at most 80 characters")
    return value.strip()


def sequence(value, maximum):
    if not isinstance(value, list) or len(value) > maximum:
        raise ValueError("Expected a bounded list")
    return value

def evaluate(data):
    fields(data, ("records", "max_records", "max_bytes"))
    limit, budget = integer(data["max_records"], 1, 100), integer(data["max_bytes"], 1, 10**6)
    batches, current, size, seen = [], [], 0, set()
    for record in sequence(data["records"], 1000):
        fields(record, ("id", "bytes"))
        ident, amount = label(record["id"]), integer(record["bytes"], 0, budget)
        if ident in seen:
            raise ValueError("Duplicate record ID")
        seen.add(ident)
        if current and (len(current) == limit or size + amount > budget):
            batches.append({"ids": current, "bytes": size})
            current, size = [], 0
        current.append(ident)
        size += amount
    if current:
        batches.append({"ids": current, "bytes": size})
    return {"batches": batches}
