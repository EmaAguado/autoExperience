from PySide2 import QtCore, QtGui, QtWidgets
from ui.widget import customWidgets
import os, encrypt
from functools import partial

class Preferences(QtWidgets.QWidget):

    """
    Class to generate a preference menu. This class will be generated based on a QStackedWidget. 
    This is linked to a men-bar that will have access to the different sections of the preferences.
    """

    fill_color = QtGui.QColor(30, 30, 30, 230)
    pen_color = QtGui.QColor("#333333")

    settings = QtCore.QSettings(os.environ["APPDATA"]+"/dragonary_autoexperience/preferences.ini",QtCore.QSettings.IniFormat)


    def __init__(self,parent=None):
        super(Preferences, self).__init__(parent)
        self.parent = parent
        self.save = False

        self.createWidgets()
        self.createLayout()
        self.createConnections()

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum))

    def createWidgets(self):
        
        self.main_layout            = QtWidgets.QGridLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.central_layout         = QtWidgets.QGridLayout()
        self.central_layout.setContentsMargins(0,0,0,0)
        self.central_layout.setSpacing(0)
        self.close_layout           = QtWidgets.QHBoxLayout()
        
        self.b_close                = customWidgets.AnimPushButton(text="Cancel",size=(290,30))
        self.b_close.setAnimation(150,QtGui.QColor(15,15,15,0).name(),QtGui.QPalette().color(QtGui.QPalette.Highlight).name())
        self.toolbar                = QtWidgets.QFrame()
        self.toolbar.setMaximumWidth(100)
        self.toolbar_layout         = QtWidgets.QVBoxLayout(self.toolbar)
        self.toolbar_layout.setContentsMargins(0,0,0,0)
        self.toolbar_buttons_layout = QtWidgets.QVBoxLayout()
        self.stacked                = QtWidgets.QStackedWidget()
        self.b_save                 = customWidgets.AnimPushButton(text="Save",size=(290,30))
        self.b_save.setAnimation(150,QtGui.QColor(15,15,15,0).name(),QtGui.QPalette().color(QtGui.QPalette.Highlight).name())

        self.log                    = QtWidgets.QFrame()
        self.log_layout             = QtWidgets.QHBoxLayout(self.log)
        self.log_label              = QtWidgets.QLabel("")

        self.stacked.setStyleSheet("QStackedWidget{background-color: palette(mid)}")
        # self.stacked.setMaximumSize(2000,640)
        self.toolbar.setStyleSheet("QFrame{background-color: palette(base)}")
        # self.b_close.setMaximumWidth(75)
        # self.b_save.setMaximumWidth(75)
        self.log.setMaximumHeight(100)
        self.log.setStyleSheet("QFrame{background-color: red}")
        self.log.hide()

        self.menu = dict()
        self.b_show = dict()

        self.widget_data = dict()

    def addMenu(self,name,form,adjust=True):
        """
        Parameters
        ----------
        name : str or list
            Title Menu preferences.
        param2 : :dict: `str`(title of the input), `obj`(input type)
            dictionary that generates the title input in a QLabel and the input widget.

        Example
        -------
        self.addMenu("Title",{"title input",QtWidgets.QLineEdit()})

        """

        self.menu[name] = QtWidgets.QScrollArea()
        self.menu[name].setWidgetResizable(True)
        self.menu[name].setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.central_widget = QtWidgets.QWidget()
        # self.central_widget.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred))
        self.menu_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.menu_layout)

        self.menu[name].setWidget(self.central_widget)


        for key in form.keys():
            real_key = key
            icon = False
            if "|" in key:
                key,icon = key.split(" | ")
            
            if form[real_key]:
                if icon:
                    icon_widget = QtWidgets.QLabel()
                    pixmap = QtGui.QPixmap(icon)
                    pixmap = pixmap.scaled(32, 32, QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation) 
                    icon_widget.setPixmap(pixmap)
                    frame = QtWidgets.QFrame()
                    frame.setObjectName("frame_preferences")
                    lay = QtWidgets.QHBoxLayout(frame)
                    lay.addWidget(icon_widget)
                    label = QtWidgets.QLabel(key + "   ")
                    label.adjustSize()
                    lay.addWidget(label)
                    lay.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
                    self.menu_layout.addWidget(frame)
                    frame.setStyleSheet("QFrame{border-top: 2px solid palette(mid)}QLabel{border:0px}")
                else:
                    label = QtWidgets.QLabel(key)
                    label.adjustSize()
                    self.menu_layout.addWidget(label)
                
                self.menu_layout.addWidget(form[real_key])
                self.widget_data[key] = form[real_key]
            else:
                title = QtWidgets.QLabel(key)
                title.setStyleSheet("font:75 12pt")
                self.menu_layout.addWidget(title)
                self.menu_layout.addWidget(QtWidgets.QLabel("_"*40))

        if adjust: self.menu_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        self.stacked.addWidget(self.menu[name])

        self.b_show[name] = customWidgets.AnimPushButton(text=name,size=(100,30),checked=True)
        self.b_show[name].setAnimation(150,QtGui.QPalette().color(QtGui.QPalette.Base).name(),QtGui.QPalette().color(QtGui.QPalette.Mid).name())
        self.b_show[name].setCheckable(True)
        self.b_show[name].clicked.connect(partial(self.onClicked, self.menu[name], name))

        self.toolbar_buttons_layout.addWidget(self.b_show[name])

    def onClicked(self, widget, button):
        """
        Uncheck all buttons except the clicked button.

        Parameters
        ----------
        widget : QtWidgets.QPushButton
            Widget button.
        param2 : button
            Button key in the menu variable

        """

        for key in self.b_show.keys():
            if key == button:
                self.b_show[key].setChecked(True)
            else:
                self.b_show[key].setChecked(False)

        self.stacked.setCurrentWidget(widget)

    def createLayout(self):

        self.toolbar_layout.addLayout(self.toolbar_buttons_layout)
        self.toolbar_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        #self.close_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.close_layout.addWidget(self.b_close)
        self.close_layout.addWidget(self.b_save)

        self.log_layout.addWidget(self.log_label)

        self.central_layout.addWidget(self.log,0,0,1,2)
        self.central_layout.addWidget(self.toolbar,1,0)
        self.central_layout.addWidget(self.stacked,1,1)
        self.central_layout.addLayout(self.close_layout,2,0,1,2)

        self.main_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),1,0)
        self.main_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),1,2)
        self.main_layout.addLayout(self.central_layout,1,1)
        # self.main_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding),0,1)
        # self.main_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding),2,1)

    def createConnections(self):

        self.b_close.clicked.connect(self.close)
        self.b_save.clicked.connect(self.onSaveClicked)

    def data(self):
        """
        Returns
        -------
        self._data = ``dict()``
    
            Dictionary with input values and widget key
    
                {
                    'widget_key1': str(input1),
                    'widget_key2': str(input2)
                }
        """
        self._data = dict()

        for key in self.widget_data.keys():

            if   isinstance(self.widget_data[key], QtWidgets.QLineEdit):
                self._data[key] = encrypt.encode(str(self.widget_data[key].text()),10)

            elif isinstance(self.widget_data[key], QtWidgets.QCheckBox):
                self._data[key] =  encrypt.encode(str(self.widget_data[key].isChecked()),10)

            elif isinstance(self.widget_data[key], QtWidgets.QComboBox):
                self._data[key] =  encrypt.encode(str(self.widget_data[key].currentText()),10)

            elif str(type(self.widget_data[key])) == "<class 'ui.main.ScheduleMainWidget'>":
                self._data[key] =  encrypt.encode(str(self.widget_data[key].returnData()),10)    

        return self._data

    def filter(self):
        """
        Returns
        -------
        bool
            True if successful, False otherwise.

            Support function. Its function is to generate filters that will be applied at the time of saving the inputs.

        :ToDo:
        ------
            Currently it is only possible to add filters by generating an instance of the class

        Example function
        ----------------
        
            if not os.path.exists(encrypt.decode(self._data["Path"],10)) and not encrypt.decode(self._data["Path"],10) == "":
    
                self.log_label.setText("Path not exists.")
                return False
    
            elif not len(encrypt.decode(self._data["User"],10)+encrypt.decode(self._data["Password"],10)) == 0:
                try:
                    if not cs.sg.authenticate_human_user(encrypt.decode(self._data["User"],10), encrypt.decode(self._data["Password"],10)):
                        self.log_label.setText("User or password is incorrect.")
                        return False
                except:
                    self.log_label.setText("User or password is incorrect.")
                    return False
    
            return True

        Note
        ----
        It is ``very important`` to remember that "self._data" has encrypted values. Use the function `encrypt.encode(value,int(10))`

        """
        return True

    def paintEvent(self, event):

        """
        Action on resize main window.

        """

        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(self.pen_color)
        qp.setBrush(self.fill_color)
        qp.drawRect(0, 0, self.parent.width(), self.parent.height())
        self.resize(self.parent.width(), self.parent.height())
        qp.end()

    def onSaveClicked(self):
        """
        Save data.
        """
        self._data = self.data()


        if not self.filter():
            self.log.show()

        else:
            self.log.hide()

            self.settings.setValue('preferences',self._data)
            self.save = True
            self.parent.readSettings()
            self.close()
    
    def readData(self):
        """
        Read data.
        """
        data = self.settings.value('preferences')

        if data:
            
            for key in data.keys():
                if key in self.widget_data.keys():
                    if   isinstance(self.widget_data[key], QtWidgets.QLineEdit):

                        self.widget_data[key].setText(encrypt.decode(data[key],10))
            
                    elif isinstance(self.widget_data[key], QtWidgets.QCheckBox):

                        if encrypt.decode(data[key],10) == "True":
                            self.widget_data[key].setChecked(True)
                        else: 
                            self.widget_data[key].setChecked(False)
            
                    elif isinstance(self.widget_data[key], QtWidgets.QComboBox):

                        self.widget_data[key].setCurrentIndex(self.widget_data[key].findText(encrypt.decode(data[key],10), QtCore.Qt.MatchFixedString))

                    elif str(type(self.widget_data[key])) == "<class 'ui.main.ScheduleMainWidget'>":

                        self.widget_data[key].setData(eval(encrypt.decode(data[key],10).replace("PySide2.","")))
