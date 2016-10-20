from model import *


class AlphaBetaAgent:
    def __init__(self, boardmatrix, turn, depth, function):
        self.boardmatrix = boardmatrix
        self.turn = turn
        self.maxdepth = depth
        self.function = function

    def max_value(self, state, alpha, beta, depth):
        if depth == self.maxdepth:
            return state.utility(self.turn)
        v = -float("inf")
        for action in state.available_actions():
            v = max(v, self.min_value(state.transfer(action), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, alpha, beta, depth):
        if depth == self.maxdepth:
            return state.utility(self.turn)
        v = float("inf")
        for action in state.available_actions():
            v = min(v, self.max_value(state.transfer(action), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def alpha_beta_decision(self):
        final_action = None
        initialstate = State(boardmatrix=self.boardmatrix, turn=self.turn, function=self.function)
        v = -float("inf")
        for action in initialstate.available_actions():
            new_state = initialstate.transfer(action)
            if new_state.isgoalstate():
                final_action = action
                break
            minresult = self.min_value(new_state, -float("inf"), float("inf"), 1)
            if minresult > v:
                final_action = action
                v = minresult
        print(final_action.getString())
        return initialstate.transfer(final_action)

