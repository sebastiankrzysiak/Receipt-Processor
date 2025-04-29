import math

def calculate_points(receipt):
    points = 0

    # Rule 1: 1 point for every alphanumeric character in the retailer name
    retailer_name = receipt["retailer"]

    for letter in retailer_name:
        if letter.isalnum():
            points +=1

    # Rule 2: 50 points if the total is a round dollar amount with no cents
    total = float(receipt["total"])
    if total == int(total):
        points += 50
    
    # Rule 3: 25 points if the total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25

    # Rule 4: 5 points for every two items on the receipt
    points += (len(receipt["items"]) // 2) * 5

    # Rule 5: If the trimmed description length is a multiple of 3, 
    # add ceil(price * 0.2) to the points
    for item in receipt["items"]:
        desc = item["shortDescription"].strip()
        if len(desc) % 3 == 0:
            price = float(item["price"])
            points += math.ceil(price * 0.2)
    
    # Rule 6: 6 points if the day of the purchase date is odd
    year, month, day = receipt["purchaseDate"].split("-")
    if int(day) % 2 == 1:
        points += 6
    
    # Rule 7: 10 points if the time is between 2:00pm and 4:00pm
    hour, minute = receipt["purchaseTime"].split(":")
    hour = int(hour)
    minute = int(minute)
    total_minutes = hour * 60 + minute
    if 14 * 60 < total_minutes < 16 * 60:
        points += 10

    return points