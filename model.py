
initial_boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [2, 2, 2, 2, 2, 2, 2, 2],
               [2, 2, 2, 2, 2, 2, 2, 2]]


MAXNUM = float("inf")
MINNUM = -float("inf")
MAXTUPLE = (MAXNUM, MAXNUM)
MINTUPLE = (MINNUM, MINNUM)

# direction: 1 -> left, 2 -> middle, 3 -> right
def single_move(initial_pos, direction, turn):
    if turn == 1:
        if direction == 1:
            return initial_pos[0] + 1, initial_pos[1] - 1
        elif direction == 2:
            return initial_pos[0] + 1, initial_pos[1]
        elif direction == 3:
            return initial_pos[0] + 1, initial_pos[1] + 1
    elif turn == 2:
        if direction == 1:
            return initial_pos[0] - 1, initial_pos[1] - 1
        elif direction == 2:
            return initial_pos[0] - 1, initial_pos[1]
        elif direction == 3:
            return initial_pos[0] - 1, initial_pos[1] + 1

def alterturn(turn):
    if turn == 1:
        return 2
    if turn == 2:
        return 1

class Action:
    def __init__(self, coordinate, direction, turn):
        self.coordinate = coordinate
        self.direction = direction
        self.turn = turn
    def getString(self):
        return self.coordinate, self.direction, self.turn
    def getCoordinate_x(self):
        return self.coordinate[0]

class State:
    def __init__(self,
                 boardmatrix=None,
                 black_position=None,
                 white_position=None,
                 black_num=0,
                 white_num=0,
                 turn=1,
                 function=0,
                 width=8,
                 height=8):
        self.width = width
        self.height = height
        if black_position is None:
            self.black_positions = []
        else:
            self.black_positions = black_position
        if white_position is None:
            self.white_positions = []
        else:
            self.white_positions = white_position
        self.black_num = black_num
        self.white_num = white_num
        self.turn = turn
        self.function = function
        if boardmatrix is not None:
            # self.wide = len(boardmatrix[0])
            # self.height = len(boardmatrix)
            for i in range(self.height):
                for j in range(self.width):
                    if boardmatrix[i][j] == 1:
                        self.black_positions.append((i, j))
                        self.black_num += 1
                    if boardmatrix[i][j] == 2:
                        self.white_positions.append((i, j))
                        self.white_num += 1

