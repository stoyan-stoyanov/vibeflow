"""
Data parsing example for the VIBE decorator.

This script demonstrates how to use the @vibe decorator to generate
a function that parses a string of data, extracts numerical values,
and calculates their average.
"""

from vibeflow import vibe


@vibe
def calculate_average_from_data(data: str) -> float:
    """Parses a multi-line string where each line contains 'item_name,value'.

    It extracts the numerical values, calculates their average, and returns the result.
    Lines with non-numeric values or malformed data are ignored.

    Args:
        data: A string containing the data to parse, with each entry on a new line.

    Returns:
        The average of the extracted numerical values.
    """
    pass


if __name__ == "__main__":
    print("--- VIBE Data Parsing Example ---")

    sample_data = """
    apples,0.5
    oranges,0.75
    milk,3.50
    bread,2.25
    invalid_data
    eggs,4.0
    sugar,not_a_number
    flour,1.75
    """

    average_price = calculate_average_from_data(sample_data)
    print(f"The average price of all valid items is: ${average_price:.2f}")
    print("ℹ️ The result should be 2.12 ☝️")
