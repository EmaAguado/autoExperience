from PySide2 import QtCore, QtGui, QtWidgets, QtCharts

class Chart(QtCharts.QtCharts.QChartView):
    def __init__(self,parent=None):

        super(Chart,self).__init__()

        self.zoom_in_factor = 1.25
        self.zoom_in_factor = 1.25
        self.zoom_clamp     = True
        self.zoom           = 1
        self.zoom_step      = 1
        self.zoom_range     = [1,9]

        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.setMouseTracking(True)
        self.setRenderHint(QtGui.QPainter.Antialiasing)


    def wheelEvent(self, event):
        

        zoom_out_factor = 1 / self.zoom_in_factor

        if event.angleDelta().y() > 0:

            zoom_factor = self.zoom_in_factor
            self.zoom += self.zoom_step

        else:

            zoom_factor = zoom_out_factor
            self.zoom -= self.zoom_step


        clamped = False

        if self.zoom < self.zoom_range[0]: self.zoom, clamped = self.zoom_range[0], True
        if self.zoom > self.zoom_range[1]: self.zoom, clamped = self.zoom_range[1], True

        if not clamped or self.zoom_clamp is False:

            self.chart().zoom(zoom_factor)#(zoom_factor, zoom_factor)

        else:
            self.chart().zoomReset()

    def mousePressEvent(self,event):
    
        if event.button() == QtCore.Qt.MiddleButton:
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
            self.m_lastMousePos = event.pos()
            event.accept()

        super(Chart,self).mousePressEvent(event)

    def mouseMoveEvent(self, event):

        if (event.buttons() & QtCore.Qt.MiddleButton):
            dPos = event.pos() - self.m_lastMousePos
            self.chart().scroll(-dPos.x(), dPos.y())

            self.m_lastMousePos = event.pos()
            event.accept()

            QtWidgets.QApplication.restoreOverrideCursor()
        
        super(Chart,self).mouseMoveEvent(event)

class Graphic(QtWidgets.QFrame):

    addValue = QtCore.Signal(int or None,list or None)

    def __init__(self, main=None):

        super(Graphic,self).__init__()

        self.main  = main
        self.data  = []
        self.index = 0
        self.max_hash = 0
        self.createWidgets()
        self.createLayout()
        self.createStyle()
        self.createConnections()
        # self.refresh([[0,0],[0,1],[0,2]])
        

    def createWidgets(self):

        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.chart_view = Chart()
        self.chart = QtCharts.QtCharts.QChart()

        self.line = QtCharts.QtCharts.QLineSeries()

        self.chart.addSeries(self.line)

        self.chart.setTitle("HashRate")
        self.chart.setAnimationOptions(QtCharts.QtCharts.QChart.SeriesAnimations)

        axisX = QtCharts.QtCharts.QValueAxis()
        axisX.setGridLineVisible(False)
        self.chart.addAxis(axisX, QtCore.Qt.AlignBottom)
        self.line.attachAxis(axisX)

        axisY = QtCharts.QtCharts.QValueAxis()
        self.chart.addAxis(axisY, QtCore.Qt.AlignLeft)
        self.line.attachAxis(axisY)

        self.chart.legend().setVisible(True)

        self.chart_view.setChart(self.chart)
        self.chart_view.chart().setTheme(QtCharts.QtCharts.QChart.ChartThemeDark)

    def createLayout(self):

        self.main_layout.addWidget(self.chart_view)

    def createStyle(self):

        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.chart_view.setRenderHint(QtGui.QPainter.Antialiasing)

    def createConnections(self):

        self.addValue.connect(self.onAddValue)

    def refresh(self,data=None):

        if data:
            self.line.clear()

            x = 0
            for i in data:
                self.line << QtCore.QPointF(x, i[1])

                x += 1

    def onAddValue(self,value=None,data=None):
        
        if not data:
            self.max_hash = value if self.max_hash < value else self.max_hash
            self.index += 1
            self.data.append([self.index, value])

        else:
            self.data = data

        self.line.clear()
        n = 0
        for i in self.data:
            self.line << QtCore.QPointF(n,i[1])
            n += 1
            if data:
                self.max_hash = i[1] if i[1] > self.max_hash else self.max_hash

        if not data:
            self.chart.axisX().setRange(0,self.index)
            self.chart.axisY().setRange(0,self.max_hash)
        else:
            self.chart.axisX().setRange(0,n)
            self.chart.axisY().setRange(0,self.max_hash)


