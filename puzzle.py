import math

def LoadFromFile(filepath):
    with open(filepath, 'r') as file:
        n = int(file.readline())
        data = [next(file).strip().split('\t') for x in range(n)]
        result=[]
        for row in data:
            result = result + row
    if len(result) > n*n:
        print(result)
        return None
    elif '*' not in result:
        print(result)
        return None
    else:
        return tuple(result)

def ComputeNeighbors(state):
    n = int(math.sqrt(len(state)))
    res = []
    ind = state.index('*')
    if not top(ind, n):
        res.append(up_neig(state, ind, n))
    if not bottom(ind, n):
        res.append(down_neig(state, ind, n))
    if not left(ind, n):
        res.append(left_neig(state, ind))
    if not right(ind, n):
        res.append(right_neig(state, ind))
    return res

def top(ind, n):
    return ind < n

def bottom(ind, n):
    return ind > n*n - (n+1)

def left(ind, n):
    return ind in [0, n, n*2]

def right(ind, n):
    return ind in [n-1, (n-1) + n, n*n - 1]

def up_neig(state, ind, n):
    _state = list(state)
    _state[ind], _state[ind-n] = _state[ind-n], _state[ind]
    return tuple(_state)

def down_neig(state, ind, n):
    _state = list(state)
    _state[ind], _state[ind+n] = _state[ind+n], _state[ind]
    return tuple(_state)

def left_neig(state, ind):
    _state = list(state)
    _state[ind], _state[ind-1] = _state[ind-1], _state[ind]
    return tuple(_state)

def right_neig(state, ind):
    _state = list(state)
    _state[ind], _state[ind+1] = _state[ind+1], _state[ind]
    return tuple(_state)

def BFS(state):
    Q = [state]
    visited = set(state)
    parents = {state: None}
    while Q:
        current_state = pop(Q)
        visited.add(current_state)
        print(current_state)
        if IsGoal(current_state):
            path = []
            w = current_state
            while w is not None:
                path.insert(0, w)
                w = parents[w]
            return path
        for neighbor in ComputeNeighbors(current_state):
            if neighbor not in visited:
                Q.append(neighbor)
                visited.add(neighbor)
                parents[neighbor] = current_state
    return None

def DFS(state):
    S = [state]
    discovered = set(state)
    parents = {state:None}
    while S:
        current_state = pop(S)
        discovered.add(current_state)
        if IsGoal(current_state):
            path = []
            w = current_state
            while w is not None:
                path.insert(0, w)
                w = parents[w]
            return path
        for _neighbor in ComputeNeighbors(current_state):
            if _neighbor not in discovered:
                push(_neighbor, S)
                discovered.add(_neighbor)
                parents[_neighbor] = current_state
    return None

def bidirectional(state):
    Q = [state]
    n = len(state)
    goal = []
    for number in range(1, n):
        goal.append(number)
    goal.append('*')
    goal = tuple(goal)
    print(goal)
    Q2 = [goal]
    visited = set(state)
    discovered = set(goal)
    parents = {state: None}
    reverse_parents = {goal: None}
    while Q and Q2:
        current_state = pop(Q)
        visited.add(current_state)
        for neighbor in ComputeNeighbors(current_state):
            if neighbor not in visited:
                Q.append(neighbor)
                visited.add(neighbor)
                parents[neighbor] = current_state
        reverse_current = pop(Q2)
        discovered.add(reverse_current)
        for neighbor in ComputeNeighbors(reverse_current):
            if neighbor not in discovered:
                Q2.append(neighbor)
                discovered.add(neighbor)
                reverse_parents[neighbor] = reverse_current
        intersect = visited.intersection(discovered)
        if intersect:
            intersection = list(intersect)[0]
            path = []
            path.append(intersection)
            w = current_state
            b = reverse_current
            while w is not None:
                path.insert(0, w)
                w = parents[w]
            while b is not None:
                path.append(b)
                b = reverse_parents[b]
            return path
    return None

def pop(q):
    if len(q) > 0:
        val = q[0]
        del q[0]
        return val
    else:
        print("error")

def push(s, list):
    list.insert(0, s)
    return list

def IsGoal(state):
    if state[-1]!='*':
        return False
    previous = state[0]
    n = int(math.sqrt(len(state)))
    for x in state[:-1]:
        if x < previous:
            return False
        previous = x
    return True

def main():
    state = LoadFromFile("/Users/triciazhang/npuzzle/filepath.txt")
    print(ComputeNeighbors(state))
    print(BFS(state))
    print(DFS(state))
    print(bidirectional(state))

if __name__ == "__main__":
    main()
