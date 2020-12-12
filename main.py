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
