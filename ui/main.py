import pprint
from PySide2 import QtCore, QtGui, QtWidgets, QtCharts
from functools import partial
from ui.palette import styleS, stylesheet
from ui.widget import mainWindow, customWidgets, loading, shell, stackedWidget
from ui import preferences
import mutils

import time
import requests
import json
import os
import datetime
import threading
import subprocess
import encrypt
import hashlib

created_at     = str(datetime.datetime.now(datetime.timezone.utc).strftime("%y-%m-%d_%H-%M-%S"))
local_log_path = os.environ["APPDATA"]+"/dragonary_autoexperience/logs/{}_log.txt".format(created_at)

############
############
##   UI   ##
############
############

import pygetwindow
import time
import os
import pyautogui
import PIL
import cv2
import numpy as np
import easyocr
import matplotlib.pyplot as plt


def getEmber():

    try:
        image_screenshot = './screenshots/screen.jpg'
        image_screenshot_dragonary = './screenshots/dragonary.jpg'

        # get screensize
        my = pygetwindow.getWindowsWithTitle('Dragonary')[0]
        save_x = my.topleft.x
        save_y = my.topleft.y

        my.activate()
        time.sleep(3)

        # save screenshot
        p = pyautogui.screenshot()
        p.save(image_screenshot)

        # # edit screenshot
        im = PIL.Image.open(image_screenshot)

        left   = save_x
        top    = save_y
        right  = left + my.width
        bottom = top + my.height

        im_crop = im.crop((left,top,right,bottom))
        im_crop.save(image_screenshot_dragonary, quality=100)

        reader = easyocr.Reader(['en','es'])
        result = reader.readtext(image_screenshot_dragonary)

        for x in result:
            print(x)
          # if "/" in x[1]:
          #   try:
          #       return int(x[1].split("/")[0])
          #   except:
          #       return 0

    except Exception as e:
        print(e)
        return 0
    
def thread(function):
        
    def wrapper(*args,**kwargs):

        print("[THREAD] Starting...")
        worker = threading.Thread(target=function,args=args,kwargs=kwargs)
        worker.start()

        return kwargs

    return wrapper

class PanelPreferences(preferences.Preferences):


    def __init__(self,parent=None):
        super(PanelPreferences, self).__init__(parent)

        self.parent = parent

        input_name = QtWidgets.QLineEdit()
        input_name.setPlaceholderText("Insert name")

        input_token = QtWidgets.QLineEdit()
        input_token.setPlaceholderText("Insert token")

        input_executable = QtWidgets.QLineEdit()
        input_executable.setPlaceholderText("Insert path dragonary.exe")

        input_email = QtWidgets.QLineEdit()
        input_email.setPlaceholderText("Insert email")




        self.addMenu("PREFERENCES",{    "CREDENTIALS":None,
                                        "NAME"        :input_name,
                                        "TOKEN"       :input_token,
                                        "EXECUTABLE"  :input_executable,
                                        "NOTIFICATION":None,
                                        "EMAIL"       :input_email})


    def filter(self):

        name        = encrypt.decode(self._data["NAME"],10)
        hash_object = hashlib.sha256(name.encode())
        hex_dig     = hash_object.hexdigest()
        token       = encrypt.encode(hex_dig,10)
        print(token)

        if not os.path.exists(encrypt.decode(self._data["EXECUTABLE"],10)):
            if not encrypt.decode(self._data["EXECUTABLE"],10) == "":
                self.log_label.setText("Executable not found.")
                return False
        if not encrypt.decode(self._data["TOKEN"],10) == token and name != "":
            self.log_label.setText("Invalid credentials.")
            return False

        self.log_label.setText("")
        return True

    def closeEvent(self,event):

        super(PanelPreferences, self).closeEvent(event)

class ActionWidgetSchedule(QtWidgets.QFrame):

    def __init__(self,list_actions,item,data=None):

        super(ActionWidgetSchedule, self).__init__()    

        self.starting = True
        self.item = item

        if data:
            self.data = data
        else:
            self.data = {"type":"schedule","priority":99999,"time":"00:00","state":True}

        self.list_actions = list_actions
        self.createWidgets()
        if data: self.setData()
        self.starting = False

    def createWidgets(self): 

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)

        self.move_button  = QtWidgets.QLabel()
        self.move_button.setPixmap("./ui/resources/img/drop.png")
        self.move_button.setScaledContents(True)
        self.move_button.setStyleSheet("QLabel{background-color:palette(highlight);border-top-left-radius:8px;border-bottom-left-radius:8px}QLabel:hover{background-color:palette(dark);border:none;padding:5px}")
        self.move_button.setMinimumWidth(30)
        self.move_button.setMaximumWidth(30)
        self.move_button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred))

        self.main_layout.addWidget(self.move_button)

        self.main_layout.addWidget(QtWidgets.QLabel("       SCHEDULE"))

        self.central_layout = QtWidgets.QVBoxLayout()
        self.central_layout.setSpacing(0)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addLayout(self.central_layout)

        self.time_edit = QtWidgets.QTimeEdit()
        self.desactive_button = customWidgets.ButtonIcon(icon="./ui/resources/img/visible.png",size=[24,24],checked_color=[42, 130, 218,255])
        self.desactive_button.setCheckable(True)
        self.desactive_button.setChecked(True)
        self.desactive_button.clicked.connect(self.onActive)
        self.delete_button    = customWidgets.ButtonIcon(icon="./ui/resources/img/close.png",size=[24,24])
        self.delete_button.clicked.connect(self.onClose)

        self.main_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.main_layout.addWidget(QtWidgets.QLabel("   Time: "))
        self.main_layout.addWidget(self.time_edit)
        self.main_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.main_layout.addWidget(self.desactive_button)
        self.main_layout.addWidget(self.delete_button)
        self.time_edit.timeChanged.connect(self.changeData)

    def changeData(self):

        if not self.starting:
            self.data = {"type":"schedule","priority":self.list_actions.row(self.item),"time":self.time_edit.time().toString()[:-3],"state":self.desactive_button.isChecked()}

            self.list_actions.saveChanges()

    def onActive(self,state):

        self.changeData()
        
        if state:
            self.move_button.setStyleSheet("QLabel{background-color:palette(highlight);border-top-left-radius:8px;border-bottom-left-radius:8px}QLabel:hover{background-color:palette(dark);border:none;padding:5px}")
            self.time_edit.setEnabled(True)
        else:
            self.time_edit.setEnabled(False)
            self.move_button.setStyleSheet("QLabel{background-color:palette(alternate-base);border-top-left-radius:8px;border-bottom-left-radius:8px}QLabel:hover{background-color:palette(dark);border:none;padding:5px}")

    def onClose(self):

        self.list_actions.takeItem(self.list_actions.row(self.item))

    def returnData(self):

        return self.data

    def setData(self):

        self.time_edit.setTime(QtCore.QTime(int(self.data["time"].split(":")[0]),int(self.data["time"].split(":")[1]), 0))
        self.desactive_button.setChecked(self.data["state"])
        self.onActive(self.data["state"])

