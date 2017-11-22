import numpy as np
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
        self.actions = []
        self.M = np.zeros((self.n, self.m), dtype=np.int8)
        self.totalScores = [0, 0]
        self.alignments = [[], []]
        self.nb_zeros = self.n * self.m

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
        self.actions.append(action)
        self.nb_zeros -= 1

    def unstep(self, max_unsteps=1):
        """
            Arguments:
            ----------
            - `max_unsteps` : number

            Cancel until `max_unsteps` consecutive
            last actions already performed in the game
        """
        k = max_unsteps
        while k > 0 and self.actions != []:
            x, i, j = self.actions.pop()
            self.currentX = x
            self.M[i, j] = 0
            aligns = [y for y in self.alignments[x - 1] if (i, j) not in y]
            nbaligns = len([y for y in self.alignments[x - 1] if (i, j) in y])
            self.totalScores[x - 1] -= nbaligns
            self.alignments[x - 1] = aligns
            self.nb_zeros += 1
            k -= 1

    def terminalState(self):
        """
            Check the end of the game, which holds if :
            - The grid is full
            or
            - There is no new possible alignment
        """
        if self.nb_zeros == 0:
            return True

        currentX = self.currentX

        lst = np.argwhere(self.M == 0)
        len_lst = self.nb_zeros
        # Test for first player
        k = 0
        totalScores1 = self.totalScores[0]
        totalScores2 = self.totalScores[1]
        while k < len_lst:
            i = lst[k][0]
            j = lst[k][1]
            self.currentX = 1
            self.step((1, i, j))

            k += 1
            if self.totalScores[0] != totalScores1:
                self.unstep(max_unsteps=k)
                self.currentX = currentX
                return False

        self.unstep(max_unsteps=len_lst)
        # Test for second player
        k = 0
        while k < len_lst:
            i = lst[k][0]
            j = lst[k][1]
            self.currentX = 2
            self.step((2, i, j))

            k += 1
            if self.totalScores[1] != totalScores2:
                self.unstep(max_unsteps=k)
                self.currentX = currentX
                return False

        self.unstep(max_unsteps=len_lst)

        self.currentX = currentX
        return True

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
        for a in self.alignments[x - 1]:
            if len(a.intersection(align)) > 1:
                return False
        return True

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
            - the cell at (`i`,`j`) in the grid is available (== 0)
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

    def render(self, show_indices=True):
        """
            Arguments:
            ----------
            - `show_indices` : boolean

            Renders the board with indices if `show_indices` is true
            Credits : CorentinJ
        """

        hor_offset = '   ' if show_indices else ''
        hor_indices = hor_offset + \
            ''.join([' ' + str(i).rjust(2) + ' ' for i in range(self.m)])
        a = hor_offset + (' ___' * self.m)

        c = [hor_indices] if show_indices else []
        for i in range(self.n):
            b = [str(i).rjust(2)] if show_indices else []
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
