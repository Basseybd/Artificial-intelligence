import random
import sys

DEFAULT_STATE = '       | ###  -| # #  +| # ####|       '


class Action:

    def __init__(self, name, dx, dy):
        self.name = name
        self.dx = dx
        self.dy = dy


ACTIONS = [
    Action('UP', 0, -1),
    Action('RIGHT', +1, 0),
    Action('DOWN', 0, +1),
    Action('LEFT', -1, 0)
]


class State:

    def __init__(self, env, x, y):
        self.env = env
        self.x = x
        self.y = y

    def clone(self):
        return State(self.env, self.x, self.y)

    def is_legal(self, action):
        cell = self.env.get(self.x + action.dx, self.y + action.dy)
        return cell is not None and cell in ' +-'

    def legal_actions(self, actions):
        legal = []
        for action in actions:
            if self.is_legal(action):
                legal.append(action)
        return legal

    def reward(self):
        cell = self.env.get(self.x, self.y)
        if cell is None:
            return None
        elif cell == '+':
            return +10
        elif cell == '-':
            return -10
        else:
            return 0

    def at_end(self):
        return self.reward() != 0

    def execute(self, action):
        self.x += action.dx
        self.y += action.dy
        return self

    def __str__(self):
        tmp = self.env.get(self.x, self.y)
        self.env.put(self.x, self.y, 'A')
        s = ' ' + ('-' * self.env.x_size) + '\n'
        for y in range(self.env.y_size):
            s += '|' + ''.join(self.env.row(y)) + '|\n'
        s += ' ' + ('-' * self.env.x_size)
        self.env.put(self.x, self.y, tmp)
        return s


class Env:

    def __init__(self, string):
        self.grid = [list(line) for line in string.split('|')]
        self.x_size = len(self.grid[0])
        self.y_size = len(self.grid)

    def get(self, x, y):
        if x >= 0 and x < self.x_size and y >= 0 and y < self.y_size:
            return self.grid[y][x]
        else:
            return None

    def put(self, x, y, val):
        if x >= 0 and x < self.x_size and y >= 0 and y < self.y_size:
            self.grid[y][x] = val

    def row(self, y):
        return self.grid[y]

    def random_state(self):
        x = random.randrange(0, self.x_size)
        y = random.randrange(0, self.y_size)
        while self.get(x, y) != ' ':
            x = random.randrange(0, self.x_size)
            y = random.randrange(0, self.y_size)
        return State(self, x, y)


class QTable:

    def __init__(self, env, actions):
        self.env = env
        self.actions = actions
        self.qTable = [[['----' for col in range(env.x_size)] for col in range(env.y_size)]
                       for col in range(len(ACTIONS))]

    def get_q(self, state, action):
        # return the value of the q table for the given state, action
        if self.qTable[ACTIONS.index(action)][state.y][state.x] == '----':
            return 0
        else:
            return float(self.qTable[ACTIONS.index(action)][state.y][state.x])


    # def get_q_row(self, state):
    #     # return the row of q table corresponding to the given state
    #     return self.qTable[state]

    def set_q(self, state, action, val):
        # set the value of the q table for the given state, action
        if state.is_legal(action):
            if val == '0.0':
                val = '----'
            self.qTable[ACTIONS.index(action)][state.y][state.x] = val

    def learn_episode(self, alpha=.10, gamma=.90):
        # with the given alpha and gamma values,
        # from a random initial state,
        # consider a random legal action, execute that action,
        # compute the reward, and update the q table for (state, action).
        # repeat until an end state is reached (thus completing the episode)
        # also print the state after each action
        starting_state = self.env.random_state().clone()
        working_state = starting_state.clone()
        end = False
        while end is False:
            print(working_state)
            legal_actions = working_state.legal_actions(ACTIONS)
            action = random.choice(legal_actions)
            next_state = working_state.clone().execute(action)
            next_reward = []
            for n in next_state.legal_actions(ACTIONS):
                next_reward.append(self.get_q(next_state, n))
            value = ((1 - alpha) * self.get_q(working_state, action)) + alpha * (
                    next_state.reward() + (gamma * max(next_reward)))
            value = round(value, 2)
            self.set_q(working_state, action, str(value))
            working_state = next_state
            if working_state.at_end() is True:
                end = True
        return self.qTable

    def learn(self, episodes, alpha=.10, gamma=.90):
        # run <episodes> number of episodes for learning with the given alpha and gamma
        for n in range(episodes):
            self.learn_episode()

    def __str__(self):
        # return a string for the q table as described in the assignment
        for n in ACTIONS:
            print(n.name)
            for x in self.qTable[ACTIONS.index(n)]:
                print(' '.join(x))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        env = Env(sys.argv[2] if len(sys.argv) > 2 else DEFAULT_STATE)
        if cmd == 'learn':
            qt = QTable(env, ACTIONS)
            qt.learn(100)
            print(qt.__str__())
