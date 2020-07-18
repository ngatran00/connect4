import math
import time

from functools import partial

import connect4

from PyQt5.QtWidgets import QApplication, QPushButton, QMessageBox, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QLine


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Connect 4"

        self.top = 200
        self.left = 100
        self.width = 265
        self.height = 275
        self.paintCircle = False
        self.line = QLine()

        self.circles_filled = {}

        for i in range(7):
            for j in range(6):
                self.circles_filled[(i, j)] = False

        self.circles_pos = {}

        self.space = 35
        start_x = 15
        start_y = 20

        x = range(start_x, start_x+ self.space*7, self.space)
        y = range(start_y, start_y+ self.space*6, self.space)[::-1]

        for i in range(7):
            for j in range(6):
                self.circles_pos[(i, j)] = (x[i], y[j])

        self.c4 = connect4.Connect4()

        c = ["-"]*7
        self.board = [c] * 6

        self.init_window()

    def init_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        l1 = QPushButton('1', self)
        l2 = QPushButton('2', self)
        l3 = QPushButton('3', self)
        l4 = QPushButton('4', self)
        l5 = QPushButton('5', self)
        l6 = QPushButton('6', self)
        l7 = QPushButton('7', self)

        self.buttons = [l1, l2, l3, l4, l5, l6, l7]

        x = 10

        for i, l in enumerate(self.buttons):
            l.move(x, 240)
            l.resize(32, 32)
            x += 35
            self.btnCallBack = partial(self.setUserMove, i)
            l.clicked.connect(self.btnCallBack)

        self.setFixedSize(self.width, self.height)

        self.bot = True

        for button in self.buttons:
            button.setDisabled(True)
        self.setBotMove()
        self.show()

    def setUserMove(self, user_col):
        if self.c4.finish(self.board) == -1 and not self.c4.full(self.board):
            valid = False
            while not valid:
                for button in self.buttons:
                    button.setDisabled(False)
                for row, i in enumerate(range(5, -1, -1)):
                    if self.board[i][user_col] == "-":
                        self.board[i][user_col] = "X"
                        self.color = Qt.green
                        self.circles_filled[(user_col, row)] = Qt.green
                        time.sleep(0.5)
                        valid = True
                        break
                else:
                    QMessageBox.about(self, "Error", "Invalid input")

            self.bot = not self.bot

        if self.c4.finish(self.board) != -1 or self.c4.full(self.board):
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Game Over")
            msgBox.setStandardButtons(QMessageBox.Ok)
            if self.c4.finish(self.board) == 0:
                msgBox.setText("Computer wins")
            elif self.c4.finish(self.board) == 1:
                msgBox.setText("Player wins")
            elif self.c4.full(self.board):
                msgBox.setText("Tie")

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                self.close()

        else:
            self.setBotMove()

    def setBotMove(self):
        if self.c4.finish(self.board) == -1 and not self.c4.full(self.board):
            b, score = self.c4.minimax(self.board, not self.bot, -math.inf, math.inf, 7)
            for row in range(6):
                diff = [b[row][col] == self.board[row][col] for col in range(7)]
                if False in diff:
                    col = diff.index(False)
                    self.board = b
                    self.color = Qt.red
                    self.circles_filled[(col, 5-row)] = Qt.red
                    self.changeColor()
                    for button in self.buttons:
                        button.setDisabled(False)
                    break

            self.bot = not self.bot

        if self.c4.finish(self.board) != -1 or self.c4.full(self.board):
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Game Over")
            msgBox.setStandardButtons(QMessageBox.Ok)
            if self.c4.finish(self.board) == 0:
                msgBox.setText("Computer wins")
            elif self.c4.finish(self.board) == 1:
                msgBox.setText("Player wins")
            elif self.c4.full(self.board):
                msgBox.setText("Tie")

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                self.close()

    def changeColor(self):
        self.paintCircle = True
        self.update()

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))

        painter.drawRect(5, 10, self.space*7+10, self.space*6+10)

        for (val, (x, y)) in self.circles_pos.items():
            painter.drawEllipse(x, y, 20, 20)

        for i in range(7):
            for j in range(6):
                color = self.circles_filled[(i, j)]
                if color:
                    painter.setBrush(QBrush(color, Qt.SolidPattern))
                    x, y = self.circles_pos[(i, j)]
                    painter.drawEllipse(x, y, 20, 20)

        if self.paintCircle:
            self.paintCircle = False


if __name__ == "__main__":

    app = QApplication([])

    window = Window()

    app.exec_()
