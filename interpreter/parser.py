import json

grammar = [
    ("S", ["P"]),
    ("P", ["(", "P", ")", "P"]),
    ("P", [])
]

tokens = ["(", "(", ")", ")", "(", ")"]

def add_to_chart(the_set, index, element):
    if not element in the_set[index]:
        the_set[index] = [element] + the_set[index]
        return True
    return False

def closure(grammar, i, x, ab, cd, j):
    next_states = [(rule[0], [], rule[1], i) \
            for rule in grammar if cd != [] and cd[0] == rule[0]]
    return next_states

def shift(tokens, i, x, ab, cd, j):
    if cd != [] and tokens[i] == cd[0]:
        return (x, ab + [cd[0]], cd[1:], j)
    return None

def reductions(chart, i, x, ab, cd, j):
    return [(jstate[0], jstate[1] + [x], jstate[2][1:], jstate[3])
        for jstate in chart[j] if cd == [] and jstate[2] != [] and
        jstate[2][0] == x]

def parse(tokens, grammar):
    tokens = tokens + ["EOF"]
    chart = {}
    start_rule = grammar[0]
    for i, e in enumerate(tokens):
        chart[i] = []
    start_state = (start_rule[0], [], start_rule[1], 0)
    chart[0] = [start_state]
    for i, e in enumerate(tokens):
        while True:
            changes = False
            for state in chart[i]:
                x = state[0]
                ab = state[1]
                cd = state[2]
                j = state[3]

                next_states = closure(grammar, i, x, ab, cd, j)
                print 'next states: ', next_states
                for next_state in next_states:
                    changes = add_to_chart(chart, i, next_state) or changes

                next_state = shift(tokens, i, x, ab, cd, j)
                print 'shift: ', next_state
                if next_state:
                    any_changes = add_to_chart(chart, i + 1, next_state) or any_changes

                next_states = reductions(chart, i, x, ab, cd, j)
                print 'reduction: ', next_states, i, x, ab, cd, j
                for next_state in next_states:
                    changes = add_to_chart(chart, i, next_state) or changes

            if not changes:
                break

    accepting_state = (start_rule[0], start_rule[1], [], 0)
    if accepting_state in chart[len(tokens) - 1]:
        return json.dumps(chart)
    else:
        return False

print parse(tokens, grammar)
"""
{
    "0": [["S", ["P"], [], 0], ["P", [], [], 0], ["P", [], ["(", "P", ")"], 0], ["S", [], ["P"], 0]], 
    
    "1": [["P", ["(", "P"], [")"], 0], ["P", [], [], 1], ["P", [], ["(", "P", ")"], 1], ["P", ["("], ["P", ")"], 0]], 
    
    "2": [["P", ["(", "P"], [")"], 1], ["P", [], [], 2], ["P", [], ["(", "P", ")"], 2], ["P", ["("], ["P", ")"], 1]], 
    
    "3": [["P", ["(", "P"], [")"], 0], ["P", ["(", "P", ")"], [], 1]], 
    
    "4": [["S", ["P"], [], 0], ["P", ["(", "P", ")"], [], 0]]}

"""
