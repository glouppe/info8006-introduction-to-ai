import numpy as np
import sys
from human import Human
from importlib import import_module
from tictactoe import Tictactoe
from copy import deepcopy
import thread
import threading
import time

# XXX: Do not modify anything.

TIMEOUT = 60.0

"""
    Main program 
Play tic tac toe. Players are either AIs or humans.
Arguments:
- n : (int) Number of lines
- m : (int) Number of columns
- k : (int) Size of alignments
- p1 : (str) Player, 'h' for human and 'c_`class`' for computer
- p2 : (str) Player, 'h' for human and 'c_`class`' for computer
        - `class` is the name of your python file. The name of the class inside this file has to be `Class`
        - Random selection of the first player.
    
"""
def help():
        print """
Main program 
Play tic tac toe. Players are either AIs or humans.
Arguments:
- n : (int) Number of lines
- m : (int) Number of columns
- k : (int) Size of alignments
- p1 : (str) Player, 'h' for human and 'c_`class`' for computer
- p2 : (str) Player, 'h' for human and 'c_`class`' for computer
        - `class` is the name of your python file. The name of the class inside this file has to be `Class`
        - Random selection of the first player.
        """

def f_with_timeout(f,*args):
    
    timer = threading.Timer(TIMEOUT, thread.interrupt_main)
    out = None
    t = time.time()
    try:
        timer.start()
        out = f(*args)
    except KeyboardInterrupt:
        pass
    t = time.time() - t
    timer.cancel()
    return (t,out)

def extractAgent(module_name,player,k):
    mod = __import__(module_name)
    return getattr(mod, module_name.capitalize())(player,k)

def play(args):
        if len(args) < 6:
                help()
                return -1
                
        try:
                n = int(args[1])
        except:
                help()
                return -1
        try:
                m = int(args[2])
        except:
                help()
                return -1
                
        try:
                k = int(args[3])
        except:
                help()
                return -1
                
        try:
                p1 = args[4]
                if p1[0] != "h":
                       name = p1.split("_")[1]
                       p1 = extractAgent(name, 1, k)
                else:
                       p1 = Human(1,k)       
        except:
                help()
                return -1
                
        try:
                p2 = args[5]
                if p2[0] != "h":
                        name = p2.split("_")[1]
                        p2 = extractAgent(name, 2, k) 
                else:
                        p2 = Human(2,k)       
        except:
                help()
                return -1           
        env = Tictactoe(n,m,k)
        p = [p1,p2]
        t = [0,0]
        nact = [0,0]
        while not env.terminalState():
                _,currentPlayer,_,_ = env.currentState()
                tX,act = f_with_timeout(p[currentPlayer - 1].move,deepcopy(env)) 
                print act
                if act is not None:
                        i,j = act
                        env.step((currentPlayer,i,j))
                else:
                        env.step((currentPlayer,-1,-1))
                t[currentPlayer-1] += tX
                nact[currentPlayer-1] += 1
        env.render()
        currState = env.currentState()
        return (nact,t,np.argmax(currState[2])+1, currState)

if __name__=="__main__":
        res = play(sys.argv)
        if res != -1:
                nact,t,winner,state = res  
                score = state[2]
                print "Winner is player " + str(winner)
                print "Score per player: " + "/".join(map(str,score))
                print "Number of moves per player : " + "/".join(map(str,nact))
                print "Play time per player : " + "/".join(map(str,t))
        
