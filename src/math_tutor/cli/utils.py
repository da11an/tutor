from typing import Union, Tuple, List, Dict
from time import sleep

class UserChoiceBase:
    def __init__(self, options: Union[Dict[str, str], List[str]]):
        """
        Initialize the UserChoiceBase instance with options.

        Args:
            options (dict or list): A dictionary of options or a list of options.
        """
        self.options = options

    def display_options(self):
        """Display the options to the user."""
        print("  Please select an option:")
        for idx, option in enumerate(self.get_displayable_options(), start=1):
            print(f"    {idx}. {option}")

    def get_displayable_options(self):
        """Get the options to display."""
        raise NotImplementedError("Subclasses should implement this method.")

    def get_choice(self) -> Tuple[str, Union[str, None]]:
        """Get the user's choice from the options."""
        self.display_options()
        
        # Get user input and validate
        while True:
            try:
                choice = int(input("  Enter the number of your choice: "))
                if 1 <= choice <= len(self.get_displayable_options()):
                    return self.process_choice(choice)
                else:
                    print(f"  Please enter a number between 1 and {len(self.get_displayable_options())}.")
            except ValueError:
                print("  Invalid input. Please enter a number.")

    def process_choice(self, choice: int) -> Tuple[str, Union[str, None]]:
        """Process the user's choice and return the selected option."""
        raise NotImplementedError("Subclasses should implement this method.")


class UserChoiceIntRange:
    def __init__(self, min_value: int, max_value: int, prompt: str=None):
        assert isinstance(min_value, int), "Must provide an integer minimum value"
        assert isinstance(max_value, int), "Must provide an integer maximum value"
        self.min_value = min_value
        self.max_value = max_value
        if prompt is None:
            self.prompt = f"Select an integer between {self.min_value} and {self.max_value}"
        else:
            self.prompt = prompt
    
    def get_choice(self) -> Tuple[str, Union[str, None]]:
        """Get the user's choice from the options."""
        
        # Get user input and validate
        while True:
            try:
                choice = int(input(f"{self.prompt}: "))
                if self.min_value <= choice <= self.max_value:
                    return choice
                else:
                    print(f"  Please enter a number between {self.min_value} and {self.max_value}.")
            except ValueError:
                print(f"  Invalid input. Please enter a number between {self.min_value} and {self.max_value}.")
    

class UserChoiceDict(UserChoiceBase):
    def get_displayable_options(self) -> List[str]:
        """Return the keys of the dictionary for display."""
        return list(self.options.keys())

    def process_choice(self, choice: int) -> Tuple[str, str]:
        """Return the selected key and its associated value."""
        selected_key = self.get_displayable_options()[choice - 1]
        return selected_key, self.options[selected_key]


class UserChoiceList(UserChoiceBase):
    def get_displayable_options(self) -> List[str]:
        """Return the list of options for display."""
        return self.options

    def process_choice(self, choice: int) -> Tuple[str, None]:
        """Return the selected option."""
        selected_option = self.get_displayable_options()[choice - 1]
        return selected_option


def count_down(delay=3):
    print(' ....', end='')
    delay = max(1, round(delay))
    for countdown in range(delay):
        print(delay - countdown, end='', flush=True)
        for subcount in range(4):
            print('.', end='', flush=True)
            sleep(0.25)
    print('GO!')

# Example usage
# options_dict = {'Option 1': 'Description 1', 'Option 2': 'Description 2'}
# user_choice_dict = UserChoiceDict(options_dict)
# selected_key, selected_value = user_choice_dict.get_choice()
# print(f"You selected: {selected_key}, with value: {selected_value}")

# options_list = ['Option 1', 'Option 2']
# user_choice_list = UserChoiceList(options_list)
# selected_option, _ = user_choice_list.get_choice()
# print(f"You selected: {selected_option}")