class ActionWidgetLoop(QtWidgets.QFrame):

    def __init__(self,list_actions,item,data=None):

        super(ActionWidgetLoop, self).__init__()    

        self.starting = True
        self.item = item

        if data:
            self.data = data
        else:
            self.data = {"type":"loop","priority":99999,"state":True}

        self.list_actions = list_actions
        self.createWidgets()
        if data: self.setData()
        self.starting = False

    def createWidgets(self): 

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)

        self.move_button  = QtWidgets.QLabel()
        self.move_button.setPixmap("./ui/resources/img/drop.png")
        self.move_button.setScaledContents(True)
        self.move_button.setStyleSheet("QLabel{background-color:palette(highlight);border-top-left-radius:8px;border-bottom-left-radius:8px}QLabel:hover{background-color:palette(dark);border:none;padding:5px}")
        self.move_button.setMinimumWidth(30)
        self.move_button.setMaximumWidth(30)
        self.move_button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred))

        self.main_layout.addWidget(self.move_button)

        self.main_layout.addWidget(QtWidgets.QLabel("       LOOP"))

        self.central_layout = QtWidgets.QVBoxLayout()
        self.central_layout.setSpacing(0)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addLayout(self.central_layout)


        self.desactive_button = customWidgets.ButtonIcon(icon="./ui/resources/img/visible.png",size=[24,24],checked_color=[42, 130, 218,255])
        self.desactive_button.setCheckable(True)
        self.desactive_button.setChecked(True)
        self.desactive_button.clicked.connect(self.onActive)
        self.delete_button    = customWidgets.ButtonIcon(icon="./ui/resources/img/close.png",size=[24,24])
        self.delete_button.clicked.connect(self.onClose)

        self.main_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.main_layout.addWidget(QtWidgets.QLabel("   LOOP "))
        self.main_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.main_layout.addWidget(self.desactive_button)
        self.main_layout.addWidget(self.delete_button)

    def changeData(self):

        if not self.starting:
            self.data = {"type":"loop","priority":self.list_actions.row(self.item),"state":self.desactive_button.isChecked()}

            self.list_actions.saveChanges()

    def onActive(self,state):

        self.changeData()
        
        if state:
            self.move_button.setStyleSheet("QLabel{background-color:palette(highlight);border-top-left-radius:8px;border-bottom-left-radius:8px}QLabel:hover{background-color:palette(dark);border:none;padding:5px}")
        else:
            self.move_button.setStyleSheet("QLabel{background-color:palette(alternate-base);border-top-left-radius:8px;border-bottom-left-radius:8px}QLabel:hover{background-color:palette(dark);border:none;padding:5px}")

    def onClose(self):

        self.list_actions.takeItem(self.list_actions.row(self.item))

    def returnData(self):

        return self.data

    def setData(self):

        self.desactive_button.setChecked(self.data["state"])
        self.onActive(self.data["state"])

class ActionWidgetEnergy(QtWidgets.QFrame):

    def __init__(self,list_actions,item,data=None):

        super(ActionWidgetEnergy, self).__init__()    

        self.starting = True
        self.item = item

        if data:
            self.data = data
        else:
            self.data = {"type":"energy","priority":99999,"load_energy":10,"state":True}

        self.list_actions = list_actions
        self.createWidgets()
        if data: self.setData()
        self.starting = False

    def createWidgets(self): 

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)

        self.move_button  = QtWidgets.QLabel()
        self.move_button.setPixmap("./ui/resources/img/drop.png")
        self.move_button.setScaledContents(True)
        self.move_button.setStyleSheet("QLabel{background-color:palette(highlight);border-top-left-radius:8px;border-bottom-left-radius:8px}QLabel:hover{background-color:palette(dark);border:none;padding:5px}")
        self.move_button.setMinimumWidth(30)
        self.move_button.setMaximumWidth(30)
        self.move_button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred))

        self.main_layout.addWidget(self.move_button)

        self.main_layout.addWidget(QtWidgets.QLabel("       ENERGY"))

        self.central_layout = QtWidgets.QVBoxLayout()
        self.central_layout.setSpacing(0)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addLayout(self.central_layout)

        self.load_energy = QtWidgets.QSpinBox()
        self.load_energy.setRange (10, 80)
        self.load_energy.valueChanged.connect(self.changeData)


        self.desactive_button = customWidgets.ButtonIcon(icon="./ui/resources/img/visible.png",size=[24,24],checked_color=[42, 130, 218,255])
        self.desactive_button.setCheckable(True)
        self.desactive_button.setChecked(True)
        self.desactive_button.clicked.connect(self.onActive)
        self.delete_button    = customWidgets.ButtonIcon(icon="./ui/resources/img/close.png",size=[24,24])
        self.delete_button.clicked.connect(self.onClose)

        self.main_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.main_layout.addWidget(QtWidgets.QLabel("   Wait load energy: "))
        self.main_layout.addWidget(self.load_energy)
        self.main_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.main_layout.addWidget(self.desactive_button)
        self.main_layout.addWidget(self.delete_button)

    def changeData(self):

        if not self.starting:
            self.data = {"type":"energy","priority":self.list_actions.row(self.item),"load_energy":self.load_energy.value(),"state":self.desactive_button.isChecked()}

            self.list_actions.saveChanges()

    def onActive(self,state):

        self.changeData()
        
        if state:
            self.move_button.setStyleSheet("QLabel{background-color:palette(highlight);border-top-left-radius:8px;border-bottom-left-radius:8px}QLabel:hover{background-color:palette(dark);border:none;padding:5px}")
            self.load_energy.setEnabled(True)

        else:
            self.load_energy.setEnabled(False)
            self.move_button.setStyleSheet("QLabel{background-color:palette(alternate-base);border-top-left-radius:8px;border-bottom-left-radius:8px}QLabel:hover{background-color:palette(dark);border:none;padding:5px}")

    def onClose(self):

        self.list_actions.takeItem(self.list_actions.row(self.item))

    def returnData(self):

        return self.data

    def setData(self):

        self.load_energy.setValue(int(self.data["load_energy"]))
        self.desactive_button.setChecked(self.data["state"])
        self.onActive(self.data["state"])

