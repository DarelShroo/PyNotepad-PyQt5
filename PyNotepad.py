import sys
from PyQt5.QtGui import (QKeySequence,
                         QTextDocument,
                         QFont)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from WindowLayout import *
class PyNotepad(MyMainWindow):
    def __init__(self, app):
        super().__init__(app)   
        self.app = app  

        self.file_menu = self.menuBar().addMenu("&File")
        self.file_path = None
        
        self.conn_action()  
        
    def ask_for_confirmation(self):
        answer = QMessageBox.question(self, "Confirm closing",
                 "You have unsaved changes. Are you sure you want to exit?", 
                 QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        return answer

    def show_open_dialog(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Open...')
        if self.filename:
            self.file_contents = ""
            with open(self.filename, 'r') as f:
                self.file_contents = f.read()
            self.editor.setPlainText(self.file_contents)
            self.file_path = self.filename

    def show_save_dialog(self):
        self.filename, _ = QFileDialog.getSaveFileName(self, 'Save as...')
        if self.filename:
            self.file_path = self.filename
            self.save()
            return True
        return False
    
    def show_about_dialog(self):
        self.text = """
            <center>
                <h1>PyNotepad</h1><br/>
                <img src=logo.png width=200 height=200>
            </center>
            <p>Version 0.0.1</p>
            """
        QMessageBox.about(self, "About PyNotepad", self.text)

    def new_document(self):
        if self.editor.document().isModified():
            answer = self.ask_for_confirmation()
            if answer == QMessageBox.Save:
                if not self.save():
                    return
            elif answer == QMessageBox.Cancel:
                return
        self.editor.clear()
        self.file_path = None

    def save(self):
        if self.file_path is None:
            return self.show_save_dialog()
        else:
            with open(self.file_path, 'w') as f:
                f.write(self.editor.toPlainText())
            self.editor.document().setModified(False)
            return True

    def conn_action(self):
        self.new_action = QAction("&New document")
        self.new_action.triggered.connect(self.new_document)
        self.new_action.setShortcut(QKeySequence.New)
        self.file_menu.addAction(self.new_action)    

        self.open_action = QAction("&Open file...")
        self.open_action.triggered.connect(self.show_open_dialog)
        self.open_action.setShortcut(QKeySequence.Open)
        self.file_menu.addAction(self.open_action)      

        self.save_action = QAction("&Save")
        self.save_action.triggered.connect(self.save)
        self.save_action.setShortcut(QKeySequence.Save)
        self.file_menu.addAction(self.save_action)
    
        self.close_action = QAction("&Close")
        self.close_action.triggered.connect(self.close)
        self.close_action.setShortcut(QKeySequence.Quit)
        self.file_menu.addAction(self.close_action)

        self.help_menu = self.menuBar().addMenu("&Help")
        self.about_action = QAction("&About")
        self.about_action.triggered.connect(self.show_about_dialog)
        self.help_menu.addAction(self.about_action)