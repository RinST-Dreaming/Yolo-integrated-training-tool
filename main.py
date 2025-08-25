from PyQt5 import QtCore, QtGui, QtWidgets
from ui_function.main_menu_function import Ui_MainWindow_function

if __name__ == "__main__":
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_function()
    ui.setupUi(MainWindow)
    ui.setupfunction()
    MainWindow.show()
    sys.exit(app.exec_())