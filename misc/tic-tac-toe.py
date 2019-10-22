def print_state(state):
    print('******')
    for s in state:
        print(s)
    print('******')
    
def is_max_node(state):
    sum_X = 0
    sum_O = 0
    for s in state:
        for c in s:
            if c == 'X':
                sum_X += 1
            elif c == 'O':
                sum_O += 1 
    return sum_X == sum_O

def check_column(i, state):
    if state[1][i] == state[0][i] and state[0][i] == state[2][i]:
        return state[0][i]
    return '-'

def check_row(i, state):
    if state[i][0] == state[i][1] and state[i][0] == state[i][2]:
        return state[i][0]
    return '-'

def check_d1(state):
    if state[0][0] == state[1][1] and state[0][0] == state[2][2]:
        return state[1][1]
    return '-'

def check_d2(state):
    if state[2][0] == state[1][1] and state[1][1] == state[0][2]:
        return state[2][0]
    return '-'

def is_full_node(state):
    for s in state:
        for c in s:
            if c != '-':
                return False
    return True

def get_score(state):
    """
    :rtype bool
    """
    col = [check_column(i, state) for i in range(3)]
    row = [check_row(i, state) for i in range(3)]
    d1 = check_d1(state)
    d2 = check_d2(state)
    for c in col:
        if c == 'X': return True, 1
        elif c == 'O': return True, -1

    for r in row:
        if r == 'X': return True, 1
        elif r == 'O': return True, -1

    if d1 == 'X': return True, 1
    elif d1 == 'O': return True, -1

    if d2 == 'X': return True, 1
    elif d2 == 'O': return True, -1

    if is_full_node(state): return True, 0
    return False, 0

def value(state):
    terminal, score = get_score(state)
    if terminal:
        return score
    
    if is_max_node(state):
        return max_value(state)
    else:
        return min_value(state)

def max_value(state):
    return [value(s) for s in successor(state)]

def min_value(state):
    return [value(s) for s in successor(state)]

def fill(c, i, j, state):
    new_state = state[:]
    new_state[i] = new_state[i][:j] + c + new_state[i][j+1:]
    return new_state

def successor(state):
    c = 'X' if is_max_node(state) else '0'
    results = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == '-':
                results.append(fill(c, i, j, state))
    return results

if __name__ ==  '__main__':
    state = ['---', '---', '---']
    state1 = ['--O', 'X-X', 'XOO']
    state2 = ['---', 'XXX', 'OO-']
    print_state(state2)
    print(is_max_node(state1))
    print(get_score(state1))
    print(get_score(state2))
    print(value(state1))

    while True:
        terminal, score = get_score()
        x, y = map(int, input().split())


