
data = """
QMainWindow::separator {background: red;width: 4px; height: 4px;}
QMainWindow::separator:hover {background: palette(HighLight)} 
QMainWindow::separator:horizontal{image: url(ui/resources/img/splitter.png);}
QMainWindow::separator:vertical{image: url(ui/resources/img/splitter_vertical.png);}
QTabBar{background:palette(mid)}
*{font: 12px "Consolas"}
QLineEdit{font: 12px "Consolas" }
QComboBox{font: 12px "Consolas" }
QSplitter[orientation=\"1\"]::handle{image: url(ui/resources/img/splitter_vertical.png);background:palette(mid);width: 4px; height: 4px;} 
QSplitter[orientation=\"2\"]::handle:horizontal{image: url(ui/resources/img/splitter.png);background:palette(mid);width: 4px; height: 4px;} 
QSplitter::handle:hover{background:palette(HighLight)}
QScrollBar:horizontal { background: rgb(50,50,50); height: 15px; margin: 0px 0px 0 0px;}
QScrollBar::handle:horizontal { background: palette(mid);margin:2px }
QScrollBar::handle:horizontal:hover { background: palette(dark);margin:0px }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {background: None;}
QScrollBar:left-arrow:horizontal:hover{ width: 20px; height: 20px; background: palette(dark);}
QScrollBar::right-arrow:horizontal:hover { width: 20px; height: 20px; background: palette(dark);}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {background: None;}
QScrollBar:vertical { background: rgb(50,50,50); margin: 0px 0px 0px 0px;}
QScrollBar::handle:vertical { background: palette(mid);margin:2px }
QScrollBar::handle:vertical:hover { background: palette(dark);margin:0px }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {background: None;}
QScrollBar:up-arrow:vertical:hover{ width: 20px; height: 20px; background: palette(dark);}
QScrollBar::down-arrow:vertical:hover { width: 20px; height: 20px; background: palette(dark);}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: None;}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {background: None;}
QPushButton{background-color:palette(base);border:none;padding:5px}
QPushButton:hover{background-color:palette(dark);border:none;padding:5px}
QPushButton:checked{background-color:palette(highlight)}
QToolButton{background-color:palette(base);border:none;padding:5px}
QToolButton:hover{background-color:palette(dark);border:none;padding:5px}
QToolButton:checked{background-color:palette(highlight)}
QTreeWidget {show-decoration-selected: 0;selection-background-color: transparent;outline: 0}
QTreeView::item:hover{background-color: palette(Highlight)}
QTreeWidget::item:hover{background-color: palette(Highlight)}
QComboBox{background-color:palette(mid);border: 0px;padding-right:5px;padding-left:5px}
QComboBox:on{background-color:palette(base);border: 0px;padding-right:0px;padding-left:0px}
QComboBox QAbstractItemView{selection-background-color:palette(highlight)}
QComboBox::drop-down {border: 0px;padding-left:5px}
QComboBox::down-arrow {border-image: url(ui/resources/img/arrow_down.png);padding-left:5px;padding-right:5px}
QComboBox:hover{background-color:palette(highlight)}

"""