class ActionWidgetEmber(QtWidgets.QFrame):

    def __init__(self,list_actions,item,data=None):

        super(ActionWidgetEmber, self).__init__()    

        self.starting = True
        self.item = item
        if data:
            self.data = data
        else:
            self.data = {"type":"ember","priority":99999,"ember_type":"aire","ember_dificulty":"facil","start_energy":10,"stop_energy":0,"state":True}
        self.list_actions = list_actions
        self.createWidgets()
        if data: self.setData()
        self.starting = False

    def createWidgets(self): 

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)

        self.move_button  = QtWidgets.QLabel()
        self.move_button.setPixmap("./ui/resources/img/drop.png")
        self.move_button.setScaledContents(True)
        self.move_button.setStyleSheet("QLabel{background-color:palette(highlight);border-top-left-radius:8px;border-bottom-left-radius:8px}QLabel:hover{background-color:palette(dark);border:none;padding:5px}")
        self.move_button.setMinimumWidth(30)
        self.move_button.setMaximumWidth(30)
        self.move_button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred))

        self.main_layout.addWidget(self.move_button)

        self.main_layout.addWidget(QtWidgets.QLabel("       EMBERS"))

        self.central_layout = QtWidgets.QVBoxLayout()
        self.central_layout.setSpacing(0)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addLayout(self.central_layout)

        self.start_energy = QtWidgets.QSpinBox()
        self.stop_energy = QtWidgets.QSpinBox()
        self.ember_type = QtWidgets.QComboBox()
        self.ember_type.addItems(["aire","fuego","agua","tierra","trueno","planta","hielo"])

        self.ember_dificulty = QtWidgets.QComboBox()
        self.ember_dificulty.addItems(["facil","medio"])

        self.start_energy.valueChanged.connect(self.changeData)
        self.stop_energy.valueChanged.connect(self.changeData)
        self.ember_type.currentTextChanged.connect(self.changeData)
        self.ember_dificulty.currentTextChanged.connect(self.changeData)
        self.start_energy.setRange (10, 80)
        self.stop_energy.setRange (9, 70)

        self.desactive_button = customWidgets.ButtonIcon(icon="./ui/resources/img/visible.png",size=[24,24],checked_color=[42, 130, 218,255])
        self.desactive_button.setCheckable(True)
        self.desactive_button.setChecked(True)
        self.desactive_button.clicked.connect(self.onActive)
        self.delete_button    = customWidgets.ButtonIcon(icon="./ui/resources/img/close.png",size=[24,24])
        self.delete_button.clicked.connect(self.onClose)

        self.main_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.main_layout.addWidget(QtWidgets.QLabel("Ember type: "))
        self.main_layout.addWidget(self.ember_type)
        self.main_layout.addWidget(QtWidgets.QLabel("Ember dificulty: "))
        self.main_layout.addWidget(self.ember_dificulty)
        self.main_layout.addWidget(QtWidgets.QLabel("   Start energy higher: "))
        self.main_layout.addWidget(self.start_energy)
        self.main_layout.addWidget(QtWidgets.QLabel("   Stop energy less: "))
        self.main_layout.addWidget(self.stop_energy)
        self.main_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.main_layout.addWidget(self.desactive_button)
        self.main_layout.addWidget(self.delete_button)

    def changeData(self):

        if not self.starting:
            self.data = {"type":"ember","priority":self.list_actions.row(self.item),"ember_type":self.ember_type.currentText(),"ember_dificulty":self.ember_dificulty.currentText(),"start_energy":self.start_energy.value(),"stop_energy":self.stop_energy.value(),"state":self.desactive_button.isChecked()}

            self.list_actions.saveChanges()

    def onActive(self,state):

        self.changeData()
        
        if state:
            self.ember_type.setEnabled(True)
            self.ember_dificulty.setEnabled(True)
            self.move_button.setStyleSheet("QLabel{background-color:palette(highlight);border-top-left-radius:8px;border-bottom-left-radius:8px}QLabel:hover{background-color:palette(dark);border:none;padding:5px}")
            self.start_energy.setEnabled(True)
            self.stop_energy.setEnabled(True)

        else:
            self.start_energy.setEnabled(False)
            self.stop_energy.setEnabled(False)
            self.ember_type.setEnabled(False)
            self.ember_dificulty.setEnabled(False)
            self.move_button.setStyleSheet("QLabel{background-color:palette(alternate-base);border-top-left-radius:8px;border-bottom-left-radius:8px}QLabel:hover{background-color:palette(dark);border:none;padding:5px}")

    def onClose(self):

        self.list_actions.takeItem(self.list_actions.row(self.item))

    def returnData(self):

        return self.data

    def setData(self):
        self.ember_type.setCurrentText(self.data["ember_type"])
        self.ember_dificulty.setCurrentText(self.data["ember_dificulty"])
        self.start_energy.setValue(int(self.data["start_energy"]))
        self.start_energy.setValue(int(self.data["stop_energy"]))
        self.desactive_button.setChecked(self.data["state"])

        self.onActive(self.data["state"])

