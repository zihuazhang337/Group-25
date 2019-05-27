import random

items=['pumpkin', 'sugar', 'egg', 'egg',
       'planks','planks','red_mushroom']

food_recipes = {'pumpkin_pie': ['pumpkin', 'egg', 'sugar'],
                'pumpkin_seeds': ['pumpkin'],
                'bowl':['planks', 'planks'],
                'mushroom_stew':['bowl', 'red_mushroom']}

rewards_map = {'pumpkin': -5, 'egg': -25, 'sugar': -10,
               'pumpkin_pie': 100, 'pumpkin_seeds': -50,
               'red_mushroom': 5, 'planks': -5, 'bowl': -1, 'mushroom_stew': 100}

def is_solution(reward):
#    return reward == 100
   return reward == 200 #for part2

def get_curr_state(items):
    s = []
    for item in items:
        for quantity in range(item[1]):
            s.append(item[0])
    s.sort()
    return tuple(s)

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