# State.transfer(action), given an action, return a resultant state
    def transfer(self, action):
        black_pos = list(self.black_positions)
        white_pos = list(self.white_positions)

        # black move
        if action.turn == 1:
            if action.coordinate in self.black_positions:
                index = black_pos.index(action.coordinate)
                new_pos = single_move(action.coordinate, action.direction, action.turn)
                black_pos[index] = new_pos
                if new_pos in self.white_positions:
                    white_pos.remove(new_pos)
            else:
                print("Invalid action!")

        # white move
        elif action.turn == 2:
            if action.coordinate in self.white_positions:
                index = white_pos.index(action.coordinate)
                new_pos = single_move(action.coordinate, action.direction, action.turn)
                white_pos[index] = new_pos
                if new_pos in self.black_positions:
                    black_pos.remove(new_pos)
            else:
                print("Invalid action!")

        state = State(black_position=black_pos, white_position=white_pos, black_num=self.black_num, white_num=self.white_num, turn=alterturn(action.turn), function=self.function, height=self.height, width=self.width)
        return state

    def available_actions(self):
        available_actions = []
        if self.turn == 1:
            for pos in sorted(self.black_positions, key=lambda p: (p[0], -p[1]), reverse=True):
                # ======Caution!======
                if pos[0] != self.height - 1 and pos[1] != 0 and (pos[0] + 1, pos[1] - 1) not in self.black_positions:
                    available_actions.append(Action(pos, 1, 1))
                if pos[0] != self.height - 1 and (pos[0] + 1, pos[1]) not in self.black_positions and (pos[0] + 1, pos[1]) not in self.white_positions:
                    available_actions.append(Action(pos, 2, 1))
                if pos[0] != self.height - 1 and pos[1] != self.width - 1 and (pos[0] + 1, pos[1] + 1) not in self.black_positions:
                    available_actions.append(Action(pos, 3, 1))

        elif self.turn == 2:
            for pos in sorted(self.white_positions, key=lambda p: (p[0], p[1])):
                # ======Caution!======
                if pos[0] != 0 and pos[1] != 0 and (pos[0] - 1, pos[1] - 1) not in self.white_positions:
                    available_actions.append(Action(pos, 1, 2))
                if pos[0] != 0 and (pos[0] - 1, pos[1]) not in self.black_positions and (pos[0] - 1, pos[1]) not in self.white_positions:
                    available_actions.append(Action(pos, 2, 2))
                if pos[0] != 0 and pos[1] != self.width - 1 and (pos[0] - 1, pos[1] + 1) not in self.white_positions:
                    available_actions.append(Action(pos, 3, 2))

        return available_actions

    def getMatrix(self):
        matrix = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for item in self.black_positions:
            matrix[item[0]][item[1]] = 1
        for item in self.white_positions:
            matrix[item[0]][item[1]] = 2
        return matrix

    def utility(self, turn):
        #print(turn)
        if self.function == 0:
            return 0
        elif self.function == 1:
            return self.offensive_function(turn)
        elif self.function == 2:
            return self.defensive_function(turn)
        elif self.function == 3:
            return self.offensive_function_3_workers(turn)
        elif self.function == 4:
            return self.defensive_function_3_workers(turn)
        elif self.function == 5:
            return self.offensive_function_long(turn)
        elif self.function == 6:
            return self.defensive_function_long(turn)






    # def myscore(self, turn):
    #     if turn == 1:
    #         return sum(pos[0] for pos in self.black_positions) \
    #                + self.winningscore(turn)
    #     elif turn == 2:
    #         return sum(7 - pos[0] for pos in self.white_positions) \
    #                + self.winningscore(turn)
    #
    # def enemyscore(self, turn):
    #     if turn == 1:
    #         return sum(7 - pos[0] for pos in self.white_positions) \
    #                + self.winningscore(2)
    #     elif turn == 2:
    #         return sum(pos[0] for pos in self.black_positions) \
    #                + self.winningscore(1)

    def winningscore(self, turn):
        winningvalue = 200
        if turn == 1:
            if self.isgoalstate() == 1:
                return winningvalue
            elif self.isgoalstate() == 2:
                return -winningvalue
            else:
                return 0
        elif turn == 2:
            if self.isgoalstate() == 2:
                return winningvalue
            elif self.isgoalstate() == 1:
                return -winningvalue
            else:
                return 0

    def isgoalstate(self, type=0):
        if type == 0:
            if 0 in [item[0] for item in self.white_positions] or len(self.black_positions) == 0:
                return 2
            if self.height - 1 in [item[0] for item in self.black_positions] or len(self.white_positions) == 0:
                return 1
            return 0
        else:
            count = 0
            for i in self.black_positions:
                if i[0] == 7:
                    count += 1
            if count == 3:
                return True
            count = 0
            for i in self.white_positions:
                if i[0] == 0:
                    count += 1
            if count == 3:
                return True
            if len(self.black_positions) <= 2 or len(self.white_positions) <= 2:
                return True
        return False

    def get_farthest_piece(self, turn):
        if turn == 1:
            return max(pos[0] for pos in self.black_positions)
        elif turn == 2:
            return max(7 - pos[0] for pos in self.white_positions)

# num of diagonal_pairs belongs to different color
    def get_diff_diagonal_pairs(self):
        res = 0
        for black in self.black_positions:
            if (black[0] + 1, black[1] - 1) in self.white_positions:
                res += 1
            if (black[0] + 1, black[1] + 1) in self.white_positions:
                res += 1
        return res

# num of vertical pairs for Black or White
    def get_vertical_pairs(self, turn):
        res = 0
        if turn == 1:
            for black in self.black_positions:
                if (black[0] + 1, black[1]) in self.black_positions:
                    res += 1
        elif turn == 2:
            for white in self.white_positions:
                if (white[0] + 1, white[1]) in self.white_positions:
                    res += 1
        return res


