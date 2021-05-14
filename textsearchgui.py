import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit)
import reg2nfa
import statemanager
import time


# txt = "1001 10000 10000000 100000000 000000000000 1010111101 101001 1001001 1001010011 0101101 001 10100 1010100 0100001 0000001 000000"
class TextEdit(QMainWindow):
    def __init__(self, regex=' ', txt=" ", parent=None):
        super(TextEdit, self).__init__(parent)

        self.regex = regex
        self.txt = txt

        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.textEdit.setText(txt)

        self.setGeometry(500, 300, 600, 200)
        self.textEdit.resize(600, 200)

        self.wait(0.2)

        nfaController = reg2nfa.formal_nfa(self.regex)
        controlManager = statemanager.CheckStateManager(nfaController)

        start = 0
        for i, char in enumerate(txt):
            if char == " ":
                self.highlight(start, i - start, 2)
                self.wait(0.4)
                print(txt[start: i])
                if controlManager.checkString(txt[start: i]):
                    self.highlight(start, i - start, 1)
                else:
                    self.highlight(start, i - start, 3)
                start = i + 1

        self.setCentralWidget(self.textEdit)

    def highlight(self, start, n, col):
        cursor = self.textEdit.textCursor()
        clr = QColor(0, 0, 0)
        if col == 1:
            clr = QColor(0, 255, 0)
        elif col == 2:
            clr = QColor(255, 255, 0)
        elif col == 3:
            clr = clr = QColor(0, 0, 0)

        # metin rengi
        fmt = QTextCharFormat()
        fmt.setForeground(clr)

        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.Right,
                            QTextCursor.KeepAnchor, n)  # keepanchor, merge bak
        cursor.mergeCharFormat(fmt)

    def wait(self, second):
        self.show()
        QCoreApplication.processEvents() #Belirtilen bayraklara göre çağıran iş parçacığı için bazı bekleyen olayları işleyen fonk.
        time.sleep(second)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    textEdit = TextEdit('(ab)*', 'aba abbbaa abaaa aba ab ')
    textEdit.show()

    sys.exit(app.exec_())
