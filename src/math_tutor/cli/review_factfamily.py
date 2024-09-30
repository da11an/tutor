import sys
from math_tutor.core.factfamily import MultiplicationFactFamily

def get_valid_integer(prompt: str, max_attempts: int = 3) -> int:
    """
    Prompt the user for a valid integer input.
    
    :param prompt: The prompt message to display to the user.
    :param max_attempts: Maximum number of attempts to get valid input.
    :return: A valid integer input from the user.
    """
    attempts = 0
    while attempts < max_attempts:
        try:
            user_input = input(prompt)
            value = int(user_input)
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            attempts += 1
    print("Too many invalid attempts. Exiting.")
    sys.exit(1)

def review_fact_family():
    """
    Main function to review a multiplication fact family with the student.
    """
    print("Hi, what multiplication fact family would you like to review? (For example, 12).")
    max_operand = get_valid_integer("Max operand value: ")
    product = get_valid_integer("Enter the product number to review: ")

    # Create the fact family
    fact_family = MultiplicationFactFamily(product, 2, max_operand)
    
    print(f"Press ENTER to view each multiplication fact\n")
    
    for fact in fact_family.facts:
        print(f"{fact.a} x {fact.b}")
        input(f"")

    print(f"Those are the factors of {product} for factors of {max_operand} or less.")
    print("Review complete. Goodbye!")

if __name__ == "__main__":
    review_fact_family()

