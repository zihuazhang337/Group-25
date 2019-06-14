import random

def choose_action(curr_state, possible_actions, eps, q_table):
#    return possible_actions[random.randint(0, len(possible_actions) - 1)]
    best = possible_actions[0]
    bestlist = []
    elselist = []
    for i in possible_actions:
        if q_table[curr_state][i] > q_table[curr_state][best]:
            best = i
            elselist = elselist + bestlist
            bestlist = [best]
        elif q_table[curr_state][i] == q_table[curr_state][best]:
            bestlist.append(i)
        else:
            elselist.append(i)
    if random.random() > eps or len(elselist) == 0:
        return bestlist[random.randint(0, len(bestlist) - 1)]
    else:
        return elselist[random.randint(0, len(elselist) - 1)]