class ActionWidgetMision(QtWidgets.QFrame):

    def __init__(self,list_actions,item,data=None):

        super(ActionWidgetMision, self).__init__()    

        self.item = item

        self.starting = True
        if data:
            self.data = data
        else:
            self.data = {"type":"mision","priority":99999,"mission":1,"repetition":0,"loop":False,"state":True}
        self.list_actions = list_actions
        self.createWidgets()
        if data: self.setData()
        self.starting = False

    def createWidgets(self): 

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)

        self.move_button  = QtWidgets.QLabel()
        self.move_button.setPixmap("./ui/resources/img/drop.png")
        self.move_button.setScaledContents(True)
        self.move_button.setStyleSheet("QLabel{background-color:palette(highlight);border-top-left-radius:8px;border-bottom-left-radius:8px}QLabel:hover{background-color:palette(dark);border:none;padding:5px}")
        self.move_button.setMinimumWidth(30)
        self.move_button.setMaximumWidth(30)
        self.move_button.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred))

        self.main_layout.addWidget(self.move_button)

        self.main_layout.addWidget(QtWidgets.QLabel("       MISION"))

        self.central_layout = QtWidgets.QVBoxLayout()
        self.central_layout.setSpacing(0)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.main_layout.addLayout(self.central_layout)

        self.repetition = QtWidgets.QSpinBox()
        self.repetition_loop_switch = customWidgets.SwitchAnimate(text="Loop",active_color="#ccba2f")
        self.mission_number = QtWidgets.QSpinBox()
        self.mission_number.setRange (5, 12)


        self.repetition.valueChanged.connect(self.changeData)
        self.mission_number.valueChanged.connect(self.changeData)
        self.repetition_loop_switch.clicked.connect(self.changeData)

        self.desactive_button = customWidgets.ButtonIcon(icon="./ui/resources/img/visible.png",size=[24,24],checked_color=[42, 130, 218,255])
        self.desactive_button.setCheckable(True)
        self.desactive_button.setChecked(True)
        self.desactive_button.clicked.connect(self.onActive)
        self.delete_button    = customWidgets.ButtonIcon(icon="./ui/resources/img/close.png",size=[24,24])
        self.delete_button.clicked.connect(self.onClose)

        self.main_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        self.main_layout.addWidget(QtWidgets.QLabel("Mission: "))
        self.main_layout.addWidget(self.mission_number)
        self.main_layout.addWidget(QtWidgets.QLabel("           Repetitions: "))
        self.main_layout.addWidget(self.repetition)
        self.main_layout.addWidget(QtWidgets.QLabel("           Infinite loop: "))
        self.main_layout.addWidget(self.repetition_loop_switch)
        self.main_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.main_layout.addWidget(self.desactive_button)
        self.main_layout.addWidget(self.delete_button)

    def changeData(self):

        if not self.starting:
            if self.repetition_loop_switch.isChecked():
                self.repetition.setEnabled(False)
            else:
                self.repetition.setEnabled(True)

            self.data = {"type":"mision","priority":self.list_actions.row(self.item),"mission":self.mission_number.value(),"repetition":self.repetition.value(),"loop":self.repetition_loop_switch.isChecked(),"state":self.desactive_button.isChecked()}

            self.list_actions.saveChanges()

    def onActive(self,state):

        self.changeData()
        
        if state:
            if self.repetition_loop_switch.isChecked():
                self.repetition.setEnabled(False)
            else:
                self.repetition.setEnabled(True)
            self.mission_number.setEnabled(True)
            self.repetition_loop_switch.setEnabled(True)
            self.move_button.setStyleSheet("QLabel{background-color:palette(highlight);border-top-left-radius:8px;border-bottom-left-radius:8px}QLabel:hover{background-color:palette(dark);border:none;padding:5px}")
        else:
            self.repetition.setEnabled(False)
            self.repetition_loop_switch.setEnabled(False)
            self.mission_number.setEnabled(False)
            self.move_button.setStyleSheet("QLabel{background-color:palette(alternate-base);border-top-left-radius:8px;border-bottom-left-radius:8px}QLabel:hover{background-color:palette(dark);border:none;padding:5px}")

    def onClose(self):

        self.list_actions.takeItem(self.list_actions.row(self.item))

    def returnData(self):

        return self.data

    def setData(self):

        self.mission_number.setValue(int(self.data["mission"]))
        self.repetition.setValue(int(self.data["repetition"]))
        self.repetition_loop_switch.setChecked(self.data["loop"])
        self.desactive_button.setChecked(self.data["state"])

        self.onActive(self.data["state"])

class ListActions(QtWidgets.QListWidget):

    onAddActionWidget = QtCore.Signal(str,dict)

    def __init__(self):

        super(ListActions, self).__init__()
        self.setDragDropMode(self.InternalMove)
        self.createStyle()
        self.onAddActionWidget.connect(self.addActionWidget)

    def addActionWidget(self,type_action,data=None):

        item = QtWidgets.QListWidgetItem()

        if type_action == "mision":
            widget = ActionWidgetMision(self,item,data)
        elif type_action == "ember":
            widget = ActionWidgetEmber(self,item,data)
        elif type_action == "energy":
            widget = ActionWidgetEnergy(self,item,data)
        elif type_action == "loop":
            widget = ActionWidgetLoop(self,item,data)
        elif type_action == "schedule":
            widget = ActionWidgetSchedule(self,item,data)

        item.setSizeHint(QtCore.QSize(60,60))
        item.setTextAlignment (QtCore.Qt.AlignCenter)
        item.setData(3,widget)
        self.addItem(item)
        self.setItemWidget(item,widget)


    def createStyle(self):

        self.setStyleSheet( "QListWidget{background-color:palette(mid);border:none}"\
                            "QListWidget::item{background:palette(mid);border: 2px solid palette(alternate-base);border-radius:10px}"\
                            "QListWidget::item:hover{background:palette(alternate-base);border: 2px solid palette(alternate-base);border-radius:10px}")
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def leaveEvent(self, event):

        event.accept()

        try:self.itemWidget(self.selectedItems()[0]).changeData()
        except: pass

    def returnData(self,all=False):

        data = []
        for i in range(self.count()):
            item_data = self.itemWidget(self.item(i)).returnData()
            if item_data["state"] or all:
                data.append(item_data)

        data.sort(key = lambda x: x["priority"])

        return data

    def saveChanges(self):

        mutils.jsonDump(os.environ["APPDATA"]+"/dragonary_autoexperience/config.json",self.returnData(True))

