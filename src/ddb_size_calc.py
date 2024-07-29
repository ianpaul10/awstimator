import base64
import decimal

BASE_LOGICAL_SIZE_OF_NESTED_TYPES = 1
LOGICAL_SIZE_OF_EMPTY_DOCUMENT = 3


def determine_largest_attribute(attribute_sizes):
    largest_attribute = None
    max_size = 0

    for current_attribute, sizes in attribute_sizes.items():
        current_size = sizes["total"]
        if current_size > max_size:
            max_size = current_size
            largest_attribute = current_attribute

    return largest_attribute


def calculate_item_size_in_bytes(item):
    sizes = {}
    total_size = 0

    for name, value in item.items():
        size = {
            "sizeOfName": len(name.encode("utf-8")),
            "attributeSize": calculate_attribute_size_in_bytes(value),
        }
        size["total"] = size["sizeOfName"] + size["attributeSize"]
        total_size += size["total"]
        sizes[name] = size

    return {"size": total_size, "sizes": sizes}


def calculate_attribute_size_in_bytes(attr):
    if not attr:
        return 0

    # Binary
    if "B" in attr:
        return len(base64.b64decode(attr["B"]))

    # String
    if "S" in attr:
        return len(attr["S"].encode("utf-8"))

    # Number
    if "N" in attr:
        return calculate_number_size_in_bytes(attr["N"])

    # BinarySet
    if "BS" in attr:
        return sum(len(base64.b64decode(b)) for b in attr["BS"])

    # StringSet
    if "SS" in attr:
        return sum(len(s.encode("utf-8")) for s in attr["SS"])

    # NumberSet
    if "NS" in attr:
        return sum(calculate_number_size_in_bytes(n) for n in attr["NS"])

    # Boolean
    if "BOOL" in attr:
        return 1

    # Null
    if "NULL" in attr:
        return 1

    # Map
    if "M" in attr:
        size = LOGICAL_SIZE_OF_EMPTY_DOCUMENT
        for name, value in attr["M"].items():
            size += len(name.encode("utf-8"))
            size += calculate_attribute_size_in_bytes(value)
            size += BASE_LOGICAL_SIZE_OF_NESTED_TYPES
        return size

    # List
    if "L" in attr:
        size = LOGICAL_SIZE_OF_EMPTY_DOCUMENT
        for item in attr["L"]:
            size += calculate_attribute_size_in_bytes(item)
            size += BASE_LOGICAL_SIZE_OF_NESTED_TYPES
        return size

    raise ValueError(f"unknown data type in {attr}")


def calculate_number_size_in_bytes(n):
    dec = decimal.Decimal(n)
    if dec == 0:
        return 1
    fixed = format(dec, "f")
    size = measure(fixed.replace("-", "")) + 1
    if fixed.startswith("-"):
        size += 1
    return min(size, 21)


def measure(n):
    if "." in n:
        p0, p1 = n.split(".")
        if p0 == "0":
            p0 = ""
            p1 = zeros(p1, True)
        if len(p0) % 2 != 0:
            p0 = "Z" + p0
        if len(p1) % 2 != 0:
            p1 += "Z"
        return measure(p0 + p1)
    n = zeros(n, True, True)
    return (len(n) + 1) // 2


def zeros(n, left, right=False):
    while left and n.startswith("00"):
        n = n[2:]
    while right and n.endswith("00"):
        n = n[:-2]
    return n
