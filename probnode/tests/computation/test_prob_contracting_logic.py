from probnode import *
from probnode.probability import *
from probnode.probability.probability_measure import *
from probnode.computation.probability_contracting_logic import *
from typing import List
import pytest


@pytest.mark.parametrize(
    ("input", "expect"),
    [([P(ES(Outcome("sample"))), AdditiveInverseP(ES(Outcome("sample")))
       ], ProbabilityMeasure(None, 0)),
     ([
         P(ES(Outcome("sample1"))) + P(ES(Outcome("sample2"))),
         AdditiveInverseChainP.from_P(P(ES(Outcome("sample1"))) + P(ES(Outcome("sample2"))))
         ], ProbabilityMeasure(None, 0))]
    )
def test_contract_sum_2_nodes(input: List[ProbabilityMeasure], expect: ProbabilityMeasure):
  assert try_contract_sum_2_nodes(input) == expect


@pytest.mark.parametrize(
    ("input", "expect"),
    [([P(ES(Outcome("sample"))), ReciprocalP(ES(Outcome("sample")))], ProbabilityMeasure(None, 1)),
     ([
         P(ES(Outcome("sample1")) & ES(Outcome("sample2"))),
         ReciprocalP.from_P(P(ES(Outcome("sample2"))))
         ], P(ES(Outcome("sample1")) // ES(Outcome("sample2")))),
     ([P(ES(Outcome("sample1"))), P(ES(Outcome("sample2")))
       ], P(ES(Outcome("sample1")) & ES(Outcome("sample2"))))]
    )
def test_contract_product_2_nodes(input: List[ProbabilityMeasure], expect: ProbabilityMeasure):
  assert contract_product_2_nodes(input) == expect


def test_is_or_probability_pattern():
  assert is_or_probability_pattern(
      P(ES(Outcome("x"))), P(ES(Outcome("y"))),
      P(ES(Outcome("x")) & ES(Outcome("y"))).additive_invert()
      ) == True
  assert is_or_probability_pattern(
      P(ES(Outcome("x"))), P(ES(Outcome("yyyy"))),
      P(ES(Outcome("x")) & ES(Outcome("y"))).additive_invert()
      ) == False
  assert is_or_probability_pattern(
      P(ES(Outcome("x"))), P(ES(Outcome("yyyy"))), P(ES(Outcome("x")) & ES(Outcome("y")))
      ) == False


def test_try_contract_or_probability_pattern():
  assert try_contract_or_probability_pattern(
      P(ES(Outcome("x"))), P(ES(Outcome("y"))),
      P(ES(Outcome("x")) & ES(Outcome("y"))).additive_invert()
      ) == P(ES(Outcome("x")) | ES(Outcome("y")))
  assert try_contract_or_probability_pattern(
      P(ES(Outcome("x"))), P(ES(Outcome("yyyy"))),
      P(ES(Outcome("x")) & ES(Outcome("y"))).additive_invert()
      ) == None
  assert try_contract_or_probability_pattern(
      P(ES(Outcome("x"))), P(ES(Outcome("yyyy"))), P(ES(Outcome("x")) & ES(Outcome("y")))
      ) == None


def test_contract_sum_3_nodes():
  assert contract_sum_3_nodes([
      P(ES(Outcome("x"))),
      P(ES(Outcome("y"))),
      P(ES(Outcome("x")) & ES(Outcome("y"))).additive_invert()
      ]) == P(ES(Outcome("x")) | ES(Outcome("y")))
  assert contract_sum_3_nodes([
      P(ES(Outcome("x"))),
      P(ES(Outcome("yyyy"))),
      P(ES(Outcome("x")) & ES(Outcome("y"))).additive_invert()
      ]) == None
  assert contract_sum_3_nodes([
      P(ES(Outcome("x"))),
      P(ES(Outcome("yyyy"))),
      P(ES(Outcome("x")) & ES(Outcome("y")))
      ]) == None
