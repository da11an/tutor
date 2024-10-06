from typing import NamedTuple, Union


class Performance(NamedTuple):
    correct: Union[bool, float]
    timing: float
    answer: Union[int, list[int]]
    problem: str
    user: str