class ActionsWidget(QtWidgets.QFrame):

    def __init__(self):

        super(ActionsWidget, self).__init__()

        self.createWidgets()
        self.createLayout()
        self.createStyle()
        self.createConnections()

    def createWidgets(self):

        self.toolbar         = QtWidgets.QFrame()
        self.toolbar_layout  = QtWidgets.QHBoxLayout(self.toolbar)
        self.list_action     = ListActions()

        self.layout = QtWidgets.QVBoxLayout(self)

        # self.button_mission = QtWidgets.QPushButton("+ Mission")
        self.button_mission = customWidgets.AnimPushButton(text="+ Mission",size=(290,30))
        self.button_mission.setAnimation(150,QtGui.QColor(15,15,15,0).name(),QtGui.QPalette().color(QtGui.QPalette.Highlight).name())

        self.button_schedule = customWidgets.AnimPushButton(text="+ Schedule",size=(290,30))
        self.button_schedule.setAnimation(150,QtGui.QColor(15,15,15,0).name(),QtGui.QPalette().color(QtGui.QPalette.Highlight).name())
        # self.button_embers  = QtWidgets.QPushButton("+ Embers")
        self.button_embers = customWidgets.AnimPushButton(text="+ Embers",size=(290,30))
        self.button_embers.setAnimation(150,QtGui.QColor(15,15,15,0).name(),QtGui.QPalette().color(QtGui.QPalette.Highlight).name())
        # self.button_energy  = QtWidgets.QPushButton("+ Load Energy")
        self.button_energy = customWidgets.AnimPushButton(text="+ Load Energy",size=(290,30))
        self.button_energy.setAnimation(150,QtGui.QColor(15,15,15,0).name(),QtGui.QPalette().color(QtGui.QPalette.Highlight).name())
        # self.button_loop    = QtWidgets.QPushButton("+ Loop")
        self.button_loop = customWidgets.AnimPushButton(text="+ Loop",size=(290,30))
        self.button_loop.setAnimation(150,QtGui.QColor(15,15,15,0).name(),QtGui.QPalette().color(QtGui.QPalette.Highlight).name())

    def createLayout(self):

        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.list_action)

        self.toolbar_layout.addWidget(self.button_mission)
        self.toolbar_layout.addWidget(self.button_schedule)
        self.toolbar_layout.addWidget(self.button_embers)
        self.toolbar_layout.addWidget(self.button_energy)
        self.toolbar_layout.addWidget(self.button_loop)

    def createConnections(self):

        self.button_mission.clicked.connect(lambda:self.list_action.addActionWidget("mision"))
        self.button_schedule.clicked.connect(lambda:self.list_action.addActionWidget("schedule"))
        self.button_embers.clicked.connect(lambda:self.list_action.addActionWidget("ember"))
        self.button_energy.clicked.connect(lambda:self.list_action.addActionWidget("energy"))
        self.button_loop.clicked.connect(lambda:self.list_action.addActionWidget("loop"))

    def createStyle(self):

        self.setStyleSheet( "#ActionsWidget{background-color:palette(mid);border:none}")
        # self.toolbar.setStyleSheet("QFrame{background-color:palette(highlight)}")
        self.layout.setSpacing(0)
        self.toolbar_layout.setContentsMargins(0,0,0,0)
        self.toolbar_layout.setSpacing(0)
        self.button_mission.setMinimumWidth(20)
        self.button_schedule.setMinimumWidth(20)
        self.button_embers.setMinimumWidth(20)
        self.button_energy.setMinimumWidth(20)
        self.button_loop.setMinimumWidth(20)

class CentralWidget(QtWidgets.QFrame):

    def __init__(self, main=None):

        super(CentralWidget, self).__init__()

        self.main            = main
        self.shell_widget    = shell.ShellWidget(local_log_path,local_log_path,parent=self.main)
        self.list_action     = ActionsWidget()
        self.stacked         = stackedWidget.SlidingStackedWidget()
        self.stacked_position = 0

        self.stacked.addWidget(self.shell_widget)
        self.stacked.addWidget(self.list_action)

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(self.stacked)
        self.layout.setSpacing(0)

