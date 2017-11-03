import numpy as np
from copy import deepcopy
# XXX: Do not modify anything.

"""
    Tic tac toe environment class
    An alignment in a grid is either a column, a line or a diagonal
    of any size which repeats a symbol.
    Scoring of a player S in a grid _*_*k :
    Maximum number of alignments of size k with symbol S
    subject to the following constraint :
    All pairs of alignments cannot share more than 1 cell.
"""


class Tictactoe(object):

    def __init__(self, n, m, k):
        """
            Arguments:
            ----------
            - `n`: the number of lines of the grid
            - `m`: the number of columns of the grid
            - `k`: the size of an alignment.
        """
        self.n = n
        self.m = m
        self.k = k
        self.reset()

    def reset(self):
        """
            Resets the environment to an empty grid of size n*m
            and a random initial symbol (player)
        """
        self.currentX = np.random.randint(1, 3)
        self.M = np.zeros((self.n, self.m))
        self.totalScores = [0, 0]
        self.alignments = [[], []]

    def step(self, action):
        """
            Arguments:
            ----------
            - `action = (x,i,j)` : a triplet of integers

            If `action` is valid, replace the empty cell self.M[i,j] by x
            and update the current state (scoring and alignments)
        """
        x, i, j = action
        if not self.checkAction(action):
            self.currentX = 3 - self.currentX
            return
        self.M[i, j] = x
        s = self.updateScore(action)
        if s == 0:
            self.currentX = 3 - self.currentX

    def terminalState(self):
        """
            Check the end of the game, which holds if :
            - The grid is full
            or
            - There is no new possible alignment
        """
        currentX = self.currentX
        otherX = 3 - currentX

        env2 = deepcopy(self)
        env3 = deepcopy(self)

        # Test for first player
        for i in range(self.n):
            for j in range(self.m):
                if env2.M[i][j] == 0:
                    env2.currentX = currentX
                    env2.step((currentX, i, j))
                if env3.M[i][j] == 0:
                    env3.currentX = otherX
                    env3.step((otherX, i, j))
        return (self.totalScores == env2.totalScores
                and self.totalScores == env3.totalScores)

    def checkAlignment(self, align, x):
        """
            Arguments:
            ----------
            - `align` : a list of pair of integers
            - 'x' : a symbol

            Returns True if len(`align`) == k
            and does not share more than one symbol
            with another existing alignment
        """
        if len(align) != self.k:
            return False
        return len(list(filter(lambda x: len(x.intersection(align))
                               > 1, self.alignments[x - 1]))) == 0

    def checkCoordinates(self, i, j):
        """
            Arguments:
            ----------
            - `i` : a list of pair of integers
            - 'j' : a symbol

            Returns true if `i` and `j` are valid coordinates in current grid
        """
        return i >= 0 and i < self.n and j >= 0 and j < self.m

    def checkAction(self, action):
        """
            Arguments:
            ----------
            - `action = (x,i,j)` : a triplet of integers

            Returns true if :
            - `i` and `j` are valid coordinates in current grid
            - `x` is the current symbol in the game
            - the cell at (`i`,`j`) in the grid is available (= 0)
        """
        x, i, j = action
        return self.checkCoordinates(
            i, j) and self.currentX == x and self.M[i, j] == 0

    def updateScore(self, action):
        """
            Arguments:
            ----------
            - `action = (x,i,j)` : a triplet of integers

            Returns number of new alignments made with the symbol `x`
            at cell (`i`,`j`) and adjacents cells.
        """
        x, i, j = action
        k = self.k
        intervals = [[(i -
                       k +
                       1, j -
                       k +
                       1), (i +
                            k -
                            1, j +
                            k -
                            1)], [(i -
                                   k +
                                   1, j), (i +
                                           k -
                                           1, j)], [(i, j -
                                                     k +
                                                     1), (i, j +
                                                          k -
                                                          1)], [(i +
                                                                 k -
                                                                 1, j -
                                                                 k +
                                                                 1), (i -
                                                                      k +
                                                                      1, j +
                                                                      k -
                                                                      1)]]
        s = 0
        for interval in intervals:
            iStart, jStart = interval[0]
            iEnd, jEnd = interval[1]
            iTemp, jTemp = (iStart, jStart)
            align = []
            alignIdx = []
            while iTemp != iEnd or jTemp != jEnd:
                if self.checkCoordinates(iTemp, jTemp):
                    alignIdx.append((iTemp, jTemp))
                    if iTemp == i and jTemp == j:
                        align.append(x)
                    else:
                        align.append(self.M[iTemp, jTemp])
                iTemp += 1 if iTemp < iEnd else (-1 if iTemp > iEnd else 0)
                jTemp += 1 if jTemp < jEnd else (-1 if jTemp > jEnd else 0)
            if self.checkCoordinates(iEnd, jEnd):
                alignIdx.append((iEnd, jEnd))
                align.append(self.M[iEnd, jEnd])
            iBegin = 0
            iEnd = k
            len_align = len(align)
            for h in range(len_align - k + 1):
                alignIdx2 = set(alignIdx[iBegin:iEnd])
                align2 = np.asarray(align[iBegin:iEnd]) == x
                if np.all(align2) and self.checkAlignment(alignIdx2, x):
                    self.alignments[x - 1].append(alignIdx2)
                    self.totalScores[x - 1] += 1
                    s += 1
                iBegin += 1
                iEnd += 1

        return s

    def render(self):
        """
            Renders the board
        """

        a = (' ___' * self.m)
        c = []

        c = []
        for i in range(self.n):
            b = []
            for j in range(self.m):
                b.append('|')
                b.append("X" if self.M[i][j] == 1 else (
                    "O" if self.M[i][j] == 2 else " "))
            b.append('|')
            b = ' '.join(b)
            c.extend([a, b])
        c.append(a)
        print('\n'.join(tuple(c)))

    def currentState(self):
        """
            Returns the current state :
                - Current state of the grid
                - Current symbol (player)
                - Total score for the two players
                - Lists of cells involved in a alignment
        """
        return (self.M, self.currentX, self.totalScores, self.alignments)
