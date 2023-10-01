def calculate_variance_string(numbers):
    n = len(numbers)  # Count the numbers

    mean = sum(numbers) / n  # Calculate the mean

    # Calculate the sum of squares
    Sxx = sum([num ** 2 for num in numbers]) - n * mean ** 2
    Sxx = round(Sxx, 2)  # Round Sxx to 2 decimal places

    # Calculate the variance
    variance = Sxx / (n - 1)
    variance = round(variance, 2)  # Round variance to 2 decimal places

    # Create the string representation with loop
    Sxx_str = "S_{{xx}} = ( " + ' + '.join([str(num) + "^2" for num in numbers]) + " ) - ( ( " + ' + '.join([str(num) for num in numbers]) + f" )^2 / {n} ) = {Sxx}"
    variance_str = f"V = S_{{xx}}/(n-1) = {Sxx}/({n}-1) = {variance}"

    return Sxx_str, variance_str

def sum_probabilities(px_list, start, stop=None):
    # Subsetting the list from the start index to the stop index
    subset_px_list = px_list[start:stop]

    # Calculating the sum
    total = round(sum(subset_px_list), 3)

    # Creating the string with the "+" sign
    sum_string = "+".join(str(round(px, 3)) for px in subset_px_list)

    return total, sum_string

def signLT12 (x):
    temp = 1
    if x > 0.5:
        temp = -1
    return temp