class AUTOEXPERIENCE():

    stop = True

    def __init__(self,executable = None, user_name = None, is_get_experience = True, parent = None):

        self.parent = parent


        self.button_dict_mision = dict()
        self.button_dict_mision["misiones_button"]   = "./screenshots/misiones.PNG"
        self.button_dict_mision["story_button"]      = "./screenshots/story.PNG"
        self.button_dict_mision["mision_5_button"] = "./screenshots/mission_5.PNG"
        self.button_dict_mision["mision_6_button"] = "./screenshots/mission_6.PNG"
        self.button_dict_mision["mision_7_button"] = "./screenshots/mission_7.PNG"
        # self.button_dict_mision["mision_8_button"] = "./screenshots/mission_8.PNG"
        self.button_dict_mision["mision_12_button"] = "./screenshots/mission_12.PNG"
        self.button_dict_mision["jugar_button"]      = "./screenshots/jugar.PNG"
        self.button_dict_mision["iniciar_button"]    = "./screenshots/iniciar.PNG"
        self.button_dict_mision["manual_button"]     = "./screenshots/manual.PNG"
        self.button_dict_mision["x1_button"]         = "./screenshots/x1velocidad.PNG"
        self.button_dict_mision["reclamar_button"]   = "./screenshots/reclamar.PNG"
        self.button_dict_mision["continuar_button"]  = "./screenshots/continuar.PNG"
        self.button_dict_mision["salir_button"]      = "./screenshots/salir.PNG"

        self.button_dict_ember = dict()
        self.button_dict_ember["misiones_button"]   = "./screenshots/misiones.PNG"
        self.button_dict_ember["embers_button"]     = "./screenshots/embers.PNG"
        self.button_dict_ember["dificulty_facil"]     = "./screenshots/dificulty_facil.PNG"
        self.button_dict_ember["dificulty_medio"]     = "./screenshots/dificulty_medio.PNG"
        self.button_dict_ember["type_trueno"]       = "./screenshots/ember_trueno.PNG"
        self.button_dict_ember["type_agua"]         = "./screenshots/ember_agua.PNG"
        self.button_dict_ember["type_aire"]         = "./screenshots/ember_aire.PNG"
        self.button_dict_ember["type_fuego"]        = "./screenshots/ember_fuego.PNG"
        self.button_dict_ember["type_hielo"]        = "./screenshots/ember_hielo.PNG"
        self.button_dict_ember["type_planta"]       = "./screenshots/ember_planta.PNG"
        self.button_dict_ember["type_tierra"]       = "./screenshots/ember_tierra.PNG"
        self.button_dict_ember["jugar_button"]      = "./screenshots/jugar.PNG"
        self.button_dict_ember["iniciar_button"]    = "./screenshots/iniciar.PNG"
        self.button_dict_ember["manual_button"]     = "./screenshots/manual.PNG"
        self.button_dict_ember["x1_button"]         = "./screenshots/x1velocidad.PNG"
        self.button_dict_ember["reclamar_button"]   = "./screenshots/reclamar.PNG"
        self.button_dict_ember["continuar_button"]  = "./screenshots/continuar.PNG"
        self.button_dict_ember["salir_button"]      = "./screenshots/salir.PNG"


        self.executable = executable
        self.user_name = user_name
        self.is_get_experience = is_get_experience
        self.energy = 0

    def formatInforme(self,text):

        actual_time = str(datetime.datetime.now().strftime("[%d/%m/%y][%H:%M:%S]"))
        informe = "<p>{} {}</p>".format(actual_time,text)
        return informe

    def moveCursor(self,x,y,click=True,reset=True):

        currentMouseX, currentMouseY = pyautogui.position()
        pyautogui.moveTo(x, y)
        pyautogui.click(x, y)
        if reset:
            pyautogui.moveTo(currentMouseX, currentMouseY)

    def executeCommand(self,command,data_commands):

        global stop, loop, informe

        actual_command_priority = command["priority"]

        if command["type"] == "schedule": 

            print("schedule time...")
            schedule = False
            while not schedule:
                hour = str(datetime.datetime.now().strftime("%H:%M"))
                print("Actual time: {} | Active time:{}".format(hour, command["time"]))
                if hour == command["time"]:
                    schedule = True
                else:
                    time.sleep(60)

        elif command["type"] == "mision":

            informe += self.formatInforme("+++++++++++++++++++++++++++++++++")
            informe += self.formatInforme("+++      MISSION COMMAND      +++")
            informe += self.formatInforme("+++++++++++++++++++++++++++++++++")

            if not stop:

                command_finished = False
                repetitions_count = 0
                last_repetition = 0

                starting_command = True
                while not command_finished:
                    if last_repetition == 0 or last_repetition != repetitions_count+1:
                        debug = "COMMAND MISSION - repetition: {}/{}".format(repetitions_count+1,command["repetition"])
                        informe += self.formatInforme(debug)
                        print(debug)

                    last_repetition = repetitions_count+1

                    last_button_detect = ""

                    for button in self.button_dict_mision.keys():
                        
                        if not stop:

                            buttonlocation = None

                            if button == "misiones_button":
                                buttonlocation = pyautogui.locateCenterOnScreen(self.button_dict_mision[button],grayscale=True,confidence=0.95)
                            elif button == "story_button":
                                buttonlocation = pyautogui.locateCenterOnScreen(self.button_dict_mision[button],grayscale=True,confidence=0.95)
                            
                            elif "mision_" in button:
                                if "mision_{}_button".format(command["mission"]) == button:
                                    buttonlocation = pyautogui.locateCenterOnScreen(self.button_dict_mision[button],grayscale=True,confidence=0.95)
                                    if not buttonlocation:
                                        mission_5_location = pyautogui.locateCenterOnScreen(self.button_dict_mision["mision_5_button"],grayscale=True,confidence=0.95)
                                        if mission_5_location:
                                            self.moveCursor(mission_5_location[0],mission_5_location[1],click=False,reset=False)
                                            if command["mission"] > 5:
                                                scroll_value = -50000000
                                            else:
                                                scroll_value = 50000000

                                            print("SEACHING MISSION ")
                                            for x in range(150):
                                                pyautogui.scroll(scroll_value, x=mission_5_location[0], y=mission_5_location[1])

                            elif "jugar_button" in button:
                                if last_button_detect == "mision_{}_button".format(command["mission"]):
                                    buttonlocation = pyautogui.locateCenterOnScreen(self.button_dict_mision[button],grayscale=True,confidence=0.9)

                            else:
                                buttonlocation = pyautogui.locateCenterOnScreen(self.button_dict_mision[button],grayscale=True,confidence=0.9)

                            if str(type(buttonlocation)) == "<class 'pyscreeze.Point'>":

                                last_button_detect = button

                                x = buttonlocation[0]
                                y = buttonlocation[1]
                                print("DETECT: {}".format(button))
                                self.moveCursor(x, y)

                                if button == "misiones_button":

                                    time.sleep(1)

                                if button == "salir_button":
                                    informe += self.formatInforme("Mission was successfully completed. {}/{}".format(last_repetition,command["repetition"]))
                                    repetitions_count += 1

                            if not command["loop"]:
                                if command["repetition"] == repetitions_count:
                                    command_finished = True

                        if stop:
                            command_finished = True

        elif command["type"] == "ember":

            starting = True
            if self.is_get_experience:
                self.energy = self.getEnergy()
                print("ENERGY: {}".format(self.energy))

            command_finished = False

            if not command_finished:

                informe += self.formatInforme("++++++++++++++++++++++++++++++++")
                informe += self.formatInforme("+++      MISSION EMBERS      +++")
                informe += self.formatInforme("++++++++++++++++++++++++++++++++")

                debug ="COMMAND EMBER - start: {}E - end: {}E - actual: {}E".format(command["start_energy"],command["stop_energy"],self.energy)
                print(debug)
                informe += self.formatInforme(debug)
                while int(command["stop_energy"]) <= int(self.energy) and not stop:

                    last_button_detect = ""

                    for button in self.button_dict_ember.keys():

                        buttonlocation     = None

                        if not stop:

                            if button == "misiones_button":
                                buttonlocation = pyautogui.locateCenterOnScreen(self.button_dict_ember[button],grayscale=True,confidence=0.95)
                                time.sleep(1)
                            elif "jugar_button" in button:
                                if command["ember_type"] in last_button_detect:
                                    
                                    buttonlocation = pyautogui.locateCenterOnScreen(self.button_dict_ember[button],grayscale=True,confidence=0.9)
                            elif "dificulty_" in button:
                                if "dificulty_{}".format(command["ember_dificulty"]) == button:
                                    buttonlocation = pyautogui.locateCenterOnScreen(self.button_dict_ember[button],grayscale=True,confidence=0.95)

                            else:
                                if "type" in button:
                                    if command["ember_type"] in button:

                                        buttonlocation = pyautogui.locateCenterOnScreen(self.button_dict_ember[button],grayscale=True,confidence=0.9)
                                else:
                                    buttonlocation = pyautogui.locateCenterOnScreen(self.button_dict_ember[button],grayscale=True,confidence=0.9)

                            if str(type(buttonlocation)) == "<class 'pyscreeze.Point'>":

                                last_button_detect = button

                                if button == "misiones_button":
                                    if not starting:
                                        if self.is_get_experience:
                                            self.energy = self.getEnergy()
                                            print("ENERGY: {}".format(self.energy))
                                    else:
                                        starting = False

                                if int(command["stop_energy"]) <= int(self.energy) and not stop:

                                    x = buttonlocation[0]
                                    y = buttonlocation[1]
                                    print("DETECT: {}".format(button))
                                    self.moveCursor(x, y)

                                    if button == "salir_button":

                                        print("+200 OBSIDIAN")
                                        print("+1 SPARK {}".format(command["ember_type"]))
                                        informe += self.formatInforme("+200 OBSIDIAN")
                                        informe += self.formatInforme("+1 SPARK {}".format(command["ember_type"]))
                                        for x in range(30):
                                            if not stop:
                                                print("Waiting {} seconds".format(30 - x))
                                                time.sleep(1)

        elif command["type"] == "energy":

            print("LOADING ENERGY - {} ...".format(command["load_energy"]))
            informe += self.formatInforme("\n\n...LOADING ENERGY...")
            if self.is_get_experience:
                self.energy = self.getEnergy()
                print("ENERGY: {}".format(self.energy))

            while int(command["load_energy"]) > int(self.energy) and not stop:

                for x in range(60):
                    if not stop:
                        time.sleep(1)
                    else:
                        break
                if not stop:
                    if self.is_get_experience:
                        self.energy = self.getEnergy()
                        print("ENERGY: {}".format(self.energy))

        elif command["type"] == "loop":
            if not stop:
                print("LOOPING...")
                loop += 1

    def getEnergy(self):

        RETRY = 3
        for retry in range(RETRY):
            try:
                image_screenshot = './screenshots/screen.jpg'
                image_screenshot_dragonary = './screenshots/dragonary.jpg'

                # get screensize
                my = pygetwindow.getWindowsWithTitle('Dragonary')[0]
                save_x = my.topleft.x
                save_y = my.topleft.y

                my.activate()
                time.sleep(3)

                # save screenshot
                p = pyautogui.screenshot()
                p.save(image_screenshot)

                # # edit screenshot
                im = PIL.Image.open(image_screenshot)

                left   = save_x
                top    = save_y
                right  = left + my.width
                bottom = top + my.height

                im_crop = im.crop((left,top,right,bottom))
                im_crop.save(image_screenshot_dragonary, quality=100)

                reader = easyocr.Reader(['en'])
                result = reader.readtext(image_screenshot_dragonary)

                for x in result:
                  if "/" in x[1]:
                    try:
                        result = x[1].split("/")[0]
                        if len(result) > 2:
                            result = result[1:]
                        return int(result)
                    except:
                        pass
            except:
                for x in range(60):
                    if not stop:
                        time.sleep(1)
                pass

            return 0

        self.closeDragonary()
        self.openDragonary()
        
        return 0

    def openDragonary(self):

        global stop

        processes = subprocess.Popen('tasklist', stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0]
        if not "Dragonary.exe" in str(processes):

            if self.executable:
                print("Executing Dragonary.exe...")
                os.system("start {}".format(self.executable))
                for x in range(60):
                    if not stop:
                        print("Starting in {} seconds".format(60-x))
                        time.sleep(1)
            else:
                self.parent.onSignalMessage.emit("OPEN DRAGONARY","Please open dragonary.exe.\nIf you want it to open automatically, you must write the path to the executable in preferences","critical",False)
                stop = True

    def closeDragonary(self):

        try:
            processes = subprocess.Popen('tasklist', stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0]

            if "Dragonary.exe" in str(processes):

                os.system('taskkill /f /im "Dragonary.exe"')
                print("Dragonary.exe closed")

        except:
            pass

    @thread
    def startAutoExperience(self,data_commands):

        global stop, loop, informe

        stop = False
        loop = 1
        self.energy = 0

        print("AutoExperience starting...")

        if self.user_name:
            if data_commands:
                
                while not stop and loop == 1: 
                    informe = "" 
                    loop -= 1  
                    self.openDragonary()
                    if not stop:
                        for command in data_commands:

                            self.executeCommand(command,data_commands)

                        self.closeDragonary()
                        if self.parent.email:
                            mail_sender = mutils.EmailSender(encrypt.decode("7773786f626665632e6d7973784071776b73762e6d7977",10), encrypt.decode('5731326631326d31322b',10), self.parent.email)
                            mail_sender.sendMsg("Dragonary AUTOEXPERIENCE",informe)

            else:
                print("[WARNING] No task is scheduled. Please add at least one to the list.")


            print("AutoExperience stopped")

        else:

            self.parent.onSignalMessage.emit("MISSING CREDENTIALS","Please insert credentials before starting.","critical",False)
            stop = True
            print("AutoExperience stopped")
            self.parent.onPlaySignal.emit()


        self.parent.onPlaySignal.emit()

    def stopAutoExperience(self):

        global stop

        stop = True

