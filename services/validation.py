import re

def validate_receipt(data):
    if not isinstance(data, dict):
        return False
    
    required_fields = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]

    for field in required_fields:
        if not field in data:
            return False
    
    if not isinstance(data["retailer"], str) or not re.fullmatch(r"^[\w\s\-&]+$", data["retailer"]):
        return False

    if not isinstance(data["purchaseDate"], str) or not re.fullmatch(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", data["purchaseDate"]):
        return False

    if not isinstance(data["purchaseTime"], str) or not re.fullmatch(r"^(?:[01]\d|2[0-3]):[0-5]\d$", data["purchaseTime"]):
        return False

    if not isinstance(data["total"], str) or not re.fullmatch(r"^\d+\.\d{2}$", data["total"]):
        return False

    if not isinstance(data["items"], list) or len(data["items"]) == 0:
        return False
    
    for item in data["items"]:
        if not isinstance(item, dict):
            return False
        if not "shortDescription" in item or not "price" in item:
            return False
        if not isinstance(item["shortDescription"], str) or not re.fullmatch(r"^[\w\s\-]+$", item["shortDescription"]):
            return False
        if not isinstance(item["price"], str) or not re.fullmatch(r"^\d+\.\d{2}$", item["price"]):
            return False

    return True

def validate_id(id):
    return isinstance(id, str) and re.fullmatch(r"^\S+$", id) is not None