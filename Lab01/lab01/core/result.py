from dataclasses import dataclass


@dataclass
class Result:
    argument: float
    precision: float
    value: float
    n_terms: int
