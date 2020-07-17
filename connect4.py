import math
import random


class Connect4:

    def check_horizontal(self, board):
        for row in range(6):
            for column in range(4):
                if board[row][column] == board[row][column+1] == board[row][column+2] == board[row][column+3]:
                    if board[row][column] == "X":
                        return 1
                    elif board[row][column] == "O":
                        return 0
        else:
            return -1

    def check_vertical(self, board):
        for column in range(7):
            for row in range(3):
                if board[row][column] == board[row+1][column] == board[row+2][column] == board[row+3][column]:
                    if board[row][column] == "X":
                        return 1
                    elif board[row][column] == "O":
                        return 0
        else:
            return -1

    def check_diagonal(self, board):
        for column in range(4):
            for row in range(3):
                if board[row][column] == board[row+1][column+1] == board[row+2][column+2] == board[row+3][column+3]:
                    if board[row][column] == "X":
                        return 1
                    elif board[row][column] == "O":
                        return 0
        for column in range(6, 2, -1):
            for row in range(3):
                if board[row][column] == board[row+1][column-1] == board[row+2][column-2] == board[row+3][column-3]:
                    if board[row][column] == "X":
                        return 1
                    elif board[row][column] == "O":
                        return 0
        else:
            return - 1

    def finish(self, board):
        vertical = self.check_vertical(board)
        horizontal = self.check_horizontal(board)
        diagonal = self.check_diagonal(board)
        if vertical != -1:
            return vertical
        elif horizontal != -1:
            return horizontal
        elif diagonal != -1:
            return diagonal
        else:
            return -1

    def full(self, board):
        full_row = 0
        for row in board:
            if row.count("-") == 0:
                full_row += 1
        if full_row == 6:
            return False

    def generate_node(self, board, player):
        nodes = []
        if not player:
            for value in range(7):
                current = [x[:] for x in board]
                for i in range(5, -1, -1):
                    if current[i][value] == "-":
                        current[i][value] = "O"
                        break
                    else:
                        continue
                nodes.append(current)
        elif player:
            for value in range(7):
                current = [x[:] for x in board]
                for i in range(5, -1, -1):
                    if current[i][value] == "-":
                        current[i][value] = "X"
                        break
                    else:
                        continue
                nodes.append(current)
        return nodes

    def heuristic(self, board):
        value = 0

        if self.finish(board) == 1:
            value += 100
        elif self.finish(board) == 0:
            value -= 100

        # Check for threats vertically
        for row in range(6):
            column = 0
            while column < 6:
                if board[row][column] == board[row][column+1]:
                    if board[row][column] == "X":
                        value += 2
                    elif board[row][column] == "O":
                        value -= 2
                    if (column < 5) and (board[row][column] == board[row][column+2]):
                        if board[row][column] == "X":
                            value += 5
                        elif board[row][column] == "O":
                            value -= 5
                column += 1

        # Check for threats horizontally
        for column in range(7):
            row = 0
            while row < 5:
                if board[row][column] == board[row+1][column]:
                    if board[row][column] == "X":
                        value += 2
                    elif board[row][column] == "O":
                        value -= 2
                    if (row < 4) and (board[row][column] == board[row+2][column]):
                        if board[row][column] == "X":
                            value += 5
                        elif board[row][column] == "O":
                            value -= 5
                row += 1

        # Check for threats diagonally
        for column in range(4):
            row = 0
            while row < 5:
                if board[row][column] == board[row+1][column+1]:
                    if board[row][column] == "X":
                        value += 2
                    elif board[row][column] == "O":
                        value -= 2
                    if (row < 4) and (column < 5) and (board[row][column] == board[row+2][column+2]):
                        if board[row][column] == "X":
                            value += 5
                        elif board[row][column] == "O":
                            value -= 5
                row += 1
        for column in range(6, 2, -1):
            row = 0
            while row < 5:
                if board[row][column] == board[row+1][column-1]:
                    if board[row][column] == "X":
                        value += 2
                    elif board[row][column] == "O":
                        value -= 2
                    if (row < 4) and (column < 5) and (board[row][column] == board[row+2][column+2]):
                        if board[row][column] == "X":
                            value += 5
                        elif board[row][column] == "O":
                            value -= 5
                row +=1

        return value

    def minimax(self, board, bot, alpha, beta, depth):
        if self.finish(board) == 0:
            return None, -10000
        elif self.finish(board) == 1:
            return None, 10000
        elif self.full(board):
            return None, 0
        elif depth == 0:
            return None, self.heuristic(board)

        if bot:
            best_score = -math.inf
            new_score = lambda x: x > best_score
        else:
            best_score = math.inf
            new_score = lambda x: x < best_score

        nodes = self.generate_node(board, bot)
        current = nodes[random.randrange(len(nodes))]
        for node in nodes:

            temp = self.minimax(node, not bot, alpha, beta, depth-1)[1]
            if new_score(temp):
                current = node
                best_score = temp
            if bot:
                alpha = max(alpha, temp)
            else:
                beta = min(beta, temp)
            if alpha >= beta:
                break

        return current, best_score

    def print_board(self, board):
        print("#############")
        print("0 1 2 3 4 5 6")
        for row in board:
            row = " ".join(row)
            print(row)
        print("#############")


if __name__ == "__main__":
    c4 = Connect4()

    bot = True

    c = ["-"]*7
    board = [c] * 6

    while c4.finish(board) == -1 and not c4.full(board):

        if bot:
            b, score = c4.minimax(board, not bot, -math.inf, math.inf, 7)
            board = b
            c4.print_board(board)

        else:
            valid = False
            while not valid:
                user = int(input("Player's turn: "))
                for i in range(5, -1, -1):
                    if board[i][user] == "-":
                        board[i][user] = "X"
                        valid = True
                        break
                else:
                    print("Invalid")
            c4.print_board(board)

        bot = not bot

    if c4.finish(board) == 0:
        print("Computer wins")
    elif c4.finish(board) == 1:
        print("Player wins")
    else:
        print("Tie")