class UI(QtWidgets.QMainWindow):
    
    onShow = QtCore.Signal()
    onPlaySignal = QtCore.Signal()
    onSignalMessage = QtCore.Signal(str, str, str,bool)

    def __init__(self, main=None,parent = None):

        super(UI, self).__init__(parent)

        self.loading = loading.Loading()
        self.main    = main
        self.autoexperience = AUTOEXPERIENCE(parent=self)

        self.createWidgets()
        self.createLayout()
        self.createStyle()
        self.createConnections()
        self.initialize()

    def createWidgets(self):

        self.window          = mainWindow.MainWindow(self)
        self.main_widget     = QtWidgets.QWidget()

        self.main_layout     = QtWidgets.QVBoxLayout(self.main_widget)
        # self.top_frame       = QtWidgets.QFrame()
        # self.top_layout      = QtWidgets.QHBoxLayout(self.top_frame)

        self.central_layout = QtWidgets.QHBoxLayout()
        self.toolbar_frame   = QtWidgets.QFrame()
        self.toolbar_layout  = QtWidgets.QVBoxLayout(self.toolbar_frame)

        self.user_name_label = QtWidgets.QLabel()
        self.button_preferences  = customWidgets.ButtonIcon(icon = "./ui/resources/img/preferences.png",size=[32,32])

        self.button_play            = customWidgets.ButtonIcon(icon = "./ui/resources/img/play.png",size=[32,32])
        self.button_shell           = customWidgets.ButtonIcon(icon = "./ui/resources/img/shell.png",size=[32,32])
        self.button_actions         = customWidgets.ButtonIcon(icon = "./ui/resources/img/action.png",size=[32,32])

        self.central_widget = CentralWidget(self)

    def createLayout(self):

        self.setCentralWidget(self.main_widget)
        # self.main_layout.addWidget(self.top_frame)
        self.main_layout.addLayout(self.central_layout)
        # self.top_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        # self.top_layout.addWidget(self.user_name_label)
        # self.top_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.central_layout.addWidget(self.toolbar_frame)
        self.central_layout.addWidget(self.central_widget)

        self.toolbar_layout.addWidget(self.button_play)
        self.toolbar_layout.addWidget(self.button_shell)
        self.toolbar_layout.addWidget(self.button_actions)
        self.toolbar_layout.addItem(QtWidgets.QSpacerItem(5, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.toolbar_layout.addWidget(self.button_preferences)

    def createStyle(self):

        # self.top_frame.setStyleSheet("QFrame{background-color:palette(alternate-base)}")
        # self.top_frame.setMaximumHeight(50)
        # self.top_frame.setMinimumHeight(50)
        # self.top_layout.setContentsMargins(0,0,5,0)
        self.toolbar_frame.setStyleSheet("QFrame{background-color:palette(alternate-base)}")
        self.toolbar_frame.setMaximumWidth(50)
        self.toolbar_frame.setMinimumWidth(50)
        self.toolbar_layout.setContentsMargins(10,10,10,10)

        self.setStyleSheet(stylesheet.data)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)

        # sh = QtWidgets.QGraphicsDropShadowEffect(self)
        # sh.setColor(QtGui.QColor(0,0,0,255))
        # sh.setBlurRadius(15)
        # sh.setYOffset(0)
        # sh.setXOffset(0)
        # self.top_frame.setGraphicsEffect(sh)

        sh = QtWidgets.QGraphicsDropShadowEffect(self)
        sh.setColor(QtGui.QColor(0,0,0,255))
        sh.setBlurRadius(15)
        sh.setYOffset(5)
        sh.setXOffset(0)
        self.toolbar_frame.setGraphicsEffect(sh)
        
        self.user_name_label.setStyleSheet("font: 32px Consolas;padding:5")

        self.button_play.setCheckable(True)

    def createConnections(self):

        self.button_preferences.clicked.connect(self.onPreferences)
        self.onShow.connect(self.window.show)
        self.button_play.clicked.connect(self.onPlay)
        self.button_shell.clicked.connect(lambda:self.onChangeCentral(0))
        self.button_actions.clicked.connect(lambda:self.onChangeCentral(1))
        self.onPlaySignal.connect(lambda:self.onPlay(0))
        self.onSignalMessage.connect(self.onMessage)



    def initialize(self):

        self.core = CORE(self)
        self.core.start(self.core.initialize)

    def onPreferences(self):

        self.preferences = PanelPreferences(parent = self)
        self.preferences.move(0, 0)
        self.preferences.resize(self.width(), self.height())
        self.preferences.readData()
        self.preferences.show()

    def onMessage(self,title, msg, type="about",detailed=False):

        icon  = {"info"     :QtWidgets.QMessageBox.Information,
                 "warning"  :QtWidgets.QMessageBox.Warning,
                 "critical" :QtWidgets.QMessageBox.Critical,
                 "question" :QtWidgets.QMessageBox.Question,
                 "about"    :QtWidgets.QMessageBox.Information,}

        black_screen_message = customWidgets.BlackScreen(parent=self.window)
        black_screen_message.move(0, 0)
        black_screen_message.resize(self.width(), self.height())
        black_screen_message.show()
        value = None
        
        if detailed:
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setWindowTitle(title)
            msgbox.setText(msg)
            msgbox.setIcon(icon[type])
            msgbox.setDetailedText(detailed)
            msgbox.exec_()

        elif type == "about":
            if not detailed:
                QtWidgets.QMessageBox.about(self,title, msg)
        elif type == "warning":
            print("[WARNING] {}".format(msg))
            if not detailed:
                QtWidgets.QMessageBox.warning(self,title, msg)
        elif type == "information":
            if not detailed:
                QtWidgets.QMessageBox.information(self,title, msg)
        elif type == "critical":
            print("[ERROR] {}".format(msg))
            if not detailed:
                QtWidgets.QMessageBox.critical(self,title, msg)
        elif type == "question":
            question = QtWidgets.QMessageBox.question(self,title, msg)
            if question == QtWidgets.QMessageBox.Yes:
                value = True
            else:
                value = False

        black_screen_message.close()

        if value:
            return value

    def onPlay(self,value):

        
        if value:
            self.button_play.changeIcon("./ui/resources/img/stop.png")
            self.button_play.setChecked(True)
            self.onChangeCentral(0)
            self.autoexperience.startAutoExperience(self.central_widget.list_action.list_action.returnData())
        else:
            self.button_play.setChecked(False)
            self.button_play.changeIcon("./ui/resources/img/play.png")
            self.autoexperience.stopAutoExperience()

    def onChangeCentral(self,value):

        self.central_widget.stacked.slideInIdx(value)

    def readSettings(self,start=False):

        #READ DATA
        self.settings = QtCore.QSettings(os.environ["APPDATA"]+"/dragonary_autoexperience/preferences.ini",QtCore.QSettings.IniFormat)
        data = self.settings.value('preferences')

        try:
            self.user_name   = encrypt.decode(data["NAME"],10)
            if self.user_name != "":
                self.autoexperience.user_name = self.user_name
            else:
                self.autoexperience.user_name = None

        except:
            self.user_name = ""  

        try:
            self.autoexperience.executable = encrypt.decode(data["EXECUTABLE"],10)
        except:
            self.autoexperience.executable = None

        try:
            self.email = encrypt.decode(data["EMAIL"],10)
        except:
            self.email = None

        self.user_name_label.setText(self.user_name)

    def readConfig(self):

        if os.path.exists(os.environ["APPDATA"]+"/dragonary_autoexperience/config.json"):
            self.config = mutils.jsonRead(os.environ["APPDATA"]+"/dragonary_autoexperience/config.json")
        else:
            self.config = []

        for config in self.config:

            self.central_widget.list_action.list_action.onAddActionWidget.emit(config["type"],config)

    def closeEvent(self,event):

        self.autoexperience.stopAutoExperience()

        super(UI,self).closeEvent(event)

class CORE(QtCore.QThread):

    def __init__(self,main):
        super(CORE,self).__init__()

        self.main = main

    def start(self,function):

        self.function = function

        return super(CORE,self).start()

    def run(self):

        self.function()

    def initialize(self):

        self.main.loading.log.setText("Loading last session...")
        self.main.readSettings()
        self.main.readConfig()

        time.sleep(1)

        self.main.loading.log.setText("Loading core...")
        time.sleep(1)

        self.main.loading.log.setText("Initialize...")
        time.sleep(1)

        self.main.onShow.emit()
        self.main.loading.onClose.emit()