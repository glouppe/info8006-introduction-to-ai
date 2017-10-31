import numpy as np
# XXX: Do not modify anything.

"""
    Tic tac toe environment class
    An alignment is either a column, a line or a diagonal of any size in a grid which repeats a symbol 
    Scoring of a player S in a grid _*_*k : maximum number of alignments of size k with symbol S subject to the following constraint : all pairs of alignments cannot share more than 1 cell.
"""

class Tictactoe(object):
    """
        Arguments:
        ----------
        - `n`: the number of lines of the grid
        - `m`: the number of columns of the grid
        - `k`: the size of an alignment.
    """
    def __init__(self,n,m,k):
        self.n = n
        self.m = m
        self.k = k
        self.reset()

    """
        Resets the environment to an empty grid of size n*m and a random initial symbol
    """
    def reset(self):
        self.currentX = np.random.randint(1,3)
        self.M = np.zeros((self.n,self.m))
        self.totalScores = [0,0]
        self.alignments = [[],[]]
        
    """
        Arguments:
        ----------
        - `action = (x,i,j)` : a triplet of integers
        
        If `action` is valid, replace the empty cell self.M[i,j] by x and update the current state (scoring and alignments)
    """
    def step(self, action):
        if not self.checkAction(action):
            self.currentX = 3 - self.currentX
            return
        self.M[i,j] = x
        i = self.updateScore(action)
        self.totalScores[self.currentX-1] += i
        if i == 0:
                self.currentX = 3 - self.currentX
        
    """
        Arguments:
        ----------
        - `align` : a list of pair of integers
        - 'x' : a symbol
        
        Returns True if `align` to be of size k and to not share more than one symbol with the others existing alignments
    """           
    def checkAlignment(self,align,x):
        if len(align) != self.k:
                return False
        return len(filter(lambda x : len(x.intersection(align)) > 1,self.alignments[x-1])) == 0

    """
        Arguments:
        ----------
        - `i` : a list of pair of integers
        - 'j' : a symbol
        
        Returns true if `i` and `j` are valid coordinates in current grid
    """   
    def checkCoordinates(self,i,j):
        return i >= 0 and i < self.n and j >= 0 and j < self.m
        
    """
        Arguments:
        ----------
        - `action = (x,i,j)` : a triplet of integers
        
        Returns true if `i` and `j` are valid coordinates in current grid and x is the current symbol to play and the cell at (`i`,`j`) in the grid is available (= 0)
    """
    def checkAction(self,action):
        x,i,j = action
        return self.checkCoordinates(i,j) and self.currentX == x and self.M[i,j] == 0
        
    """
        Arguments:
        ----------
        - `action = (x,i,j)` : a triplet of integers
        
        Returns number of new alignments made with the symbol `x` at cell (`i`,`j`) and adjacents cells
    """
    def updateScore(self,action):
        x,i,j = action
        k = self.k
        intervals = [[(i-k+1,j-k+1),(i+k-1,j+k-1)],[(i-k+1,j),(i+k-1,j)],[(i,j-k+1),(i,j+k-1)],[(i+k-1,j-k+1),(i-k+1,j+k-1)]]
        s = 0
        print intervals
        for interval in intervals:
                iStart,jStart = interval[0]
                iEnd,jEnd = interval[1]
                iTemp, jTemp = (iStart,jStart)
                align = []
                alignIdx = []
                while iTemp != iEnd or jTemp != jEnd:
                    if self.checkCoordinates(iTemp,jTemp):
                        alignIdx.append((iTemp,jTemp))
                        align.append(self.M[iTemp,jTemp])
                    iTemp += 1 if iTemp < iEnd else (-1 if iTemp > iEnd else 0)
                    jTemp += 1 if jTemp < jEnd else (-1 if jTemp > jEnd else 0)
                if self.checkCoordinates(iEnd,jEnd):
                    alignIdx.append((iEnd,jEnd))
                    align.append(self.M[iEnd,jEnd])
                print alignIdx
                iBegin = 0
                iEnd = k
                len_align = len(align)
                for h in range(len_align - k + 1):
                    alignIdx2 = set(alignIdx[iBegin:iEnd])
                    align2 = np.asarray(align[iBegin:iEnd]) == x
                    if np.all(align2) and self.checkAlignment(alignIdx2,x):
                        self.alignments[x-1].append(alignIdx2)
                        s += 1
                    iBegin += 1
                    iEnd += 1
        
        return s
    """
        Renders the board
    """                  
    def render(self):
        board = ''

        a = (' ___' *  self.m )
        c = []
         
        c = []
        for i in range(self.n):
                b = []
                for j in range(self.m):
                        b.append('|')
                        b.append("X" if self.M[i][j] == 1 else ("O" if self.M[i][j] == 2 else " "))
                b.append('|')
                b = ' '.join(b)
                c.extend([a,b])
        c.append(a)
        print('\n'.join(tuple(c)))
        
    """
        Returns the current state (grid,current symbol, total score (of) and alignments (made by) the two players 
    """        
    def current_state(self):
        return (self.M,self.currentX,self.totalScores,self.alignments)


                print "current score is " + " ".join(map(str,env.current_state()[2]))
                print "Alignments for current player : "
                print env.alignments[env.currentX - 1]
