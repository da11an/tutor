from typing import Tuple, Union, Optional
import random
from math_tutor.utils import timeit_decorator
from typing import NamedTuple
from statistics import mean
from math_tutor.logs.historian import Historian
from math_tutor.data import Performance


history = Historian('history.json')

class MathFact:
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b
        self.symbol = None
        self.ans_name = None
        self.answer = None
        self.session_history = []
        self.quiz_logging = True

    @classmethod
    def from_problem(cls, problem):
        a, symbol, b = problem.split()
        fact_class_options = {
            '+': AdditionFact,
            '-': SubtractionFact,
            'x': MultiplicationFact,
            '/': DivisionFact
        }
        fact_class = fact_class_options.get(symbol, MathFact)
        return fact_class(int(a), int(b))

    def generate(self) -> Tuple[int, int, int]:
        """
        Generate the fact.
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

    @timeit_decorator
    def get_answer(self, show_problem=True) -> int:
        while True:
            if show_problem:
                user_input = input(f"    {self.problem} = ")
            else:
                user_input = input(f"    Answer: ")
            if user_input.strip() == "":  # Check for empty input
                print("Input cannot be empty. Please enter a valid integer.")
                continue
            try:
                return int(user_input)  # Try converting to an integer
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def quiz(self, show_problem=True, user=None):
        answer, timing = self.get_answer(show_problem)
        perf = Performance(self.check_input(answer), timing, answer, self.problem, user)
        if self.quiz_logging:
            history.add_entry(perf)
        self.session_history.append(perf)

    @property
    def performance(self) -> Performance[NamedTuple]:
        if len(self.session_history) > 1:
            mean_timing = mean(result.timing for result in self.session_history)
            mean_correctness = mean(map(int, (result.correct for result in self.session_history)))
            answers = [result.answer for result in self.session_history]
            problem = [result.problem for result in self.session_history][0]
            user = [result.user for result in self.session_history][0]
            return Performance(mean_correctness, mean_timing, answers, problem, user)
        elif len(self.session_history) == 0:
            return None
        else:
            return self.session_history[-1]

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