class PayGraphic(QtWidgets.QFrame):

    addValue = QtCore.Signal(list or None)

    def __init__(self, main=None):

        super(PayGraphic,self).__init__()

        self.main  = main
        self.data  = []
        self.index = 0
        # self.max_price = 0
        self.createWidgets()
        self.createLayout()
        self.createStyle()
        self.createConnections()
        # self.refresh([[0,0],[0,1],[0,2]])
        

    def createWidgets(self):

        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.chart_view = Chart()
        self.chart = QtCharts.QtCharts.QChart()

        self.line_pago = QtCharts.QtCharts.QLineSeries()
        self.line_actual = QtCharts.QtCharts.QLineSeries()

        self.chart.addSeries(self.line_pago)
        self.chart.addSeries(self.line_actual)

        self.chart.setTitle("Payout")
        self.chart.setAnimationOptions(QtCharts.QtCharts.QChart.SeriesAnimations)

        axisX = QtCharts.QtCharts.QValueAxis()
        axisX.setGridLineVisible(False)
        self.chart.addAxis(axisX, QtCore.Qt.AlignBottom)
        self.line_pago.attachAxis(axisX)
        self.line_actual.attachAxis(axisX)

        axisY = QtCharts.QtCharts.QValueAxis()
        self.chart.addAxis(axisY, QtCore.Qt.AlignLeft)
        self.line_pago.attachAxis(axisY)
        self.line_actual.attachAxis(axisY)

        self.chart.legend().setVisible(True)

        self.chart_view.setChart(self.chart)
        self.chart_view.chart().setTheme(QtCharts.QtCharts.QChart.ChartThemeDark)

    def createLayout(self):

        self.main_layout.addWidget(self.chart_view)

    def createStyle(self):

        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.chart_view.setRenderHint(QtGui.QPainter.Antialiasing)

    def createConnections(self):

        self.addValue.connect(self.onAddValue)

    # def refresh(self,data=None):

    #     if data:
    #         self.line.clear()

    #         x = 0
    #         for i in data:
    #             self.line << QtCore.QPointF(x, i[1])

    #             x += 1

    def onAddValue(self,data_pago=None):
        
        # if not data:
        #     self.max_hash = value if self.max_hash < value else self.max_hash
        #     self.index += 1
        #     self.data.append([self.index, value])

        # else:
        #     self.data = data

        self.max_payout = 0

        self.line_pago.clear()
        self.line_actual.clear()
        n = 0
        for i in data_pago:
            self.line_pago << QtCore.QPointF(n,i[1])
            self.line_actual << QtCore.QPointF(n,i[2])
            
            if self.max_payout < i[1]:
                self.max_payout = i[1]
            if self.max_payout < i[2]:
                self.max_payout = i[2] 

            n += 1

        # for i in self.data_actual:
        # n = 0
        #     n += 1
            # if data:
            #     self.max_hash = i[1] if i[1] > self.max_hash else self.max_hash

        # if not data:
        #     self.chart.axisX().setRange(0,self.index)
        #     self.chart.axisY().setRange(0,self.max_hash)
        # else:
        self.chart.axisX().setRange(0,n-1)
        self.chart.axisY().setRange(0,self.max_payout)


if __name__ == '__main__':

    import sys
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    main_ui = Graphic()
    main_ui.show()

    import time,threading

    def test():
        for x in range(100):

            time.sleep(1)
            main_ui.addValue.emit(x)

    worker = threading.Thread(target=test)
    worker.start()

    sys.exit(app.exec_())