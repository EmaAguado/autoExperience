from PySide2 import QtWidgets, QtGui, QtCore
import operator

class SheetTableModel(QtCore.QAbstractTableModel):


    def __init__(self, parent, headers = [], data = [[]]):
        QtCore.QAbstractTableModel.__init__(self, parent)

        self.parent = parent
        self.header = headers
        self._data = data
        self.align_to_center = True
        self.update()

    def update(self,data=None):
        """
        Clean & Regenerate Table with new values (self._data)

        """
        if data:
            self._data = data
        self.beginResetModel()
        self.endResetModel()

    def data(self, index, role):

        if not index.isValid():

            return None

        else:
            
            try:value = self._data[index.row()][index.column()]
            except:value = None

            if role == QtCore.Qt.DisplayRole:

                return value

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        try: return len(self._data[0])
        except: return 0

    def flags(self, index):

        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled 

    def headerData(self, col, orientation, role):
        try:
            if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                return self.header[col]
            elif orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole and self.verticalHeader_enable:
                return col+1
            return None
        except: return None

    def sort(self, col, order):

        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self._data = sorted(self._data,
                             key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self._data.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))

    def clear(self):

        empty = []
        self._data =  [[empty.append(None) for x in range(self.rowCount(None)+1)]]
        self.update()