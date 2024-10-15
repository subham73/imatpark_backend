def calculate_average(values):
    """
    Calculate and return the average of a list of values.
    """
    if not values:
        return 0
    return sum(values) / len(values)
