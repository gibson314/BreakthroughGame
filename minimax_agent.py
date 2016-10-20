import numpy as np
from model import *


class MinimaxAgent:
    def __init__(self, boardmatrix, turn, depth, function):
        self.boardmatrix = boardmatrix
        self.turn = turn
        self.maxdepth = depth
        self.function = function

    def max_value(self, state, depth):
        if depth == self.maxdepth:
            #print("utility", state.utility(self.turn))
            return state.utility(self.turn)
        v = MINTUPLE
        for action in state.available_actions():
            v = max(v, self.min_value(state.transfer(action), depth + 1))
        return v

    def min_value(self, state, depth):
        if depth == self.maxdepth or state.isgoalstate():
            #print("utility", state.utility(self.turn))
            return state.utility(self.turn)
        v = MAXTUPLE
        for action in state.available_actions():
            v = min(v, self.max_value(state.transfer(action), depth + 1))
        return v

    def minimax_decision(self):
        final_action = None
        initialstate = State(boardmatrix=self.boardmatrix, turn=self.turn, function=self.function)
        v = MINTUPLE
        for action in initialstate.available_actions():
            new_state = initialstate.transfer(action)
            if new_state.isgoalstate():
                final_action = action
                break
            minresult = self.min_value(new_state, 1)
            if minresult > v:
                final_action = action
                v = minresult

        print(final_action.getString())
        return initialstate.transfer(final_action)



