import unittest
from main import FARule
from main import DFADesign
from main import DFARulebook
from main import NFADesign
from main import NFARulebook
from main import NFASimulation


class TestNFARulebook(unittest.TestCase):
    def test_alphabet(self):
        rulebook = NFARulebook([
            FARule(1, 'a', 1), FARule(1, 'a', 2), FARule(1, None, 2),
            FARule(2, 'b', 3),
            FARule(3, 'b', 1), FARule(3, None, 2),
        ])
        print(rulebook.alphabet())
        assert rulebook.alphabet() == {"a", "b"}


class TestDFA(unittest.TestCase):
    def test_dfa(self):
        dfa = DFADesign(1, [3], DFARulebook([
            FARule(1, 'a', 2), FARule(1, 'b', 1),
            FARule(2, 'a', 2), FARule(2, 'b', 3),
            FARule(3, 'a', 3), FARule(3, 'b', 3),
        ]))
        assert not dfa.accept("a")
        assert not dfa.accept("baa")
        assert dfa.accept("baba")


class TestNFA(unittest.TestCase):
    def test_nfa(self):
        nfa = NFADesign(1, [4], NFARulebook([
            FARule(1, 'a', 1), FARule(1, 'b', 1), FARule(1, 'b', 2),
            FARule(2, 'a', 3), FARule(2, 'b', 3),
            FARule(3, 'a', 4), FARule(3, 'b', 4),
        ]))
        assert nfa.accept("bab")
        assert nfa.accept("bbbbb")
        assert not nfa.accept("bbabb")

    def test_nfa_with_current_states(self):
        nfa = NFADesign(1, {3}, NFARulebook([
            FARule(1, 'a', 1), FARule(1, 'a', 2), FARule(1, None, 2),
            FARule(2, 'b', 3),
            FARule(3, 'b', 1), FARule(3, None, 2),
        ]))
        assert nfa.to_nfa().get_current_states() == {1, 2}
        assert nfa.to_nfa({2}).get_current_states() == {2}
        assert nfa.to_nfa({3}).get_current_states() == {3, 2}

    def test_nfa_free_move(self):
        nfa = NFADesign(1, [2, 4], NFARulebook([
            FARule(1, None, 2), FARule(1, None, 4),
            FARule(2, 'a', 3),
            FARule(3, 'a', 2),
            FARule(4, 'a', 5),
            FARule(5, 'a', 6),
            FARule(6, 'a', 4),
        ]))
        assert nfa.accept('aa')
        assert nfa.accept('aaa')
        assert not nfa.accept('aaaaa')
        assert nfa.accept('aaaaaa')


class TestNFASimulation(unittest.TestCase):
    def test_next_state(self):
        nfa_design = NFADesign(1, {3}, NFARulebook([
            FARule(1, 'a', 1), FARule(1, 'a', 2), FARule(1, None, 2),
            FARule(2, 'b', 3),
            FARule(3, 'b', 1), FARule(3, None, 2),
        ]))
        simulation = NFASimulation(nfa_design)
        assert simulation.next_state({1, 2}, 'a') == {1, 2}
        assert simulation.next_state({1, 2}, 'b') == {3, 2}
        assert simulation.next_state({3, 2}, 'b') == {1, 3, 2}
        assert simulation.next_state({1, 3, 2}, 'b') == {1, 3, 2}
        assert simulation.next_state({1, 3, 2}, 'a') == {1, 2}

    def test_rules_for(self):
        nfa_design = NFADesign(1, {3}, NFARulebook([
            FARule(1, 'a', 1), FARule(1, 'a', 2), FARule(1, None, 2),
            FARule(2, 'b', 3),
            FARule(3, 'b', 1), FARule(3, None, 2),
        ]))
        simulation = NFASimulation(nfa_design)


if __name__ == "__main__":
    unittest.main()
