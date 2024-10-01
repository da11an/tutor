from typing import List
from random import sample, shuffle
from copy import deepcopy
from math_tutor.core.mathfacts import (
        MathFact,
        AdditionFact,
        SubtractionFact,
        MultiplicationFact,
        DivisionFact,
    )

class FactFamily:
    def __init__(self, value: int, min_operand: int = None, max_operand: int = None):
        self.value = value
        self.min_operand = min_operand
        self.max_operand = max_operand
        self._facts = []

    @property
    def facts(self) -> List[MathFact]:
        """This should always return populated facts for subclasses."""
        if not self._facts:
            self._facts = self.generate_facts()  # Generate facts if not already populated
        return self._facts

    @property
    def len(self) -> int:
        return len(self._facts)

    def generate_facts(self) -> List:
        """
        Generate all facts related to the given value. This method should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def from_addition(cls, instance1, instance2):
        # Creates a new instance from the combined lists
        return cls(value=(instance1.value, instance2.value), min_operand=None, max_operand=None, facts=instance1.facts+instance2.facts)

    def __add__(self, other):
        if isinstance(other, AdditionFactFamily):
            # Create a new instance with the combined lists
            new_list = self.facts + other.facts
            return self.from_addition(self, other)
        return NotImplemented

    def append(self, fact: AdditionFact):
        """Append a single AdditionFact to the facts list."""
        self._facts.append(fact)

    def sample(self, k) -> 'FactFamily':
        k = min(k, self.len)
        new_instance = deepcopy(self)
        new_instance._facts = sample(self._facts, k)
        return new_instance

    def sample_fact(self, k) -> 'MathFact':
        return sample(self._facts, 1)[0]


    def shuffle(self):
        shuffle(self._facts)

    @property
    def problems(self) -> List:
        return [item.problem for item in self.facts]

    @property
    def print_problems(self) -> str:
        print('    ' + '       '.join(self.problems))

    @property
    def len(self) -> int:
        return len(self.facts)
    
    def quiz(self, count=1, shuffle=False):
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(answer={self.value}, max_operand={self.max_operand}, min_operand={self.min_operand}, facts={self.facts})"


class AdditionFactFamily(FactFamily):
    def __init__(self, value: int, min_operand: int = None, max_operand: int = None, facts: List[AdditionFact] = None):
        super().__init__(value, min_operand, max_operand)  # Initialize the base class
        self._facts = facts if facts is not None else self.generate_facts()
        
    def generate_facts(self) -> List[AdditionFact]:
        """
        Generate all addition facts that result in the given sum.
        """
        facts = []

        for a in range(1, self.value):
            b = self.value - a  # Calculate b to satisfy a + b = self.value
            if self.max_operand is None or (a <= self.max_operand and b <= self.max_operand):
                if self.min_operand is None or (a >= self.min_operand and b >= self.min_operand):
                    facts.append(AdditionFact(a, b))  # Assuming AdditionFact is a defined class
 
        return facts


class SubtractionFactFamily(FactFamily):
    def __init__(self, value: int, min_operand: int = None, max_operand: int = None, facts: List[SubtractionFact] = None):
        super().__init__(value, min_operand, max_operand)  # Initialize the base class
        self._facts = facts if facts is not None else self.generate_facts()
        
    def generate_facts(self) -> List[AdditionFact]:
        """
        Generate all subtraction facts that relate to the given difference and subtracted number.
        """
        facts = []

        for b in range(1, self.value):
            a = self.value + b  # Calculate b to satisfy a + b = self.value
            if self.max_operand is None or (a <= self.max_operand and b <= self.max_operand):
                if self.min_operand is None or (a >= self.min_operand and b >= self.min_operand):
                    facts.append(SubtractionFact(a, b))  # Assuming AdditionFact is a defined class
 
        return facts


class MultiplicationFactFamily(FactFamily):
    def __init__(self, value: int, min_operand: int = None, max_operand: int = None, facts: List[MultiplicationFact] = None):
        super().__init__(value, min_operand, max_operand)  # Initialize the base class
        self._facts = facts if facts is not None else self.generate_facts()
        
    def generate_facts(self) -> List[MultiplicationFact]:
        """
        Generate all multiplication facts that result in the given product.
        """
        facts = []
        for i in range(1, self.value + 1):
            if self.value % i == 0:
                a = i
                b = self.value // i
                if self.max_operand is None or (a <= self.max_operand and b <= self.max_operand):
                    if self.min_operand is None or (a >= self.min_operand and b >= self.min_operand):
                        facts.append(MultiplicationFact(a, b))
        return facts


class DivisionFactFamily(FactFamily):
    def __init__(self, value: int, min_operand: int = None, max_operand: int = None, facts: List[DivisionFact] = None):
        super().__init__(value, min_operand, max_operand)  # Initialize the base class
        self._facts = facts if facts is not None else self.generate_facts()
        
    def generate_facts(self) -> List[MultiplicationFact]:
        """
        Generate all division facts for a given quotient.
        """
        facts = []
        for b in range(self.min_operand, self.max_operand + 1):
            a = b * self.value
            if self.max_operand is None or (a <= (self.max_operand * self.max_operand) and self.value <= self.max_operand):
                if self.min_operand is None or (a >= self.min_operand and self.value >= self.min_operand):
                    facts.append(DivisionFact(a, b))

        return facts
