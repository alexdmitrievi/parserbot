def filter_lots(lots):
    result = []
    for lot in lots:
        if lot["purpose"] in ["ИЖС", "СНТ"] and lot["price"] <= 3000000:
            result.append(lot)
    return result