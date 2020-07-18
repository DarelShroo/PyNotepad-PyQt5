import sys
from PyQt5.QtGui import (QKeySequence,
                         QTextDocument,
                         QFont)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyNotepad import *



if __name__ == '__main__':
    app = QApplication(sys.argv)
    pynotepad = PyNotepad(app)
    pynotepad.show()
    sys.exit(app.exec_())
