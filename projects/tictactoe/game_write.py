import numpy as np
import sys
from game import play

# XXX: Do not modify anything.


if __name__ == "__main__":
    res = play(sys.argv)
    f = open(sys.argv[6], "w+")
    if res != -1:
        nact, t, env = res
        state = env.currentState()
        score = state[2]
        winner = np.argmax(score) + 1 if score[0] != score[1] else 0
        f.write(str(winner) +
                ";" +
                str(score[0]) +
                ";" +
                str(score[1]) +
                ";" +
                str(nact[0]) +
                ";" +
                str(nact[1]) +
                ";" +
                str(t[0]) +
                ";" +
                str(t[1]))
    else:
        f.write("Err")
    f.close()
