import random
import math

class RandomAgent:
    """Agent that picks a random available move.  You should be able to beat it."""
    def get_move(self, state, depth=None):
        return random.choice(state.successors())

class HumanAgent:
    """Prompts user to supply a valid move."""
    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        prompt = "Kindly enter your move {}: ".format(sorted(move__state.keys()))
        move = None
        while move not in move__state:
            try:
                move = int(input(prompt))
            except ValueError:
                continue
        return move, move__state[move]

class MinimaxAgent:
    """Artificially intelligent agent that uses minimax to optimally select the best move."""

    def get_move(self, state, depth=None):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None

        for move, state in state.successors():
            util = self.minimax(state, depth)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def MaxValue(self, state):
        if state.is_full():
            return state.score()
        util = -math.inf
        for move, board in state.successors():
            util = max(util, self.MinValue(board))
        return util

    def MinValue(self, state):
        if state.is_full():
            return state.score()
        util = math.inf
        for move, board in state.successors():
            util = min(util, self.MaxValue(board))
        return util

    def minimax(self, state, depth):
        """Determine the minimax utility value of the given state.

        Args:
            state: a connect.GameState object representing the current board
            depth: for this agent, the depth argument should be ignored!

        Returns: the exact minimax utility value of the state
        """
        if state.is_full():
            return state.score()
        else:
            nextPlayer = state.next_player()
            if nextPlayer == 1:
                util = self.MaxValue(state)
                return util
            else:
                util = self.MinValue(state)
                return util

class HeuristicAgent(MinimaxAgent):
    """Artificially intelligent agent that uses depth-limited minimax to select the best move."""

    def minimax(self, state, depth):
        return self.minimax_depth(state, depth)

    def minimax_depth(self, state, depth):
        """Determine the heuristically estimated minimax utility value of the given state.

        Args:
            state: a connect.GameState object representing the current board
            depth: the maximum depth of the game tree that minimax should traverse before
                estimating the utility using the evaluation() function.  If depth is 0, no
                traversal is performed, and minimax returns the results of a call to evaluation().
                If depth is None, the entire game tree is traversed.

        Returns: the minimax utility value of the state
        """
        if state.next_player() == 1:
            return self.max_value(state, depth)
        else:
            return self.min_value(state, depth)

    def max_value(self, state, depth):
        if state.is_full():
            return state.score() + self.evaluation(state)
        elif depth is not None and depth == 0:
            return self.evaluation(state)
        if depth != 0:
            depth -= 1
        util = -math.inf
        for move, succ in state.successors():
            util = max(util, self.minimax(succ, depth))
        return util

    def min_value(self, state, depth):
        if state.is_full():
            return state.score() + self.evaluation(state)
        elif depth is not None and depth == 0:
            return self.evaluation(state)
        if depth != 0:
            depth -= 1
        util = math.inf
        for move, succ in state.successors():
            util = min(util, self.minimax(succ, depth))
        return util

    def openEnded(self, list):
        num1 = 0
        num2 = 0
        if len(list) <= 3:
            if len(list) < 3:
                return num1, num2
            else:
                for ind, val in enumerate(list):
                    if ind == 0 and list[ind+1] == list[ind+2] and val == 0:
                        if list[ind+1] == 1:
                            num1 += 1
                        elif list[ind+1] == -1:
                            num2 += 1
                    elif ind == 2 and list[ind-1] == list[ind-2] and val == 0:
                        if list[ind-1] == 1:
                            num1 += 1
                        elif list[ind-1] == -1:
                            num2 += 1
        else:
            for ind, val in enumerate(list):
                if val == 0:
                    if ind - 2 >= 0 and ind + 2 <= (len(list)-1):
                        if list[ind-1] == list[ind-2]:
                            if list[ind-1] == 1:
                                num1 += 1
                            elif list[ind-1] == -1:
                                num2 += 1
                        if list[ind+1] == list[ind+2]:
                            if list[ind + 1] == 1:
                                num1 += 1
                            elif list[ind + 1] == -1:
                                num2 += 1
                    elif ind - 2 < 0:
                        if list[ind+1] == list[ind+2]:
                            if list[ind + 1] == 1:
                                num1 += 1
                            elif list[ind + 1] == -1:
                                num2 += 1
                    elif ind + 2 > len(list)-1:
                        if list[ind-1] == list[ind-2]:
                            if list[ind-1] == 1:
                                num1 += 1
                            elif list[ind-1] == -1:
                                num2 += 1
        return num1, num2

    def evaluation(self, state):
        """Estimate the utility value of the game state based on features.

        This method must run in O(1) time!
        Args:
            state: a connect.GameState object representing the current board

        Returns: a heusristic estimate of the utility value of the state
        """
        play1Cnt = 0
        play2Cnt = 0
        for i in range(state.num_rows):
            row = state.get_row(i)
            cnt1, cnt2 = self.openEnded(row)
            play1Cnt += cnt1
            play2Cnt += cnt2

        for i in range(state.num_cols):
            col = state.get_col(i)
            cnt1, cnt2 = self.openEnded(col)
            play1Cnt += cnt1
            play2Cnt += cnt2

        for i in range(state.num_rows):
            for j in range(state.num_cols):
                up, down = state.get_diags(i, j)
                cnt1, cnt2 = self.openEnded(up)
                play1Cnt += cnt1
                play2Cnt += cnt2
                cnt3, cnt4 = self.openEnded(down)
                play1Cnt += cnt3
                play2Cnt += cnt4

        dif = (abs(play1Cnt - play2Cnt)) ** 2
        util = 0
        sco = state.score()
        if state.score() > 0:
            util = dif + sco
        elif state.score() < 0:
            util = sco - dif
        return util 

class PruneAgent(HeuristicAgent):
    """Smarter computer agent that uses minimax with alpha-beta pruning to select the best move."""

    def minimax(self, state, depth):
        return self.minimax_prune(state, depth)

    def minimax_prune(self, state, depth):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        The value should be equal to the one determined by ComputerAgent.minimax(), but the 
        algorithm should do less work.  You can check this by inspecting the class variables
        GameState.p1_state_count and GameState.p2_state_count, which keep track of how many
        GameState objects were created over time.

        When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  That is, you cannot prune
        the state reached by moving to column 4 before you've explored the state reached by a move
        to to column 1.

        Args: see ComputerDepthLimitAgent.minimax() above

        Returns: the minimax utility value of the state
        """

        if state.next_player() == 1:
            return self.max_value(state, depth)
        else:
            return self.min_value(state, depth)

    def max_value(self, state, depth, alpha=-math.inf, beta=math.inf):
        if state.is_full():
            return state.score()
        elif depth is not None and depth == 0:
            return self.evaluation(state)
        if depth is not None:
            depth -= 1
        for move, board in state.successors():
            alpha = max(alpha, self.min_value(board, depth, alpha, beta))
            if alpha >= beta:
                return alpha
        return alpha

    def min_value(self, state, depth, alpha=-math.inf, beta=math.inf):
        if state.is_full():
            return state.score()
        elif depth is not None and depth == 0:
            return self.evaluation(state)
        if depth is not None:
            depth -= 1
        for move, board in state.successors():
            beta = min(beta, self.max_value(board, depth, alpha, beta))
            if alpha >= beta:
                return beta
        return beta
