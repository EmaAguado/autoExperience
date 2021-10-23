# import sys
# sys.path.append("../")
from PySide2 import QtCore, QtGui, QtWidgets, QtUiTools, QtMultimedia, QtXml
from ui.palette import styleS, stylesheet
from ui.widget import customWidgets
import autoExperience
import win32api,win32con,win32gui
from ctypes.wintypes import POINT
import ctypes.wintypes

#GLOBALS
class MINMAXINFO(ctypes.Structure):
    _fields_ = [
        ("ptReserved",      POINT),
        ("ptMaxSize",       POINT),
        ("ptMaxPosition",   POINT),
        ("ptMinTrackSize",  POINT),
        ("ptMaxTrackSize",  POINT),
    ]

class MainWindow(QtWidgets.QFrame):

    BorderWidth = 10

    def __init__(self, widget=None, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setObjectName("MainWindow")
        self.cursor = QtGui.QCursor()
        self.createHeader()
        self.createWidgets()
        self.createLayout()
        self.addLayout()
        self.createStyle()
        self.widget = widget
        if self.widget:
            self.addWidget(self.widget)

    def paintEvent(self, event=None):
        
        painter = QtGui.QPainter(self)

        painter.setOpacity(0.004)
        painter.setBrush(QtCore.Qt.black)
        painter.setPen(QtGui.QPen(QtCore.Qt.black))   
        painter.drawRect(self.rect())

        painter.setOpacity(100)
        painter.setBrush(QtGui.QColor(10,10,10))#QPalette().color(QtGui.QPalette.Base))
        painter.setPen(QtGui.QColor(10,10,10))#QtGui.QPen(QtGui.QPalette().color(QtGui.QPalette.Base)))
        painter.drawRect(QtCore.QRect(self.BorderWidth, self.BorderWidth, self.width()-((self.BorderWidth*2) + 1), 24))

        return super(MainWindow,self).paintEvent(event)

    def createHeader(self):

        self.header_layout = QtWidgets.QHBoxLayout()
        self.header_layout.setSpacing(0)
        self.header_layout.setContentsMargins(0,0,0,0)

        self.icon = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("./ui/resources/img/logo.png")
        pixmap = pixmap.scaled(24, 24, QtCore.Qt.KeepAspectRatio) 
        self.icon.setPixmap(pixmap)
        self.title = QtWidgets.QLabel("Dragonary Auto Experience")
        self.title.setStyleSheet("*{margin-left:10px}")
        self.version = QtWidgets.QLabel("- {}".format(autoExperience.__version__))
        self.spacer = QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.title.setMinimumHeight(24)
        self.title.setMaximumHeight(24)

        self.bminimize = customWidgets.AToolButton()
        self.bminimize.setIcon(QtGui.QIcon("./ui/resources/img/minimize.png"))
        self.bminimize.setAnimation(150,QtGui.QColor(10,10,10),QtGui.QPalette().color(QtGui.QPalette.AlternateBase).name())
        self.bminimize.setMinimumSize(30,24)
        self.bminimize.setMaximumSize(30,24)

        self.bmaximize = customWidgets.AToolButton()
        self.bmaximize.setIcon(QtGui.QIcon("./ui/resources/img/maximize.png"))
        self.bmaximize.setAnimation(150,QtGui.QColor(10,10,10),QtGui.QPalette().color(QtGui.QPalette.AlternateBase).name())
        self.bmaximize.setMinimumSize(30,24)
        self.bmaximize.setMaximumSize(30,24)

        self.bclose = customWidgets.AToolButton()
        self.bclose.setAnimation(150,QtGui.QColor(10,10,10),"#CA3433")
        self.bclose.setIcon(QtGui.QIcon("./ui/resources/img/close.png"))
        self.bclose.setMinimumSize(30,24)
        self.bclose.setMaximumSize(30,24)

        self.header_layout.addWidget(self.icon)
        self.header_layout.addWidget(self.title)
        self.header_layout.addWidget(self.version)
        self.header_layout.addItem(self.spacer)
        self.header_layout.addWidget(self.bminimize)
        self.header_layout.addWidget(self.bmaximize)
        self.header_layout.addWidget(self.bclose)

        self.bminimize.clicked.connect(lambda:self.showMinimized())
        self.bmaximize.clicked.connect(lambda:self.showMaximized())
        self.bclose.clicked.connect(lambda:self.close())

    def createWidgets(self):

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setObjectName("central_widget")
        self.central_layout = QtWidgets.QVBoxLayout(self.central_widget)

    def createLayout(self):

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addWidget(self.central_widget)

    def addLayout(self):

        pass

    def addWidget(self,widget):

        self.widget = widget
        self.central_layout.addWidget(self.widget)

    def createStyle(self):

        self.setStyleSheet(stylesheet.data)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setMinimumSize(QtCore.QSize(500,200))
        self._rect = QtWidgets.QApplication.instance().desktop().availableGeometry(self)
        self.resize(800, 600)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint
                            | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint| QtCore.Qt.WindowCloseButtonHint)
        style = win32gui.GetWindowLong(int(self.winId()), win32con.GWL_STYLE)
        win32gui.SetWindowLong(int(self.winId()), win32con.GWL_STYLE, style | win32con.WS_THICKFRAME)

        self.main_layout.setContentsMargins(self.BorderWidth,self.BorderWidth,self.BorderWidth,self.BorderWidth)
        self.main_layout.setSpacing(0)

        self.central_layout.setContentsMargins(0,0,0,0)
        self.central_layout.setSpacing(0)

        self.central_widget.setStyleSheet("#central_widget{background-color:palette(mid)}")

        self.version.setStyleSheet('font-size:8px "Consolas";color:grey')

        # sh = QtWidgets.QGraphicsDropShadowEffect(self.central_widget)
        # sh.setColor(QtGui.QColor(0,0,0,122))
        # sh.setBlurRadius(0)
        # sh.setYOffset(2)
        # sh.setXOffset(0)
        # self.central_widget.setGraphicsEffect(sh)

    def nativeEvent(self, eventType, message):

        if eventType == "windows_generic_MSG":

            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            pos = self.mapFromGlobal(self.cursor.pos())
            x = pos.x()
            y = pos.y()

            if msg.message == win32con.WM_NCCALCSIZE:

                return True, 0

            elif self.childAt(x,y) != None:

                return super(MainWindow, self).nativeEvent(eventType, message)


            elif msg.message == win32con.WM_GETMINMAXINFO:

                info = ctypes.cast(msg.lParam, ctypes.POINTER(MINMAXINFO)).contents
                info.ptMaxSize.x = self._rect.width()
                info.ptMaxSize.y = self._rect.height()
                info.ptMaxPosition.x, info.ptMaxPosition.y = 0,0 

            elif msg.message == win32con.WM_NCHITTEST:

                w, h = self.width(), self.height()
                lx = x < self.BorderWidth
                rx = x > w - self.BorderWidth
                ty = y < self.BorderWidth
                by = y > h - self.BorderWidth

                if (lx and ty):
                   return True, win32con.HTTOPLEFT
                elif (rx and by):
                   return True, win32con.HTBOTTOMRIGHT
                elif (rx and ty):
                   return True, win32con.HTTOPRIGHT
                elif (lx and by):
                   return True, win32con.HTBOTTOMLEFT
                elif ty:
                   return True, win32con.HTTOP
                elif by:
                   return True, win32con.HTBOTTOM
                elif lx:
                   return True, win32con.HTLEFT
                elif rx:
                   return True, win32con.HTRIGHT
                       
                return True, win32con.HTCAPTION

            return super(MainWindow, self).nativeEvent(eventType, message)

    def closeEvent(self,event):

        try:
            self.widget.close()
        except:
            pass

        super(MainWindow, self).closeEvent(event)

if __name__ == '__main__':

    import sys
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(styleS.autoStyle())

    main_ui = MainWindow()
    main_ui.show()

    sys.exit(app.exec_())