# num of pieces in baseline 1, 2, 5, 6
    def get_important_pos_baseline(self, turn):
        if turn == 1:
            return len([pos for pos in self.black_positions if pos[0] == 0 and pos[1] in [1, 2, 5, 6]])
        elif turn == 2:
            return len([pos for pos in self.white_positions if pos[0] == 7 and pos[1] in [1, 2, 5, 6]])

    def myscore(self, turn):
        if turn == 1:
            return len(self.black_positions) \
                   + sum(pos[0] for pos in self.black_positions) + self.winningscore(turn)
                   #+ max(pos[0] for pos in self.black_positions) \

        elif turn == 2:
            return len(self.white_positions) \
                   + sum(7 - pos[0] for pos in self.white_positions) + self.winningscore(turn)
                   #+ max(7 - pos[0] for pos in self.white_positions) \


    def enemyscore(self, turn):
        if turn == 1:
            return len(self.white_positions) \
                   + sum(7 - pos[0] for pos in self.white_positions) + self.winningscore(2)
                   #+ max(7 - pos[0] for pos in self.white_positions)\

        elif turn == 2:
            return len(self.black_positions) \
                   + sum(pos[0] for pos in self.black_positions) + self.winningscore(1)
                   #+ max(pos[0] for pos in self.black_positions) \


    def offensive_function(self, turn):
        """
        2 * offensive_component + defensive_componet + tie_breaking
        """
        return 2 * self.myscore(turn) - 1 * self.enemyscore(turn)
               #+  self.get_important_pos_baseline(turn)

    def defensive_function(self, turn):
        """
        2 * defensive_component + offensive_componet + tie_breaking
        """
        return 1 * self.myscore(turn) - 2 * self.enemyscore(turn)
               #+ 2 * self.get_vertical_pairs(turn) + 4 * self.get_important_pos_baseline(turn)


    def myscore_3_workers(self, turn):
        if turn == 1:
            return len(self.black_positions) \
                   + sum(pos[0] for pos in self.black_positions) \
                   + sum(sorted([pos[0] for pos in self.black_positions], reverse=True)[0:3]) \
                   + self.winningscore(turn)
        elif turn == 2:
            return len(self.white_positions) \
                   + sum(7 - pos[0] for pos in self.white_positions) \
                   + sum(sorted([7 - pos[0] for pos in self.white_positions], reverse=True)[0:3]) \
                   + self.winningscore(turn)

    def enemyscore_3_workers(self, turn):
        if turn == 1:
            return len(self.white_positions) \
                   + sum(7 - pos[0] for pos in self.white_positions) \
                   + sum(sorted([7 - pos[0] for pos in self.white_positions], reverse=True)[0:3]) \
                   + self.winningscore(2)
        elif turn == 2:
            return len(self.black_positions) \
                   + sum(pos[0] for pos in self.black_positions) \
                   + sum(sorted([pos[0] for pos in self.black_positions], reverse=True)[0:3]) \
                   + self.winningscore(1)

    def myscore_long(self, turn):
        if turn == 1:
            return  len(self.black_positions) \
                   + 5 * sum(pos[0] for pos in self.black_positions) \
                   + self.winningscore(turn)

        elif turn == 2:
            return len(self.white_positions) \
                   + 5 *sum(7 - pos[0] for pos in self.white_positions) \
                   + self.winningscore(turn)

    def enemyscore_long(self, turn):
        if turn == 1:
            return len(self.white_positions) \
                   + 5 * sum(7 - pos[0] for pos in self.white_positions) \
                   + self.winningscore(2)
        elif turn == 2:
            return len(self.black_positions) \
                   + 5 * sum(pos[0] for pos in self.black_positions) \
                   + self.winningscore(1)

    def offensive_function_3_workers(self, turn):
        return 3 * self.myscore_3_workers(turn) - self.enemyscore_3_workers(turn)

    def defensive_function_3_workers(self, turn):
        return self.myscore_3_workers(turn) - 3 * self.enemyscore_3_workers(turn)

    def offensive_function_long(self, turn):
        return 4 * self.myscore_long(turn) - self.enemyscore_long(turn)

    def defensive_function_long(self, turn):
        return self.myscore_long(turn) - 4 * self.enemyscore_long(turn)