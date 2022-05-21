from typing import List
import pytest
from probnode import p__X_, ES__
from probnode.computation.expand import expand
from probnode.computation.util import _get_alternatives_from_list_of_possible_items
from probnode.probability.event_set import GenericSureEventSet

from probnode.probability.event_set import *


def test_expand_simple_prob_exp(simple_prob_expression1: SimpleEventSet):
  assert expand(p__X_(simple_prob_expression1))[0] == p__X_(simple_prob_expression1)


def test_expand_invert_prob_exp(
    simple_prob_expression1: SimpleEventSet, simple_invert_prob_expression1: SimpleInvertEventSet
    ):
  assert expand(p__X_(simple_invert_prob_expression1)
                )[0] == (p__X_(ES__(GenericSureEventSet())) - p__X_(simple_prob_expression1))


def test_expand_and_prob_exp(
    simple_prob_expression1: SimpleEventSet,
    simple_prob_expression2: SimpleEventSet,
    and_prob_expression: AndEventSet,
    ):
  assert expand(p__X_(and_prob_expression))[0] == (
      p__X_(simple_prob_expression1 // simple_prob_expression2) * p__X_(simple_prob_expression2)
      )
  assert expand(p__X_(and_prob_expression))[1] == (
      p__X_(simple_prob_expression2 // simple_prob_expression1) * p__X_(simple_prob_expression1)
      )


def test_expand_or_prob_exp(
    simple_prob_expression1: SimpleEventSet,
    simple_prob_expression2: SimpleEventSet,
    or_prob_expression: OrEventSet,
    and_prob_expression: AndEventSet,
    ):
  assert expand(p__X_(or_prob_expression))[0] == (
      p__X_(simple_prob_expression1) + p__X_(simple_prob_expression2) - p__X_(and_prob_expression)
      )


def test_expand_conditional_prob_exp(
    simple_prob_expression1: SimpleEventSet, simple_prob_expression2: SimpleEventSet,
    or_prob_expression: OrEventSet, and_prob_expression: AndEventSet,
    conditional_prob_expression: ConditionalEventSet
    ):
  assert expand(p__X_(conditional_prob_expression)
                )[0] == (p__X_(and_prob_expression) / p__X_(simple_prob_expression2))


def test_expand_complex_prob_exp_chain(
    simple_prob_expression1: SimpleEventSet, simple_prob_expression2: SimpleEventSet,
    or_prob_expression: OrEventSet, and_prob_expression: AndEventSet,
    conditional_prob_expression: ConditionalEventSet
    ):
  assert expand(p__X_(and_prob_expression) + p__X_(simple_prob_expression1))[0] == (
      p__X_(simple_prob_expression1 // simple_prob_expression2) * p__X_(simple_prob_expression2) +
      p__X_(simple_prob_expression1)
      )
  assert expand(p__X_(and_prob_expression) - p__X_(simple_prob_expression1))[1] == (
      p__X_(simple_prob_expression2 // simple_prob_expression1) * p__X_(simple_prob_expression1) -
      p__X_(simple_prob_expression1)
      )
  assert expand(p__X_(and_prob_expression) / p__X_(simple_prob_expression1))[1] == (
      p__X_(simple_prob_expression2 // simple_prob_expression1) * p__X_(simple_prob_expression1) /
      p__X_(simple_prob_expression1)
      )
  assert expand(p__X_(and_prob_expression) + p__X_(simple_prob_expression1.invert()))[1] == (
      p__X_(simple_prob_expression2 // simple_prob_expression1) * p__X_(simple_prob_expression1) +
      p__X_(ES__(GenericSureEventSet())) - p__X_(simple_prob_expression1)
      )


@pytest.mark.parametrize(
    ("input", "expect"),
    [([[], [1, 2, 3]], [[1], [2], [3]]), ([[1, 2, 3]], [[1], [2], [3]]),
     ([[1, 2, 3], [], []], [[1], [2], [3]]), ([[1, 2], [3]], [[1, 3], [2, 3]]),
     ([[1, 2], [3], [4, 5, 6]], [[1, 3, 4], [1, 3, 5], [1, 3, 6], [2, 3, 4], [2, 3, 5], [2, 3, 6]])]
    )
def test_get_alternatives_from_list_of_possible_items(
    input: List[List[int]], expect: List[List[int]]
    ):
  assert _get_alternatives_from_list_of_possible_items(input) == expect
