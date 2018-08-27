import random

MAZE_SIZE = 7

if __name__ == '__main__':
    board = []
    for k in range(10):
        for i in range(MAZE_SIZE):
            row = []
            for j in range(MAZE_SIZE):
                if (i == 0) or (j == 0) or (i == MAZE_SIZE - 1) or (j == MAZE_SIZE - 1):
                    row.append('%')
                elif random.random() < 0.3:
                    row.append('.')
                else:
                    row.append(' ')
            board.append(row)

        rand_pos = [random.randint(1,6), random.randint(1,6)]
        board[rand_pos[0]][rand_pos[1]] = 'P'

        with open('random%dx%d_%d.lay' % (MAZE_SIZE, MAZE_SIZE, k + 1), 'w') as f:
            f.write('\n'.join([''.join(b) for b in board]))