from PySide2 import QtCore, QtGui, QtWidgets
from datetime import datetime,timezone
from traceback import format_exception
import sys, shutil, os

class LineNumberArea(QtWidgets.QWidget):

    def __init__(self, editor):
        QtWidgets.QWidget.__init__(self, editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

class CodeEditor(QtWidgets.QPlainTextEdit):

    addLog = QtCore.Signal(str,str)

    def __init__(self):
        QtWidgets.QPlainTextEdit.__init__(self)

        self.line_number_area = LineNumberArea(self)
        self.setPlaceholderText("Ctrl+B to execute code")
        self.blockCountChanged[int].connect(self.update_line_number_area_width)
        self.updateRequest[QtCore.QRect, int].connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.setStyleSheet("CodeEditor{background-color:palette(base);padding-left:0}")
        self.setTabStopWidth(self.fontMetrics().width(' ') * 4)
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.update_line_number_area_width(0)
        self.highlight_current_line()
        self.addLog.connect(self.addLogText)

    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num *= 0.1
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def resizeEvent(self, e):
        super().resizeEvent(e)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        rect = QtCore.QRect(cr.left(), cr.top(), width, cr.height())
        self.line_number_area.setGeometry(rect)

    def lineNumberAreaPaintEvent(self, event):
        painter = QtGui.QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QtGui.QPalette().color(QtGui.QPalette.Mid).name())
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        offset = self.contentOffset()
        top = self.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QtCore.Qt.white)
                width = self.line_number_area.width()
                height = self.fontMetrics().height()
                painter.drawText(0, top, width-5, height,QtCore.Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    @QtCore.Slot()
    def update_line_number_area_width(self, newBlockCount):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    @QtCore.Slot()
    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            width = self.line_number_area.width()
            self.line_number_area.update(0, rect.y(), width, rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    @QtCore.Slot()
    def highlight_current_line(self):
    	
        extra_selections = []

        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()

            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)

            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def addLogText(self,text,type):

        self.moveCursor(QtGui.QTextCursor.End)
        tf = self.currentCharFormat()

        if type == "info":
            tf.setForeground(QtGui.QColor("#78ffa7"))
            self.setCurrentCharFormat(tf)
            label_log = "[INFO]"

        elif type == "error":
            tf.setForeground(QtGui.QColor("#ff5c57"))
            self.setCurrentCharFormat(tf)
            label_log = "[ERROR]"


        elif type == "warning":
            tf.setForeground(QtGui.QColor("#ffc978"))
            self.setCurrentCharFormat(tf)
            label_log = "[WARNING]"

        elif type == "log":
            tf.setForeground(QtGui.QColor("#44aaf2"))
            self.setCurrentCharFormat(tf)
            label_log = "[LOG]"

        elif type == "server":
            tf.setForeground(QtGui.QColor("#db44f2"))
            self.setCurrentCharFormat(tf)
            label_log = "[SERVER]"

        elif type == "sync":
            tf.setForeground(QtGui.QColor("#db44f2"))
            self.setCurrentCharFormat(tf)
            label_log = "[SYNC]"

        time = text.split(label_log)[0]
        text = "".join(text.split(label_log)[1:])


        self.insertPlainText(time)
        self.insertPlainText(label_log)
        tf.setForeground(QtGui.QColor("white"))
        self.setCurrentCharFormat(tf)
        self.insertPlainText(" {}\n".format(text))

        self.moveCursor(QtGui.QTextCursor.End)

    def openFile(self,file):

        self.clear()

        with open(file,"r") as read:

            lines = read.readlines()

            for line in lines:

                if "[ERROR]" in line:
                    self.addLogText(line.replace("\n",""),"error")

                elif "[WARNING]" in line:
                    self.addLogText(line.replace("\n",""),"warning")

                elif "[SYNC]" in line:
                    self.addLogText(line.replace("\n",""),"sync")

                else:
                    self.addLogText(line.replace("\n",""),"log")

class Console(QtWidgets.QPlainTextEdit):

    addConsole = QtCore.Signal(str,str or "log")
    onHashRate = QtCore.Signal(str)

    def __init__(self,save_path_log=None):

        QtWidgets.QPlainTextEdit.__init__(self)
        self.save_path_log = save_path_log
        self.setStyleSheet("Console{background-color:black}")
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse | QtCore.Qt.TextSelectableByKeyboard)
        # self.setTabStopWidth(self.fontMetrics().width(' ') * 4)
        self.addConsole.connect(self.addConsoleText)

    def addConsoleText(self,text,type="log"):

        self.moveCursor(QtGui.QTextCursor.End)

        tf = self.currentCharFormat()
        actual_time = str(datetime.now().strftime("[%d/%m/%y][%H:%M:%S]"))
        self.insertPlainText(actual_time)

        if type == "info":
            tf.setForeground(QtGui.QColor("#78ffa7"))
            self.setCurrentCharFormat(tf)
            label_log = "[INFO]"

        elif type == "error":
            tf.setForeground(QtGui.QColor("#ff5c57"))
            self.setCurrentCharFormat(tf)
            label_log = "[ERROR]"


        elif type == "warning":
            tf.setForeground(QtGui.QColor("#ffc978"))
            self.setCurrentCharFormat(tf)
            label_log = "[WARNING]"

        elif type == "log":
            tf.setForeground(QtGui.QColor("#44aaf2"))
            self.setCurrentCharFormat(tf)
            label_log = "[LOG]"

        elif type == "sync":
            tf.setForeground(QtGui.QColor("#db44f2"))
            self.setCurrentCharFormat(tf)
            label_log = "[SYNC]"


        if "Hashrate:" in text:

            self.onHashRate.emit(text)


        self.insertPlainText(label_log)
        tf.setForeground(QtGui.QColor("white"))
        self.setCurrentCharFormat(tf)
        self.insertPlainText(" {}\n".format(text))

        self.moveCursor(QtGui.QTextCursor.End)

        with open(self.save_path_log,"a") as w_log:
            w_log.write("{}{} {}\n".format(actual_time,label_log,text))
            
