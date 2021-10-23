from PySide2 import QtCore, QtGui, QtWidgets

class AnimPushButton(QtWidgets.QPushButton):
    def __init__(self, icon=None, text="", size=None, tooltip=None, checked=False, parent=None):
        super().__init__(parent)
        self.checked = checked
        self._animation = None
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred))
        if icon: self.setIcon(icon)
        if text: self.setText(text)
        if tooltip: self.setToolTip(tooltip)
        if size: 
            self.setMinimumSize(QtCore.QSize(size[0],size[1]))
            if icon:
                self.setIconSize(QtCore.QSize(size[0],size[1]))

    def setAnimation(self,time=0, valueA="", valueB=""):

        self._animation = QtCore.QVariantAnimation(self)

        self._animation.valueChanged.connect(self._animate)
        self._animation.setStartValue(QtGui.QColor(valueA))
        self._animation.setEndValue(QtGui.QColor(valueB))
        self._animation.setDuration(time)

    def _animate(self, value):
        if not self.checked:
            style = "*{{background-color: {value};border:5px solid {value}}}".format(value=value.name())+"*:pressed{background-color:palette(highlight);border:5px solid palette(highlight)}"
        else:
            style = "*{{background-color: {value};border:5px solid {value}}}".format(value=value.name())+"*:pressed{background-color:palette(highlight);border:5px solid palette(highlight)}*:checked{background-color:palette(highlight);border:5px solid palette(highlight)}"
        self.setStyleSheet(style)
        

    def enterEvent(self, event):
        if self._animation:
            self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
            self._animation.start()
            super().enterEvent(event)

    def leaveEvent(self, event):
        if self._animation:
            self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
            self._animation.start()
            super().enterEvent(event)

class APushButton(QtWidgets.QPushButton):
    def __init__(self, title="",time=None, valueA=None, valueB=None, radius=0, parent=None):
        super().__init__(parent)
        self._animation = None
        self._radius = radius
        self.setText(title)
        if not time and not valueA and not valueB:self.setAnimation(250,QtGui.QPalette().color(QtGui.QPalette.Mid).name(),QtGui.QPalette().color(QtGui.QPalette.Light).name())
        else: self.setAnimation(time, valueA, valueB)

    def setAnimation(self,time=0, valueA="", valueB=""):

        self._animation = QtCore.QVariantAnimation(self)

        self._animation.valueChanged.connect(self._animate)
        self._animation.setStartValue(QtGui.QColor(valueA))
        self._animation.setEndValue(QtGui.QColor(valueB))
        self._animation.setDuration(time)

    def _animate(self, value):

        style = "*{{background-color: {value};border:None;padding:10px;border-radius:{radius}}}".format(value=value.name(),radius=self._radius)
        self.setStyleSheet(style)

    def enterEvent(self, event):
        if self._animation:
            self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
            self._animation.start()
            super().enterEvent(event)

    def leaveEvent(self, event):
        if self._animation:
            self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
            self._animation.start()
            super().enterEvent(event)

