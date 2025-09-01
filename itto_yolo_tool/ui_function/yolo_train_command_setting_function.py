from PyQt5 import QtCore, QtWidgets
from itto_yolo_tool.ui_interface.yolo_train_command_setting import Ui_yolo_train_command_setting_Form

class Ui_yolo_train_command_setting_Form_function(Ui_yolo_train_command_setting_Form):
    def setupfunction(self,yolo_train_command_setting_QWidget):
        self.yolo_train_command_setting_QWidget = yolo_train_command_setting_QWidget

        self.train_command_textEdit_bq = self.train_command_textEdit.toPlainText()

        self.confirm_pushButton.clicked.connect(self.confirm_function)
        self.cancel_pushButton.clicked.connect(self.cancel_function)

    def confirm_function(self):
        self.train_command_textEdit_bq = self.train_command_textEdit.toPlainText()
        
        self.yolo_train_command_setting_QWidget.close()

    def cancel_function(self):
        self.train_command_textEdit.setPlainText(self.train_command_textEdit_bq)
        
        self.yolo_train_command_setting_QWidget.close()

        

if __name__ == "__main__":
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    QWidget = QtWidgets.QWidget()
    ui = Ui_yolo_train_command_setting_Form()
    ui.setupUi(QWidget)
    QWidget.show()
    sys.exit(app.exec_())