class ShellWidget(QtWidgets.QWidget):

    def __init__(self,local_log_path=None,server_log_path=None,parent=None):

        super(ShellWidget,self).__init__()
        global minervus
        minervus = parent

        self.local_log_path  = local_log_path
        self.server_log_path = server_log_path

        self.createWidgets()
        self.createLayout()
        self.createConnections()
        self.createStyle()

        sys.stdout     = Shell(self,"stdout",local_log_path,server_log_path)
        sys.stderr     = Shell(self,"stderr",local_log_path,server_log_path)

        if local_log_path: self.console.addConsole.emit("The log will be saved in: " + self.local_log_path,"log")

    def createWidgets(self):

        self.central_layout   = QtWidgets.QVBoxLayout(self)
        self.central_splitter = QtWidgets.QSplitter()
        self.console          = Console(self.local_log_path)
        self.code_editor      = CodeEditor()

    def createLayout(self):

        self.central_splitter.addWidget(self.console)
        self.central_splitter.addWidget(self.code_editor)
        self.central_layout.addWidget(self.central_splitter)

    def createConnections(self):

        self.execute_command_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+B'), self, self.executeCommand)

    def createStyle(self):

        self.central_layout.setContentsMargins(0,0,0,0)
        self.central_layout.setSpacing(0)

        self.central_splitter.setOrientation(QtCore.Qt.Vertical)
        self.central_splitter.setStretchFactor(0, 3)
        self.central_splitter.setStretchFactor(1, 1)

        self.central_splitter.setSizes([1, 0])

    def executeCommand(self):

        code = self.code_editor.toPlainText()
        for line in code.split("\n"):
            print(">>> {}".format(line))
        exec(code)

    def saveLOG(self):

        try:
            if self.local_log_path and self.server_log_path:
                shutil.copy2(self.local_log_path,self.server_log_path)
                print("The log has been saved in {}".format(self.server_log_path))
        except Exception as e:
            print("[ERROR] " + str(e))

class Shell(object):

    def __init__(self,shell_widget=False,type="stdout",local_log_path=None,server_log_path=None,verbose=False):
        
        if local_log_path: self.local_log_path  = local_log_path 
        if server_log_path: self.server_log_path = server_log_path 

        self.type = type

        self.createLog()

        if   type == "stdout":
            self.out = sys.stdout
        elif type == "stderr":
            self.err = sys.stderr

        sys.excepthook = self.writeError

        self.shell_widget    = shell_widget
        self.verbose         = verbose

    def createLog(self):

        if self.local_log_path:
            if not os.path.exists(os.path.dirname(self.local_log_path)): 
                os.makedirs(os.path.dirname(self.local_log_path))
        if self.server_log_path:
            if not os.path.exists(os.path.dirname(self.server_log_path)):
                if os.path.exists(USER_SERVER_DRIVE):
                    os.makedirs(os.path.dirname(self.server_log_path))

    def flush(self):
        try:
            if self.type == "stdout":
                self.out.flush()
            if self.type == "stderr":
                self.err = sys.stderr
        except:
            pass

    def write(self, message):

        message = message.replace("\n","")

        if not self.verbose:

            if message not in [""," "]:

                if "[ERROR]" in message:
                    self.shell_widget.console.addConsole.emit(message.replace("[ERROR]",""),"error")

                elif "[WARNING]" in message:
                    self.shell_widget.console.addConsole.emit(message.replace("[WARNING]",""),"warning")

                elif "[SYNC]" in message:
                    self.shell_widget.console.addConsole.emit(message.replace("[SYNC]",""),"sync")
                
                elif "Exception in thread" in message:
                    self.shell_widget.console.addConsole.emit(message,"error")

                elif "error:" in message.lower():
                    self.shell_widget.console.addConsole.emit(message,"error")

                else:
                    self.shell_widget.console.addConsole.emit(message,"log")

    def writeError(self,type_, value, traceback):
        tab = ""
        for message in format_exception(type_, value, traceback):
            if message[0] == " ": message = message[1:]
            print("[ERROR] {}{}".format(tab,message))
            tab += "     "






if __name__ == "__main__":

    pass