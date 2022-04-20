from collections import Counter
from typing import List, Tuple
import pytest
from probnode import *
from probnode.computation.contract import *


def test_contract():
  sure_prob = P(SureEvent())
  prob_x = P(Event("x"))
  prob_y = P(Event("y"))
  prob_z = P(Event("z"))
  prob_x_and_y = P(prob_x & prob_y)
  prob_y_and_x = P(prob_y & prob_x)
  prob_x_or_y = P(prob_x | prob_y)
  node_x_and_y = Node(prob_x_and_y)
  node_y_and_x = Node(prob_y_and_x)
  node_y_when_x = N(P(prob_y // prob_x))
  node_x_when_y = N(P(prob_x // prob_y))

  chain_1 = N(prob_x) + N(prob_y) - N(prob_x_and_y)
  chain_2 = chain_1 + N(sure_prob)
  chain_3 = N(prob_x) - N(prob_x_and_y) + N(prob_y)
  chain_4 = N(prob_x) - N(prob_x_and_y) + N(prob_y) * N(prob_z) + N(prob_y)
  chain_5 = N(prob_x) - N(prob_x_and_y) + N(prob_y) * N(prob_z) + N(prob_y) - N(prob_y)
  chain_6 = N(prob_x) - N(prob_x_and_y) + N(prob_y) * N(prob_z) + N(prob_y) - N(
      prob_y
      ) + N(prob_x) * N(prob_y) * node_y_when_x

  assert contract(SumNode()) == SumNode()
  assert contract(chain_1) == N(prob_x_or_y)
  assert contract(chain_2) == (N(sure_prob) + N(prob_x_or_y))
  assert contract(chain_3) == N(prob_x_or_y)
  assert contract(chain_4) == N(prob_y) * N(prob_z) + N(prob_x_or_y)
  assert contract(chain_5) == N(prob_y) * N(prob_z) + N(prob_x) - N(prob_x_and_y)
  assert contract(chain_6).is_permutation_of(
      N(prob_y) * N(prob_z) + N(prob_x) - N(prob_x_and_y) + N(prob_y) * node_y_and_x
      )


def test_remove_same_exp_in_simple_vs_and_prob_lists():
  prob_x = P(Event("x"))
  prob_y = P(Event("y"))
  prob_z = P(Event("z"))
  prob_x_and_y = P(prob_x & prob_y)
  prob_x_or_y = P(prob_x | prob_y)
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([], []) == ([], [])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([prob_x], []) == ([prob_x], [])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([], [prob_x_and_y]) == ([], [
      prob_x_and_y
      ])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([prob_x], [prob_x_and_y]) == ([
      prob_x
      ], [prob_x_and_y])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([prob_x, prob_y],
                                                                    [prob_x_and_y]) == ([
                                                                        prob_x_or_y
                                                                        ], [])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([prob_x, prob_y, prob_z],
                                                                    [prob_x_and_y]) == ([
                                                                        prob_z, prob_x_or_y
                                                                        ], [])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([prob_x, prob_z, prob_y],
                                                                    [prob_x_and_y]) == ([
                                                                        prob_z, prob_x_or_y
                                                                        ], [])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([prob_x, prob_y, prob_y],
                                                                    [prob_x_and_y]) == ([
                                                                        prob_y, prob_x_or_y
                                                                        ], [])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_or_probs([prob_x, prob_x, prob_y],
                                                                    [prob_x_and_y]) == ([
                                                                        prob_x, prob_x_or_y
                                                                        ], [])


def test_contract_or_prob_pattern_nodes():
  prob_x = P(Event("x"))
  prob_y = P(Event("y"))
  prob_z = P(Event("z"))
  prob_x_and_y = P(prob_x & prob_y)
  node_x = Node(prob_x)
  node_y = Node(prob_y)
  node_z = Node(prob_z)
  node_x_and_y = Node(prob_x_and_y)
  node_x_or_y = Node(P(prob_x | prob_y))
  inverted_node_x_and_y = node_x_and_y.additive_invert()
  assert contract_or_prob_pattern_nodes([], []) == ([], [])
  assert contract_or_prob_pattern_nodes([node_x], []) == ([node_x], [])
  assert contract_or_prob_pattern_nodes([],
                                        [inverted_node_x_and_y]) == ([], [inverted_node_x_and_y])
  assert contract_or_prob_pattern_nodes([node_x],
                                        [inverted_node_x_and_y]) == ([node_x],
                                                                     [inverted_node_x_and_y])
  assert contract_or_prob_pattern_nodes([node_x, node_y],
                                        [inverted_node_x_and_y]) == ([node_x_or_y], [])
  assert contract_or_prob_pattern_nodes([node_x, node_y, node_z],
                                        [inverted_node_x_and_y]) == ([node_z, node_x_or_y], [])
  assert contract_or_prob_pattern_nodes([node_x, node_z, node_y],
                                        [inverted_node_x_and_y]) == ([node_z, node_x_or_y], [])
  assert contract_or_prob_pattern_nodes([node_x, node_y, node_y],
                                        [inverted_node_x_and_y]) == ([node_y, node_x_or_y], [])
  assert contract_or_prob_pattern_nodes([node_x, node_x, node_y],
                                        [inverted_node_x_and_y]) == ([node_x, node_x_or_y], [])


def test_contract_negating_nodes():
  prob_x = P(Event("x"))
  prob_y = P(Event("y"))
  prob_z = P(Event("z"))
  prob_x_and_y = P(prob_x & prob_y)
  node_x = Node(prob_x)
  node_y = Node(prob_y)
  node_z = Node(prob_z)
  node_x_and_y = Node(prob_x_and_y)
  inverted_node_x_and_y = node_x_and_y.additive_invert()
  inverted_node_x = node_x.additive_invert()
  inverted_node_y = node_y.additive_invert()
  assert contract_negating_nodes([], []) == ([], [])
  assert contract_negating_nodes([node_x_and_y], [inverted_node_x_and_y]) == ([], [])
  assert contract_negating_nodes([], [inverted_node_x_and_y]) == ([], [inverted_node_x_and_y])
  assert contract_negating_nodes([node_x, node_x_and_y], [inverted_node_x_and_y]) == ([node_x], [])
  assert contract_negating_nodes([node_x, node_x], []) == ([node_x, node_x], [])
  assert contract_negating_nodes([node_x, node_x, node_y], [inverted_node_x]) == ([node_x,
                                                                                   node_y], [])
  assert contract_negating_nodes([node_x, node_x, node_y],
                                 [inverted_node_x, inverted_node_y]) == ([node_x], [])
  assert contract_negating_nodes([node_y],
                                 [inverted_node_x, inverted_node_y]) == ([], [inverted_node_x])


def test_contract_complement_nodes():
  sure_prob = P(SureEvent())
  prob_x = P(Event("x"))
  prob_y = P(Event("y"))
  prob_z = P(Event("z"))
  prob_x_and_y = P(prob_x & prob_y)
  node_1 = Node(sure_prob)
  node_x = Node(prob_x)
  node_y = Node(prob_y)
  node_z = Node(prob_z)
  node_x_and_y = Node(prob_x_and_y)
  node_not_x = Node(prob_x.invert())
  node_not_y = Node(prob_y.invert())
  node_not_x_and_y = Node(prob_x_and_y.invert())
  assert contract_complement_nodes(2, [], []) == (2, [], [])
  assert contract_complement_nodes(2, [node_x, node_y, node_1],
                                   []) == (2, [node_x, node_y, node_1], [])
  assert contract_complement_nodes(2, [node_x], [node_not_y]) == (2, [node_x], [node_not_y])
  assert contract_complement_nodes(2, [node_y], [node_not_y]) == (2, [node_y], [node_not_y])
  assert contract_complement_nodes(2, [node_1],
                                   [node_not_y.additive_invert()]) == (1, [node_1, node_y], [])
  assert contract_complement_nodes(2, [node_1, node_1], [node_not_y.additive_invert()
                                                         ]) == (1, [node_1, node_1, node_y], [])
  assert contract_complement_nodes(
      2, [node_1, node_1, node_1],
      [node_x.additive_invert(), node_y.additive_invert()]
      ) == (0, [node_1, node_1, node_1, node_not_x, node_not_y], [])
  assert contract_complement_nodes(
      2, [node_1],
      [node_x.additive_invert(), node_x_and_y.additive_invert()]
      ) == (0, [node_1, node_not_x, node_not_x_and_y], [])
  assert contract_complement_nodes(
      2, [node_1],
      [node_x.additive_invert(), node_x_and_y.additive_invert(), node_z]
      ) == (0, [node_1, node_not_x, node_not_x_and_y], [node_z])


def test_contract_arbitrary_sum_node_group():
  sure_prob = P(SureEvent())
  prob_x = P(Event("x"))
  prob_y = P(Event("y"))
  prob_z = P(Event("z"))
  prob_x_and_y = P(prob_x & prob_y)
  prob_x_or_y = P(prob_x | prob_y)
  node_1 = Node(sure_prob)
  node_x = Node(prob_x)
  node_y = Node(prob_y)
  node_z = Node(prob_z)
  node_x_and_y = Node(prob_x_and_y)
  node_not_x = Node(prob_x.invert())
  node_not_y = Node(prob_y.invert())
  node_x_or_y = Node(prob_x_or_y)

  assert contract_arbitrary_sum_node_group([]) == []
  assert contract_arbitrary_sum_node_group([node_x]) == [node_x]
  assert contract_arbitrary_sum_node_group([node_x, node_x, node_y]) == [node_x, node_x, node_y]
  assert contract_arbitrary_sum_node_group([node_x, node_x.additive_invert(), node_y]) == [node_y]
  assert contract_arbitrary_sum_node_group([node_1, node_x,
                                            node_x.additive_invert(), node_y]) == [1, node_y]
  assert contract_arbitrary_sum_node_group([
      node_1, node_x, node_x.additive_invert(),
      node_x.additive_invert(), node_y
      ]) == [node_y, node_not_x]
  assert contract_arbitrary_sum_node_group([
      node_1, node_x,
      node_x.additive_invert(),
      node_x.additive_invert(), node_x, node_y,
      node_x_and_y.additive_invert()
      ]) == [node_y, Node(prob_x_and_y.invert())]
  assert contract_arbitrary_sum_node_group([node_1, node_x, node_y,
                                            node_x_and_y.additive_invert()]) == [1, node_x_or_y]
  assert contract_arbitrary_sum_node_group([
      node_1, node_x, node_y, node_not_y,
      node_x_and_y.additive_invert()
      ]) == [1, node_not_y, node_x_or_y]
  assert contract_arbitrary_sum_node_group([
      node_1, node_x, node_y,
      node_not_y.additive_invert(),
      node_x_and_y.additive_invert()
      ]) == [node_x_or_y, node_y]


def test_replace_same_exp_in_simple_vs_and_prob_lists_with_conditional_probs():
  prob_x = P(Event("x"))
  prob_y = P(Event("y"))
  prob_z = P(Event("z"))
  prob_x_and_y = P(prob_x & prob_y)
  prob_y_when_x = P(prob_y // prob_x)
  prob_x_when_y = P(prob_x // prob_y)
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_conditional_probs([], []) == ([], [])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_conditional_probs([prob_x],
                                                                             []) == ([prob_x], [])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_conditional_probs([],
                                                                             [prob_x_and_y
                                                                              ]) == ([],
                                                                                     [prob_x_and_y])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_conditional_probs([prob_x],
                                                                             [prob_x_and_y
                                                                              ]) == ([], [
                                                                                  prob_y_when_x
                                                                                  ])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_conditional_probs([prob_x, prob_y],
                                                                             [prob_x_and_y]) == ([
                                                                                 prob_y
                                                                                 ], [prob_y_when_x])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_conditional_probs([
      prob_x, prob_y, prob_z
      ], [prob_x_and_y]) == ([prob_y, prob_z], [prob_y_when_x])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_conditional_probs([
      prob_y, prob_z, prob_x
      ], [prob_x_and_y]) == ([prob_z, prob_x], [prob_x_when_y])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_conditional_probs([
      prob_x, prob_y, prob_y
      ], [prob_x_and_y]) == ([prob_y, prob_y], [prob_y_when_x])
  assert replace_same_exp_in_simple_vs_and_prob_lists_with_conditional_probs([
      prob_x, prob_x, prob_y
      ], [prob_x_and_y]) == ([prob_x, prob_y], [prob_y_when_x])


def test_contract_conditional_pattern_nodes():
  prob_x = P(Event("x"))
  prob_y = P(Event("y"))
  prob_z = P(Event("z"))
  node_x = N(prob_x)
  node_y = N(prob_y)
  node_z = N(prob_z)
  node_x_and_y = N(P(prob_x & prob_y))
  node_y_when_x = N(P(prob_y // prob_x))
  node_x_when_y = N(P(prob_x // prob_y))
  assert contract_conditional_pattern_nodes([], []) == ([], [])
  assert contract_conditional_pattern_nodes([node_x], []) == ([node_x], [])
  assert contract_conditional_pattern_nodes([], [node_x_when_y]) == ([], [node_x_when_y])
  assert contract_conditional_pattern_nodes([node_x_and_y],
                                            [node_x.reciprocate()]) == ([node_y_when_x], [])
  assert contract_conditional_pattern_nodes([node_x_and_y],
                                            [node_x.reciprocate(),
                                             node_y.reciprocate()]) == ([node_y_when_x],
                                                                        [node_y.reciprocate()])
  assert contract_conditional_pattern_nodes([node_x_and_y], [
      node_x.reciprocate(), node_y.reciprocate(),
      node_z.reciprocate()
      ]) == ([node_y_when_x], [node_y.reciprocate(), node_z.reciprocate()])
  assert contract_conditional_pattern_nodes([node_x_and_y], [
      node_y.reciprocate(), node_x.reciprocate(),
      node_z.reciprocate()
      ]) == ([node_x_when_y], [node_x.reciprocate(), node_z.reciprocate()])
  assert contract_conditional_pattern_nodes([node_x_and_y], [
      node_x.reciprocate(), node_y.reciprocate(),
      node_y.reciprocate()
      ]) == ([node_y_when_x], [node_y.reciprocate(), node_y.reciprocate()])
  assert contract_conditional_pattern_nodes([node_x_and_y], [
      node_x.reciprocate(), node_x.reciprocate(),
      node_y.reciprocate()
      ]) == ([node_y_when_x], [node_x.reciprocate(), node_y.reciprocate()])


def test_contract_arbitrary_product_node_group():
  sure_prob = P(SureEvent())
  prob_x = P(Event("x"))
  prob_y = P(Event("y"))
  prob_z = P(Event("z"))
  prob_x_and_y = P(prob_x & prob_y)
  prob_y_and_x = P(prob_y & prob_x)
  prob_x_or_y = P(prob_x | prob_y)
  node_1 = Node(sure_prob)
  node_x = Node(prob_x)
  node_y = Node(prob_y)
  node_z = Node(prob_z)
  node_x_and_y = Node(prob_x_and_y)
  node_y_and_x = Node(prob_y_and_x)
  node_y_when_x = N(P(prob_y // prob_x))
  node_x_when_y = N(P(prob_x // prob_y))

  assert contract_arbitrary_product_node_group([]) == []
  assert contract_arbitrary_product_node_group([node_x]) == [node_x]
  assert contract_arbitrary_product_node_group([node_x, node_x, node_y]) == [node_x, node_x, node_y]
  assert contract_arbitrary_product_node_group([node_x, node_x.reciprocate(), node_y]) == [node_y]
  assert contract_arbitrary_product_node_group([node_1, node_x,
                                                node_x.reciprocate(), node_y]) == [node_1, node_y]
  assert contract_arbitrary_product_node_group([
      node_1, node_x, node_x.reciprocate(),
      node_x.reciprocate(), node_y
      ]) == [node_1, node_y, node_x.reciprocate()]
  assert contract_arbitrary_product_node_group([
      node_1, node_x,
      node_x.reciprocate(),
      node_x.reciprocate(), node_x, node_y, node_x_and_y
      ]) == [node_1, node_y, node_x_and_y]
  assert contract_arbitrary_product_node_group([node_1, node_x,
                                                node_y.reciprocate(),
                                                node_x_and_y]) == [node_1, node_x, node_x_when_y]
  assert contract_arbitrary_product_node_group([node_x, node_x,
                                                node_y_when_x]) == [node_x, node_y_and_x]
  assert contract_arbitrary_product_node_group([node_y, node_x, node_y_when_x,
                                                node_x_when_y]) == [node_y_and_x, node_x_and_y]
