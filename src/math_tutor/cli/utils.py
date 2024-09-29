

def get_user_choice(options: dict) -> str:
    """
    Display options to the user and get their choice.

    Args:
        options (dict): A dictionary of options where keys are the choices.

    Returns:
        str: The selected value associated with the user's choice.
    """
    # Display the options to the user
    print("\nPlease select an option:")
    for idx, key in enumerate(options.keys(), start=1):
        print(f"{idx}. {key}")

    # Get user input and validate
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                selected_key = list(options.keys())[choice - 1]
                return selected_key, options[selected_key]  # Return the value associated with the selected key
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Example usage
if __name__ == "__main__":
    options = {
        "Option A": "Value A",
        "Option B": "Value B",
        "Option C": "Value C"
    }

    selected_value = get_user_choice(options)
    print(f"You selected: {selected_value}")

