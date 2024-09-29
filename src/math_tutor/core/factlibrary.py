from typing import List
from random import sample
from math_tutor.core.mathfacts import AdditionFact, SubtractionFact, MultiplicationFact, DivisionFact
from math_tutor.core.factfamily import AdditionFactFamily, SubtractionFactFamily, MultiplicationFactFamily, DivisionFactFamily

class FactLibrary:
    def __init__(self, min_operand: int = 2, max_operand: int = 12):
        self.max_operand = max_operand
        self.min_operand = min_operand
        #self.fact_library = self.generate_library()

    def generate_library(self) -> List:
        """
        Generate library of facts related to the given value. This method should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def fact_family(self, family):
        return self.fact_library[family] if family in self.fact_library else None

    def sample(self, k):
        return [self.fact_family(family) for family in sample(list(self.fact_library.keys()), k)]

    @property
    def catalog(self):
        return {k: len(v.facts) for k, v in self.fact_library.items()}

    @property
    def problems(self):
        return {k: v.problems for k, v in self.fact_library.items()}

    def problem(self, family=None):
        problem_dict = {k: v.problems for k, v in self.fact_library.items()}
        if family is None:
            return problem_dict
        else:
            return problem_dict[family] if family in problem_dict else None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(max_value={self.max_value}, max_operand={self.max_operand}, fact_family={self.fact_library})"


class AdditionFactLibrary(FactLibrary):
    def __init__(self, min_operand: int = 1, max_operand: int = 12, fact_library: List[AdditionFactFamily] = None):
        super().__init__(min_operand, max_operand)  # Initialize the base class
        self.max_value = None
        self.fact_library = fact_library if fact_library is not None else self.generate_library()

    def generate_library(self) -> dict[AdditionFactFamily]:
        """
        Generate all addition facts that result in the given sum.
        """
        fact_library = {}
        
        if self.max_value is None:
            self.max_value = self.max_operand + self.max_operand
        for value in range(1, self.max_value + 1):
             family = AdditionFactFamily(value, self.min_operand, self.max_operand)
             if family.len > 0:
                 fact_library[value] = family
        return fact_library


class SubtractionFactLibrary(AdditionFactLibrary):
    def __init__(self, min_operand: int = 1, max_operand: int = 12, fact_library: List[SubtractionFactFamily] = None):
        super().__init__(min_operand, max_operand)  # Initialize the base class
        self.max_value = None
        self.fact_library = fact_library if fact_library is not None else self.generate_library()

    def generate_library(self) -> dict[SubtractionFactFamily]:
        """
        Generate all addition facts that result in the given sum.
        """
        fact_library = {}
        
        if self.max_value is None:
            self.max_value = self.max_operand + self.max_operand
        for value in range(1, self.max_value + 1):
             family = SubtractionFactFamily(value, self.min_operand, self.max_operand)
             if family.len > 0:
                 fact_library[value] = family
        return fact_library


class MultiplicationFactLibrary(FactLibrary):
    def __init__(self, min_operand: int = 2, max_operand: int = 12, fact_library: List[MultiplicationFactFamily] = None):
        super().__init__(min_operand, max_operand)  # Initialize the base class
        self.max_value = None
        self.fact_library = fact_library if fact_library is not None else self.generate_library()

    def generate_library(self) -> dict[MultiplicationFactFamily]:
        """
        Generate all multiplication facts that result in the given product.
        """
        fact_library = {}
        
        if self.max_value is None:
            self.max_value = self.max_operand * self.max_operand
        for value in range(1, self.max_value + 1):
             family = MultiplicationFactFamily(value, self.min_operand, self.max_operand)
             if family.len > 0:
                 fact_library[value] = family
        return fact_library


class DivisionFactLibrary(FactLibrary):
    def __init__(self, min_operand: int = 2, max_operand: int = 12, fact_library: List[DivisionFactFamily] = None):
        super().__init__(min_operand, max_operand)  # Initialize the base class
        self.max_value = None
        self.fact_library = fact_library if fact_library is not None else self.generate_library()

    def generate_library(self) -> dict[MultiplicationFactFamily]:
        """
        Generate all division facts that result in the given quotient.
        """
        fact_library = {}
        
        if self.max_value is None:
            self.max_value = self.max_operand * self.max_operand
        for value in range(self.min_operand, self.max_value + 1):
             family = DivisionFactFamily(value, self.min_operand, self.max_operand)
             if family.len > 0:
                 fact_library[value] = family
        return fact_library
