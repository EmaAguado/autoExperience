from PySide2 import QtWidgets,QtCore,QtGui
import autoExperience
class Loading(QtWidgets.QMainWindow):

    onClose = QtCore.Signal()
    
    def __init__(self):

        super(Loading,self).__init__()
        self.createWidgets()
        self.createLayout()
        self.createConnections()
        self.createStyle()
        self.show()

    def createWidgets(self):

        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)

        self.central_widget = QtWidgets.QWidget()
        self.central_layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.bottom_layout = QtWidgets.QHBoxLayout()

        self.title         = QtWidgets.QLabel("DRAGONARY AUTOEXPERIENCE")
        self.loading_gif   = QtGui.QMovie("./ui/resources/img/loading.gif")
        self.label_loading = QtWidgets.QLabel()
        self.log           = QtWidgets.QLabel()
        self.version       = QtWidgets.QLabel("version: "+autoExperience.__version__)
        self.owner         = QtWidgets.QLabel(autoExperience.__owner__)
        self.label_loading.setMovie(self.loading_gif)
        self.loading_gif.start()


    def createLayout(self):

        self.setCentralWidget(self.main_widget)
        self.main_layout.addWidget(self.central_widget)

        self.central_layout.addWidget(self.title)
        self.central_layout.addWidget(self.label_loading)
        self.central_layout.addWidget(self.log)
        self.central_layout.addLayout(self.bottom_layout)

        self.bottom_layout.addWidget(self.version)
        self.bottom_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.bottom_layout.addWidget(self.owner)

    def createConnections(self):

        self.onClose.connect(self.close)

    def createStyle(self):

        self.setStyleSheet("background-color:rgba(68,27,116,0)")
        self.central_widget.setStyleSheet("background-color:rgb(68,27,116);border-radius:5px")
        self.label_loading.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.log.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.log.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint) 
        self.resize(400, 400) 
        self.move(QtWidgets.QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())

        self.sh = QtWidgets.QGraphicsDropShadowEffect(self)
        self.sh.setColor(QtGui.QColor(0,0,0,255))
        self.sh.setBlurRadius(20)
        self.sh.setYOffset(0)
        self.sh.setXOffset(0)
        self.central_widget.setGraphicsEffect(self.sh)

        self.title.setStyleSheet('font: 75 24pt "Consolas";color:white')
        self.title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.version.setStyleSheet('font-size:12px "Consolas";color:grey;margin:10px')
        self.owner.setStyleSheet('font-size:12px "Consolas";color:grey;margin:10px')
        self.version.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.owner.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
