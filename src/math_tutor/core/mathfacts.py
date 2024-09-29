from typing import Tuple, Union
import random

class MathFact:
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b
        self.symbol = None
        self.ans_name = None
        self.answer = None

    def generate(self) -> Tuple[int, int, int]:
        """
        Generate the addition fact.
        """
        return self.a, self.b, self.answer

    def check_input(self, answer: Union[int, float]) -> bool:
        """
        Check if the provided answer is correct.
        """
        return answer == self.answer

    @property
    def problem(self) -> str:
        """
        Pose problem in a string format (to be overrideen by subclasses).
        """
        return f'{self.a} {self.symbol} {self.b}'

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(a={self.a}, b={self.b}, {self.ans_name}={self.answer})"


class AdditionFact(MathFact):
    def __init__(self, a: int, b: int):
        super().__init__(a, b)
        self.answer = self.a + self.b
        self.symbol = "+"
        self.ans_name = "sum"


class SubtractionFact(AdditionFact):
    def __init__(self, a: int, b: int):
        super().__init__(a, b)
        self.answer = self.a - self.b
        self.symbol = "-"
        self.ans_name = "difference"


class MultiplicationFact(MathFact):
    def __init__(self, a: int, b: int):
        super().__init__(a, b)
        self.answer = self.a * self.b
        self.symbol = "x"
        self.ans_name = "product"


class DivisionFact(MathFact):
    def __init__(self, a: int, b: int):
        super().__init__(a, b)
        self.answer = self.a / self.b
        self.symbol = "/"
        self.ans_name = "quotient"


# Example Usage
if __name__ == "__main__":
    # Create a multiplication fact
    fact = MultiplicationFact(3, 4)
    
    # Generate the multiplication fact
    print("Generated fact:", fact.generate())  # Output: (3, 4, 12)
    
    # Check some answers
    print("Is 12 correct?", fact.check_input(12))  # Output: True
    print("Is 13 correct?", fact.check_input(13))  # Output: False

