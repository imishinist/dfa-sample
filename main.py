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

    def rules_for(self, state, char):
        r = list(self.rules)
        return filter(lambda rule: rule.can_applies_to(state, char), r)


class NFA:
    def __init__(self, current_states, accept_states, rulebook):
        self.current_states = current_states
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepting(self):
        return not self.current_states.isdisjoint(self.accept_states)

    def read_character(self, char):
        self.current_states = self.rulebook.next_states(self.current_states, char)

    def read_string(self, string):
        for c in string:
            self.read_character(c)


class NFADesign:
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def to_nfa(self):
        return NFA({self.start_state}, self.accept_states, self.rulebook)

    def accept(self, string):
        n = self.to_nfa()
        n.read_string(string)
        return n.accepting()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rb = DFARulebook([
        FARule(1, 'a', 2), FARule(1, 'b', 1),
        FARule(2, 'a', 2), FARule(2, 'b', 3),
        FARule(3, 'a', 3), FARule(3, 'b', 3),
    ])
    dfa = DFADesign(1, [3], rb)
    print(dfa.accept("a"))
    print(dfa.accept("baa"))
    print(dfa.accept("baba"))

    rb = NFARulebook([
        FARule(1, 'a', 1), FARule(1, 'b', 1), FARule(1, 'b', 2),
        FARule(2, 'a', 3), FARule(2, 'b', 3),
        FARule(3, 'a', 4), FARule(3, 'b', 4),
    ])
    nfa_design = NFADesign(1, [4], rb)
    print(nfa_design.accept("bab"))
    print(nfa_design.accept("bbbbb"))
    print(nfa_design.accept("bbabb"))
