from PySide2 import QtCore, QtGui, QtWidgets,QtXml
from ui import main

__owner__   = "Minvervus"
__version__ = "alpha 0.0.1"

if __name__ == '__main__':

    import sys
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(main.styleS.autoStyle(color=[76, 65, 97]))

    main_ui = main.UI()
    main_ui.show()

    sys.exit(app.exec_())