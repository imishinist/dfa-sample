#!/usr/bin/env python3

class FARule:
    def __init__(self, state, char, next_state):
        self.state = state
        self.character = char
        self.next_state = next_state

    def can_applies_to(self, state, char):
        return self.state == state and self.character == char

    def follow(self):
        return self.next_state

    def inspect(self):
        return "#<FARule {} --{}--> {}>".format(self.state, self.character, self.next_state)


class DFARulebook:
    def __init__(self, rules):
        self.rules = rules

    def next_state(self, state, char):
        return self.rule_for(state, char).follow()

    def rule_for(self, state, char):
        return [r for r in self.rules if r.can_applies_to(state, char)][0]


class DFA:
    def __init__(self, current_state, accept_states, rulebook):
        self.current_state = current_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepting(self):
        return self.accept_states.count(self.current_state) > 0

    def read_character(self, char):
        self.current_state = self.rulebook.next_state(self.current_state, char)

    def read_string(self, string):
        for c in string:
            self.read_character(c)


class DFADesign:
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def to_dfa(self):
        return DFA(self.start_state, self.accept_states, self.rulebook)

    def accept(self, string):
        d = self.to_dfa()
        d.read_string(string)
        return d.accepting()


class NFARulebook:
    def __init__(self, rules):
        self.rules = rules

    def next_states(self, states, char):
        flatten = lambda x: [z for y in x for z in
                             (flatten(y) if hasattr(y, '__iter__') and not isinstance(y, str) else (y,))]
        return set(list(flatten(map(lambda state: self.follow_rules_for(state, char), states))))

    def follow_rules_for(self, state, char):
        return list(map(lambda rule: rule.follow(), self.rules_for(state, char)))

    def follow_free_moves(self, states):
        more_states = self.next_states(states, None)

        if more_states.issubset(states):
            return states
        else:
            return self.follow_free_moves(states.union(more_states))

    def rules_for(self, state, char):
        r = list(self.rules)
        return filter(lambda rule: rule.can_applies_to(state, char), r)

    def alphabet(self):
        return set(filter(None, map(lambda x: x.character, list(self.rules))))


class NFA:
    def __init__(self, current_states, accept_states, rulebook):
        self.current_states = current_states
        self.accept_states = accept_states
        self.rulebook = rulebook

    def get_current_states(self):
        return self.rulebook.follow_free_moves(self.current_states)

    def accepting(self):
        return not self.get_current_states().isdisjoint(self.accept_states)

    def read_character(self, char):
        self.current_states = self.rulebook.next_states(self.get_current_states(), char)

    def read_string(self, string):
        for c in string:
            self.read_character(c)


class NFADesign:
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def to_nfa(self, current_states=None):
        curr = {self.start_state} if current_states is None else current_states
        return NFA(curr, self.accept_states, self.rulebook)

    def accept(self, string):
        n = self.to_nfa()
        n.read_string(string)
        return n.accepting()


class NFASimulation:
    def __init__(self, nfa_design):
        self.nfa_design = nfa_design

    def tap(self, x, f):
        f(x)
        return x

    def next_state(self, state, char):
        return self.tap(self.nfa_design.to_nfa(state), lambda nfa: nfa.read_character(char)).get_current_states()

    def rules_for(self, state):
        return list(map(lambda x: FARule(state, x, self.next_state(state, x)), self.nfa_design.rulebook.alphabet()))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass
