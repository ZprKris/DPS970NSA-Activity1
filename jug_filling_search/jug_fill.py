from collections import deque

CAPACITIES = (12, 8, 3)


def get_neighbors(state):
    neighbors = []

    for i in range(3):
        # Fill jug i
        if state[i] < CAPACITIES[i]:
            new_state = list(state)
            new_state[i] = CAPACITIES[i]
            neighbors.append(
                (tuple(new_state), f"Fill jug {i + 1}")
            )

        # Empty jug i
        if state[i] > 0:
            new_state = list(state)
            new_state[i] = 0
            neighbors.append(
                (tuple(new_state), f"Empty jug {i + 1}")
            )

        # Pour from jug i into jug j
        for j in range(3):
            if i == j:
                continue

            amount = min(
                # how much water is in the source jug 
                state[i],
                # how much remaining space in the destionation jug
                CAPACITIES[j] - state[j] 
            )

            # The pour is not possible if source is empty 
            # or destination jug is full. 
            if amount > 0:
                new_state = list(state)
                new_state[i] -= amount
                new_state[j] += amount

                neighbors.append((
                    tuple(new_state),
                    f"Pour jug {i + 1} into jug {j + 1}"
                ))

    return neighbors


def bfs():
    start = (0, 0, 0)

    # Frontier - queue of states the search still needs to explore,
    # and path so far, consisting of actions and resulting states. 
    # Starts with intial state. 
    frontier = deque([(start, [])]) # double-ended queue
    explored = {start}

    while frontier:
        state, path = frontier.popleft()

        # Explores all states level-by-level and 
        # returns solutions as it reaches, so guaranteed 
        # fewest steps solution. 
        for next_state, action in get_neighbors(state):
            if next_state not in explored:
                explored.add(next_state)

                # Append to the right 
                next_path = path + [(action, next_state)]

                if 1 in next_state: # Goal test
                    return next_path

                frontier.append((next_state, next_path))

    return None

if __name__ == "__main__":
    solution = bfs()

    for step, (action, state) in enumerate(solution, 1):
        print(f"Step {step}: {action} -> {state}")