class AToolButton(QtWidgets.QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animation = None
        
    def setAnimation(self,time=0, valueA="", valueB=""):

        self._animation = QtCore.QVariantAnimation(self)

        self._animation.valueChanged.connect(self._animate)
        self._animation.setStartValue(QtGui.QColor(valueA))
        self._animation.setEndValue(QtGui.QColor(valueB))
        self._animation.setDuration(time)

    def _animate(self, value):
        style = "*{background-color: "+value.name()+";border:None}"\
                "*::menu-button {background-color: palette(Base)}"\
                "*::menu-arrow {image: url(resources/img/arrowRight)} "\
                "*::menu-button:hover {background-color: 2px palette(Highlight);border-left:2px solid palette(Base);}"\
                "*:checked{background-color:palette(Highlight)}"\
                "*::menu-arrow:open {image: url(resources/img/arrowDown)}"
                                            

        self.setStyleSheet(style)
        

    def enterEvent(self, event):
        if self._animation:
            self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
            self._animation.start()
            super().enterEvent(event)

    def leaveEvent(self, event):
        if self._animation:
            self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
            self._animation.start()
            super().enterEvent(event)

class ButtonIcon(QtWidgets.QPushButton):

    def __init__(self,text="",icon = None,size=[64,64],default_color=[175,175,175,255],hover_color=[225,225,225,255],pressed_color=[255,255,255,255],checked_color=[255,255,255,255],animation=False,parent=None):
        super(ButtonIcon,self).__init__(text,parent=None)

        self._animation     = animation
        self.default_color  = default_color
        self.hover_color    = hover_color
        self.pressed_color  = pressed_color
        self.checked_color  = checked_color
        self.icon           = QtGui.QPixmap(icon)
        self.applyTint(*self.default_color)
        self.setIconSize(QtCore.QSize(*size))
        self.setMinimumSize(*size)
        self.setMaximumSize(*size)
        self.setStyleSheet("ButtonIcon{background-color:transparent}"\
                           "ButtonIcon:pressed{background-color:transparent}"\
                           "ButtonIcon:checked{background-color:transparent;padding:0px;margin:0px;spacing:0px}"\
                           "ButtonIcon:unchecked{background-color:transparent;padding:0px;margin:0px;spacing:0px}"\
                           "ButtonIcon::menu-indicator {image:None}")
        self.setFlat(True)

    def applyTint(self,r,g,b,a):

        temp = QtGui.QPixmap(self.icon)
        color = QtGui.QColor(r,g,b,a)
        painter = QtGui.QPainter(temp)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        painter.setCompositionMode(painter.CompositionMode_SourceIn)
        painter.fillRect(temp.rect(), color)
        painter.end()
        self.setIcon(temp)

    def enterEvent(self, event):
        r = super(ButtonIcon,self).enterEvent(event)
        if self._animation:
            self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
            self._animation.start()
        else:
            self.applyTint(*self.hover_color)

        if self.isCheckable():
            self.check(self.hover_color)


        return r

    def leaveEvent(self, event):

        r = super(ButtonIcon,self).leaveEvent(event)

        if self._animation:
            self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
            self._animation.start()
        else:
            self.applyTint(*self.default_color)

        if self.isCheckable():
            self.check(self.default_color)

        return r

    def mousePressEvent(self, event):
        r = super(ButtonIcon,self).mousePressEvent(event)
        if self._animation:
            self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
            self._animation.start()
        else:
            self.applyTint(*self.pressed_color)

        if self.isCheckable():
            self.check(self.pressed_color)

        return r

    def mouseReleaseEvent(self, event):
        r = super(ButtonIcon,self).mouseReleaseEvent(event)
        if self._animation:
            self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
            self._animation.start()
        else:
            self.applyTint(*self.hover_color)

        if self.isCheckable():
            self.check(self.hover_color)

        return r

    def check(self,color):

        if self.isChecked():

            self.applyTint(*self.checked_color)

        else:

            self.applyTint(*color)

    def checkStateSet(self):
        
        if self.isCheckable():
            self.check(self.default_color)

    def changeIcon(self,icon):

        self.icon           = QtGui.QPixmap(QtGui.QPixmap(icon))
        self.setIcon(self.icon)

class CComboBox(QtWidgets.QComboBox):
    def __init__(self, scrollWidget=True, *args, **kwargs):
        super(CComboBox, self).__init__(*args, **kwargs)  
        self.scrollWidget=scrollWidget
    def wheelEvent(self, *args, **kwargs):
        if self.hasFocus():
            if not self.scrollWidget:
                return None

class ProjectButton(QtWidgets.QPushButton):

    def __init__(self,text="", icon = None, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.icon = icon
        self._animation = None
        self.setMinimumSize(200,200)
        self.setMaximumSize(200,200)

    def setIcon(self,icon):

        self.icon = icon

    def setAnimation(self,time=0, border=0):

        self._animation = QtCore.QVariantAnimation(self)
        self._animation.valueChanged.connect(self._animate)
        self._animation.setStartValue(10)
        self._animation.setEndValue(border)
        self._animation.setDuration(time)
        # self._animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)

    def _animate(self, value):
        # "QPushButton{;}QPushButton:hover{border-image: url();background-color:palette(Highlight);color:white;}QPushButton:pressed{margin: 2px;}"
        style = "*{{border-image: url({ico}) ;color: rgba(255, 255, 255, 0);border-radius:{value}}}*:hover{{border-image: url();background-color:palette(Highlight);color:white;}}*:pressed{{margin: 2px;}}".format(ico = self.icon,value=value)

        self.setStyleSheet(style)

        
    def enterEvent(self, event):
        if self._animation:
            self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
            self._animation.start()

            super().enterEvent(event)

    def leaveEvent(self, event):
        if self._animation:
            self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
            self._animation.start()

            super().enterEvent(event)

class ProgressBar(QtWidgets.QProgressBar):

    changeProgressBar = QtCore.Signal(int)
    onInfiniteProgressBar = QtCore.Signal(bool)
    onError = QtCore.Signal(bool)

    def __init__(self):

        super(ProgressBar,self).__init__()

        self.createConnections()

    def createConnections(self):

        self.changeProgressBar.connect(self.setValue)
        self.onInfiniteProgressBar.connect(self.setInfiniteProgressBar)
        self.onError.connect(self.setError)

    def setProgressBar(self,value):

        self.changeProgressBar.emit(int(value))

    def setInfiniteProgressBar(self,value):

        if value:
            self.setMinimum(0)
            self.setMaximum(0)
        else:
            self.setMinimum(0)
            self.setMaximum(100)

    def setError(self,value):

        if value:
            self.setInfiniteProgressBar(False)
            self.setProgressBar(100)
            self.setStyleSheet("QProgressBar::chunk {background-color: red;border-radius: 4px}QProgressBar{text-align: center}")
            self.setFormat("ERROR")
        else:
            self.setStyleSheet("")
            self.setFormat("%p%")

class RoundButton(QtWidgets.QLabel):

    clicked = QtCore.Signal()

    def __init__(self, *args,text="",icon=None,background="palette(highlight)",size=[256,256],**kwargs):
        super(RoundButton, self).__init__(*args, **kwargs)
        self._text = text
        self.background = background
        self._size = size
        self.setMaximumSize(self._size[0], self._size[1])
        self.setMinimumSize(self._size[0], self._size[1])
        self.radius = ((self._size[0]+self._size[1])/2)/2 

        self.active = True

        self.target = QtGui.QPixmap(self.size())  
        self.target.fill(QtCore.Qt.transparent)   

        self._icon = icon

        self.target = QtGui.QPixmap(self.size())  
        self.target.fill(QtCore.Qt.transparent)   

        p = QtGui.QPixmap(self._icon).scaled(self._size[0], self._size[1], QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        self.painter = QtGui.QPainter(self.target)
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        self.painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)

        path = QtGui.QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)

        self.painter.setClipPath(path)
        self.painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)

        self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
    
    def setActive(self,status):

        self.active = status

        if not self.active:
            self.setStyleSheet("background-color:palette(mid);border-radius:{}".format(self.radius))
            self.setText("")
            self.setPixmap(QtGui.QPixmap())
            p = QtGui.QPixmap(self._icon).scaled(self._size[0], self._size[1], QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
            self.painter.drawPixmap(0, 0, p)
            self.setPixmap(self.target)
            self.repaint()

    def setIcon(self,icon):
        self._icon = icon
        p = QtGui.QPixmap(self._icon).scaled(self._size[0], self._size[1], QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        self.painter.drawPixmap(0, 0, p)
        self.setPixmap(QtGui.QPixmap())
        self.setPixmap(self.target)
        self.repaint()

    def mousePressEvent(self,event):
        if self.active:
            self.clicked.emit()

    def enterEvent(self, event):

        if self.active:
            self.setStyleSheet("background-color:{};border-radius:{}".format(self.background,self.radius))
            self.setText(self._text)
            super().enterEvent(event)

    def leaveEvent(self, event):

        self.setStyleSheet("background-color:palette(mid);border-radius:{}".format(self.radius))
        self.setText("")
        self.setPixmap(self.target)
        super().enterEvent(event)

    def closeEvent(self,event):

        self.painter.end()
        
class SimpleDropdown(QtWidgets.QWidget):

    '''
    
    Utility class used all throught the UI as a hide and show button.
    :type title: str() 

    '''

    def __init__(self, title = "", parent = None):
        super(SimpleDropdown, self).__init__(parent)
        self.title = title
        self.expand = True
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum))

        self.createWidgets()
        self.createLayout()
        self.createConnections()
    
    def createWidgets(self):
        self.central_layout = QtWidgets.QGridLayout(self)
        self.central_layout.setContentsMargins(0,0,0,0)
        self.button = QtWidgets.QPushButton(QtGui.QIcon("resources/img/arrowDown.png"),"   "+self.title)
        self.button.setCheckable(True)
        self.button.setChecked(True)
        self.frame = QtWidgets.QFrame()
        self.frame_layout = QtWidgets.QVBoxLayout(self.frame)
        self.frame_layout.setContentsMargins(0,0,0,0)

    def createLayout(self):
        self.central_layout.addWidget(self.button)
        self.central_layout.addWidget(self.frame)

    def createConnections(self):

        self.button.clicked.connect(self.setExpand)

    def addWidget(self,widget):

        self.frame_layout.addWidget(widget)

    def setTitle(self,text):
        self.button.setText(text)

    def setExpand(self):
        if self.button.isChecked():
            self.frame.show()
            self.button.setIcon(QtGui.QIcon("resources/img/arrowDown.png"))
        else:
            self.frame.hide()
            self.button.setIcon(QtGui.QIcon("resources/img/arrowRight.png"))
            
