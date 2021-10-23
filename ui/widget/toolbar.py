from PySide2 import QtCore, QtGui, QtWidgets
from ui.widget import customWidgets

class UI(QtWidgets.QFrame):

    def __init__(self,parent=None):

        super(UI, self).__init__()
        self.setObjectName("toolbar")
        self.parent = parent
        self.createWidgets()
        self.createLayout()
        self.createStyle()
        self.createConnections()
        self.raise_()

    def createWidgets(self):

        self.central_layout   = QtWidgets.QVBoxLayout(self)

        self.inbox            = customWidgets.PushButtonToolTip(icon="ui/resources/img/play.png",size=[32,32],tooltip="PLAY",align="right",parent=self.parent)
        # self.browser          = customWidgets.PushButtonToolTip(icon="ui/resources/img/browser.png",size=[32,32],tooltip="SEARCH",align="right",parent=self.parent)
        # self.task_view        = customWidgets.PushButtonToolTip(icon="ui/resources/img/taskView.png",size=[32,32],tooltip="TASK VIEW",align="right",parent=self.parent)
        # self.assets           = customWidgets.PushButtonToolTip(icon="ui/resources/img/assets.png",size=[32,32],tooltip="ASSETS",align="right",parent=self.parent)
        # self.download_monitor = customWidgets.PushButtonToolTip(icon="ui/resources/img/download.png",size=[32,32],tooltip="DOWNLOAD MONITOR",align="right",parent=self.parent)

        self.separator = QtWidgets.QLabel("....")
        self.separator.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)

        # self.project_editor = customWidgets.PushButtonToolTip(icon="ui/resources/img/projectEditor.png",tooltip="PROJECT EDITOR",align="right",parent=self.parent)
        # self.task_editor    = customWidgets.PushButtonToolTip(icon="ui/resources/img/taskEditor.png",tooltip="TASK EDITOR",align="right",parent=self.parent)

        self.separator2 = QtWidgets.QLabel("....")
        self.separator2.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)

        # self.explorer = customWidgets.PushButtonToolTip(icon="ui/resources/img/explorer.png",tooltip="EXPLORER",align="right",parent=self.parent)

        self.spacer = QtWidgets.QFrame()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.spacer.setFocusPolicy(QtCore.Qt.NoFocus)

        # self.preferences = customWidgets.PushButtonToolTip(icon="ui/resources/img/preferences.png",tooltip="PREFERENCES",align="right",parent=self.parent)

    def createLayout(self):

        self.central_layout.addWidget(self.inbox)
        # self.central_layout.addWidget(self.browser)
        # self.central_layout.addWidget(self.task_view)
        # self.central_layout.addWidget(self.assets)
        # self.central_layout.addWidget(self.download_monitor)

        # self.central_layout.addWidget(self.separator)

        # self.central_layout.addWidget(self.explorer)

        # self.central_layout.addWidget(self.spacer)

        # self.central_layout.addWidget(self.project_editor)
        # self.central_layout.addWidget(self.task_editor)
        # self.central_layout.addWidget(self.preferences)

    def createStyle(self):

        self.setStyleSheet( "#toolbar{padding:8px;background-color: palette(mid);border-right:2px solid rgb(30,30,30)}"\
                            "QFrame{background-color:palette(mid);padding:5px}"\
                            "QPushButton{background-color:transparent;padding:5px}"\
                            "QPushButton:hover{background-color:palette(light);padding:5px}"\
                            "QPushButton:pressed{background-color:palette(highlight);padding:5px}"\
                            "QToolButton{background-color:transparent;padding:5px}"\
                            "QToolButton:hover{background-color:palette(light);padding:5px}"\
                            "QToolButton:pressed{background-color:palette(highlight);padding:5px}")

        self.setMinimumWidth(50)
        self.setMaximumWidth(50)
        
        self.central_layout.setContentsMargins(0,0,0,0)
        self.central_layout.setSpacing(2)

        # self.sh = QtWidgets.QGraphicsDropShadowEffect(self)
        # self.sh.setColor(QtGui.QColor(0,0,0,100))
        # self.sh.setBlurRadius(10)
        # self.sh.setXOffset(1)
        # self.sh.setYOffset(1)
        # self.setGraphicsEffect(self.sh)

        # self.inbox.setMenu(QtWidgets.QMenu("Sub menu", parent=self))
        # self.inbox.setStyleSheet(  "QToolButton::menu-indicator {image: url(ui/resources/img/on_titan.png)}")


    def createConnections(self):

        pass
        # self.inbox.clicked.connect(self.parent.openInbox)
        # self.task_view.clicked.connect(self.parent.openTaskView)
        # self.browser.clicked.connect(self.parent.addBrowser)
        # self.assets.clicked.connect(lambda:self.parent.addAssetsView(self.parent.AssetViewCode))
        # self.download_monitor.clicked.connect(self.parent.addDownloadMonitor)
        # self.explorer.clicked.connect(lambda:self.parent.addExplorer(self.parent.ExplorerCode))
        # self.project_editor.clicked.connect(self.parent.addProjectEditor)
        # self.task_editor.clicked.connect(self.parent.addTaskEditor)
        # self.preferences.clicked.connect(self.parent.openPreferences)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    ui = UI()
    ui.show()

    sys.exit(app.exec_())