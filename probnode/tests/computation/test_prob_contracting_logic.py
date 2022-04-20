from probnode import *
from probnode.probability import *
from probnode.core.node import *
from probnode.computation.probability_contracting_logic import *
from typing import List
import pytest


@pytest.mark.parametrize(
    ("input", "expect"),
    [([N(P(Event("sample"))), AdditiveInverseNode(P(Event("sample")))], Node(None, 0)),
     ([
         N(P(Event("sample1"))) + N(P(Event("sample2"))),
         AdditiveInverseChainNode.from_node(N(P(Event("sample1"))) + N(P(Event("sample2"))))
         ], Node(None, 0))]
    )
def test_contract_sum_2_nodes(input: List[Node], expect: Node):
  assert try_contract_sum_2_nodes(input) == expect


@pytest.mark.parametrize(("input", "expect"), [
    ([N(P(Event("sample"))), ReciprocalNode(P(Event("sample")))], Node(None, 1)),
    ([
        N(P(Event("sample1")) & P(Event("sample2"))),
        ReciprocalNode.from_node(N(P(Event("sample2"))))
        ], N(P(Event("sample1")) // P(Event("sample2")))),
    ([N(P(Event("sample1"))), N(P(Event("sample2")))], N(P(Event("sample1")) & P(Event("sample2"))))
    ])
def test_contract_product_2_nodes(input: List[Node], expect: Node):
  assert contract_product_2_nodes(input) == expect


def test_is_or_probability_pattern():
  assert is_or_probability_pattern(
      N(P(Event("x"))), N(P(Event("y"))),
      N(P(Event("x")) & P(Event("y"))).additive_invert()
      ) == True
  assert is_or_probability_pattern(
      N(P(Event("x"))), N(P(Event("yyyy"))),
      N(P(Event("x")) & P(Event("y"))).additive_invert()
      ) == False
  assert is_or_probability_pattern(
      N(P(Event("x"))), N(P(Event("yyyy"))), N(P(Event("x")) & P(Event("y")))
      ) == False


def test_try_contract_or_probability_pattern():
  assert try_contract_or_probability_pattern(
      N(P(Event("x"))), N(P(Event("y"))),
      N(P(Event("x")) & P(Event("y"))).additive_invert()
      ) == N(P(Event("x")) | P(Event("y")))
  assert try_contract_or_probability_pattern(
      N(P(Event("x"))), N(P(Event("yyyy"))),
      N(P(Event("x")) & P(Event("y"))).additive_invert()
      ) == None
  assert try_contract_or_probability_pattern(
      N(P(Event("x"))), N(P(Event("yyyy"))), N(P(Event("x")) & P(Event("y")))
      ) == None


def test_contract_sum_3_nodes():
  assert contract_sum_3_nodes([
      N(P(Event("x"))),
      N(P(Event("y"))),
      N(P(Event("x")) & P(Event("y"))).additive_invert()
      ]) == N(P(Event("x")) | P(Event("y")))
  assert contract_sum_3_nodes([
      N(P(Event("x"))),
      N(P(Event("yyyy"))),
      N(P(Event("x")) & P(Event("y"))).additive_invert()
      ]) == None
  assert contract_sum_3_nodes([
      N(P(Event("x"))), N(P(Event("yyyy"))),
      N(P(Event("x")) & P(Event("y")))
      ]) == None