class PushButtonToolTip(ButtonIcon):

    def __init__(self,text="",icon="", size=[32,32], tooltip="", align="right",parent=None):

        super(PushButtonToolTip, self).__init__(text=text,icon=icon,size=size,parent=parent)
        self.setText(text)
        # self.setIcon(QtGui.QIcon(icon))
        self.setIconSize(QtCore.QSize(size[0],size[1]))
        self.tooltip = ToolTip(button = self,tooltip=tooltip,parent = parent)

    def enterEvent(self, event):
        self.tooltip.show()
        super(PushButtonToolTip, self).enterEvent(event)

    def leaveEvent(self, event):
        self.tooltip.close()
        super(PushButtonToolTip, self).leaveEvent(event)

class ToolButtonToolTip(QtWidgets.QToolButton):

    def __init__(self,text="",icon="", size=[32,32], tooltip="", align="right",parent=None):

        super(ToolButtonToolTip, self).__init__()
        self.setText(text)
        self.setIcon(QtGui.QIcon(icon))
        self.setIconSize(QtCore.QSize(size[0],size[1]))
        self.tooltip = ToolTip(button = self,tooltip=tooltip,parent = parent)

    def enterEvent(self, event):
        self.tooltip.show()

    def leaveEvent(self, event):
        self.tooltip.close()

