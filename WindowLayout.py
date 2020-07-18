import sys
from PyQt5.QtGui import (QKeySequence,
                         QTextDocument,
                         QFont)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyNotepad import *
class MyMainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.resize(1024, 768)
        
        self.app = app
        app.setApplicationName("PyNotepad")

        self.editor = QPlainTextEdit()
        self.editor.document().setDefaultFont(QFont("monospace"))
        self.setWindowTitle("PyNotepad")
        self.setCentralWidget(self.editor)  

        self.treeview()

    def closeEvent(self, e):
        if not self.editor.document().isModified():
            return
        answer = self.ask_for_confirmation()
        if answer == QMessageBox.Save:
            if not self.save():
                e.ignore()
        elif answer == QMessageBox.Cancel:
            e.ignore()

    def treeview(self):
        dockWidget = QDockWidget('Dock', self)

        self.treeview = QTreeView()
        self.listview = QListView()

        path = QDir.rootPath()

        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(QDir.rootPath())
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)

        self.treeview.setModel(self.dirModel)
        self.treeview.setRootIndex(self.dirModel.index(path))
        self.treeview.doubleClicked.connect(self.on_double_clicked)
             
        dockWidget.setWidget(self.treeview)
        dockWidget.setFloating(False)

        self.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)
        self.treeview.expandAll()

    def on_double_clicked(self, index):
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        if path:
            self.file_contents = ""
            with open(path, 'r') as f:
                self.file_contents = f.read()
            self.editor.setPlainText(self.file_contents)
            self.file_path = path