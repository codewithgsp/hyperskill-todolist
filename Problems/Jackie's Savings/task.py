def final_deposit_amount(*interests, amount=1000):
    for interest in interests:
        amount = ((interest / 100) + 1) * amount
    return round(amount, 2)