class ToolTip(QtWidgets.QWidget):

    BorderColor     = QtGui.QColor(0, 0, 0, 255)     
    BackgroundColor = QtGui.QColor(0, 0, 0, 255) 
    textColor       = QtGui.QColor(245, 245, 245, 255) 

    def __init__(self, button=None,tooltip="",align="right", parent=None):

        super(ToolTip, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.parent = parent
        self.button = button
        self.tooltip= tooltip
        self.align  = align
        self.hide()

    def paintEvent(self, event):

        super(ToolTip, self).paintEvent(event) 
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)   

        rectPath = QtGui.QPainterPath()                      
        rect = QtCore.QRectF(self.button.pos().x(), self.button.pos().y(), 120, 30)
        rectPath.addRoundedRect(rect, 5, 5)
        painter.setPen(QtGui.QPen(self.BorderColor, 2, QtCore.Qt.SolidLine,QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.setBrush(self.BackgroundColor)
        painter.drawPath(rectPath)
        painter.setPen(QtGui.QPen(self.textColor, 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawText(rect, QtCore.Qt.AlignCenter,self.tooltip)

        self.resize(self.parent.width(),self.parent.height())
        self.raise_()

class AdjustTextEdit(QtWidgets.QTextEdit):

    def __init__(self, *args, **kwargs):
        super(AdjustTextEdit, self).__init__(*args, **kwargs)  
        self.document().contentsChanged.connect(self.sizeChange)
        self.document().documentLayout().documentSizeChanged.connect(self.sizeChange)
        self.textChanged.connect(self.sizeChange)
        self.heightMin = 0
        self.heightMax = 65000

    def sizeChange(self):

        docHeight = self.document().size().height()
        if self.heightMin <= docHeight <= self.heightMax:
            if docHeight == 0: docHeight = 30
            
            elif len(self.toPlainText())<=1: docHeight = 30
            self.setMaximumHeight(docHeight+20)
            self.setMinimumHeight(docHeight+20)
   
class BlackScreen(QtWidgets.QWidget):

    pen_color = QtGui.QColor("#333333")
    onStop = QtCore.Signal()

    def __init__(self, widget=None,fill_color=QtGui.QColor(30, 30, 30, 230),alpha=120,animation=True, parent=None):

        super(BlackScreen, self).__init__(parent)

        self.fill_color = fill_color
        self.parent = parent
        self.alpha = alpha
        self.animation = animation

        self.createWidgets()
        self.createLayout()
        self.createConnections()
        
        if widget:
            self.addWidget(widget)

    def createWidgets(self):

        self.main_layout = QtWidgets.QGridLayout(self)

        self.main_layout.setVerticalSpacing(0)
        self.main_layout.setHorizontalSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)


    def createLayout(self):

        self.main_layout.addItem(QtWidgets.QSpacerItem(10, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding),0,1)
        self.main_layout.addItem(QtWidgets.QSpacerItem(10, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding),2,1)
        self.main_layout.addItem(QtWidgets.QSpacerItem(10, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),1,0)
        self.main_layout.addItem(QtWidgets.QSpacerItem(10, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),0,2)

    def createConnections(self):
        
        self.onStop.connect(self.stop)

    def start(self):
        time = 40
        for t in range(time):
            self.fill_color = QtGui.QColor(30, 30, 30, round(t*(self.alpha/time)))
            self.repaint ()

        self.fill_color = QtGui.QColor(30, 30, 30, self.alpha)
        self.repaint ()

    def stop(self):

        if self.animation:
            time = 20
            for t in range(time):
                self.fill_color = QtGui.QColor(30, 30, 30, self.alpha-round(t*(self.alpha/time)))
                self.repaint ()

        self.close()

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


    def addWidget(self,widget):

        self.main_layout.addWidget(widget,1,1)
        widget.installEventFilter(self)

    def eventFilter(self, obj, event):

        if isinstance(event,QtGui.QCloseEvent):
            self.stop()
            return True

        return False

class SwitchAnimate(QtWidgets.QCheckBox):

    def __init__(self,text="",width = 30, bg_color = "#777", circle_color = "#DDD", active_color = "#00BCff", animation_curve = QtCore.QEasingCurve.OutBounce):
        super(SwitchAnimate,self).__init__()

        self.setText(text)
        self.setFixedSize(width,17)
        self.setCursor(QtCore.Qt.PointingHandCursor)

        self._bg_color     = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

        self.circle_position = 2
        self.animation = QtCore.QVariantAnimation(self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(400)
        self.animation.valueChanged.connect(self.setCirclePosition)

        self.stateChanged.connect(self.transition)

    def setCirclePosition(self,value):
        self.circle_position = value
        self.update()

    def transition(self, value):
        self.animation.stop()
        if value:
            self.animation.setStartValue(2)
            self.animation.setEndValue(self.width() - 14)
        else:
            self.animation.setStartValue(self.width() - 14)
            self.animation.setEndValue(2)

        self.animation.start()

    def hitButton(self, pos):

        return self.contentsRect().contains(pos)
    
    def paintEvent(self, e):

        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)

        p.setPen(QtCore.Qt.NoPen)

        rect = QtCore.QRect(0,0, self.width(), self.height())

        if not self.isChecked():

            p.setBrush(QtGui.QColor(self._bg_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

            p.setBrush(QtGui.QColor(self._circle_color))
            p.drawEllipse(self.circle_position, 2, 12, 12)

        else:

            p.setBrush(QtGui.QColor(self._active_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height() / 2)

            p.setBrush(QtGui.QColor(self._circle_color))
            p.drawEllipse(self.circle_position, 2, 12, 12)

        p.end()
        
class Switch(QtWidgets.QWidget):

    clicked = QtCore.Signal(bool)

    def __init__(self, textA="",textB="", parent=None):

        super(Switch, self).__init__(parent) 
        self.textA = textA
        self.textB = textB
        self.createWidgets()
        self.createLayout()
        self.createStyle()

    def createWidgets(self):

        self.central_layout = QtWidgets.QHBoxLayout(self)
        self.slider         = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.textA_label    = QtWidgets.QLabel(self.textA)    
        self.textB_label    = QtWidgets.QLabel(self.textB)  

    def createLayout(self):

        self.central_layout.addWidget(self.textA_label)
        self.central_layout.addWidget(self.slider)
        self.central_layout.addWidget(self.textB_label)

    def createStyle(self):
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.slider.sliderPressed.connect(lambda:self.mousePressEvent("click"))
        self.slider.actionTriggered.connect(lambda:self.mousePressEvent("click"))
        self.slider.setRange (0, 1)
        self.slider.setMaximumSize(40,20)
        self.slider.setStyleSheet(  "QSlider::groove:horizontal {height: 15px;width: 30px;background:palette(base);margin: 2px 0;border-radius: 2px;}"\
                                    "QSlider::handle:horizontal {background:palette(mid);width: 15px;height: 15px;border-radius: 2px;}")

    def mousePressEvent(self,event):

        if self.slider.value() == 0:
            self.slider.setValue(1)
            result = True
        else:
            self.slider.setValue(0)
            result = False

        self.clicked.emit(result)

    def setValue(self,value):

        self.slider.setValue(int(value))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    w = ButtonIcon(icon=r"C:\Users\Emanuel\Documents\scripts\Momfinds\1_0_0\momfinds\ui\resources\img\inbox.png")
    w.clicked.connect(lambda:print("OK"))
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())