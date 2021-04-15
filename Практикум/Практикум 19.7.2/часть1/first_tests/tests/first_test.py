import pytest
import sys

sys.path.append(sys.path[0] + '\\../app') #лезем в соседнюю папку
from calculator import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_multiply_calculation_correctly(self):
        assert self.calc.multiply(self, 2,2) == 4

    def test_division_calculation_correctly(self):
        assert self.calc.division(self, 2,2) == 1

    def test_substraction_calculation_correctly(self):
        assert self.calc.substraction(self, 2,2) == 0

    def test_adding_calculation_correctly(self):
        assert self.calc.adding(self, 2,2) == 4
