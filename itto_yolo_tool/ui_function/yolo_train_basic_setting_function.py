from PyQt5 import QtCore, QtWidgets
from itto_yolo_tool.ui_interface.yolo_train_basic_setting import Ui_yolo_train_basic_setting_Form

class Ui_yolo_train_basic_setting_Form_function(Ui_yolo_train_basic_setting_Form):
    def setupfunction(self,yolo_train_basic_setting_QWidget):
        self.yolo_train_basic_setting_QWidget = yolo_train_basic_setting_QWidget

        self.train_model_comboBox_bq = self.train_model_comboBox.currentText()
        self.train_epochs_comboBox_bq = self.train_epochs_comboBox.currentText()
        self.train_patience_comboBox_bq = self.train_patience_comboBox.currentText()
        self.train_device_comboBox_bq = self.train_device_comboBox.currentText()
        self.train_task_comboBox_bq = self.train_task_comboBox.currentText()

        self.confirm_pushButton.clicked.connect(self.confirm_function)
        self.cancel_pushButton.clicked.connect(self.cancel_function)

    def confirm_function(self):
        self.train_model_comboBox_bq = self.train_model_comboBox.currentText()
        self.train_epochs_comboBox_bq = self.train_epochs_comboBox.currentText()
        self.train_patience_comboBox_bq = self.train_patience_comboBox.currentText()
        self.train_device_comboBox_bq = self.train_device_comboBox.currentText()
        self.train_task_comboBox_bq = self.train_task_comboBox.currentText()

        self.yolo_train_basic_setting_QWidget.close()

    def cancel_function(self):
        self.train_model_comboBox.setCurrentText(self.train_model_comboBox_bq)
        self.train_epochs_comboBox.setCurrentText(self.train_epochs_comboBox_bq)
        self.train_patience_comboBox.setCurrentText(self.train_patience_comboBox_bq)
        self.train_device_comboBox.setCurrentText(self.train_device_comboBox_bq)
        self.train_task_comboBox.setCurrentText(self.train_task_comboBox_bq)
        
        self.yolo_train_basic_setting_QWidget.close()

        

if __name__ == "__main__":
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    QWidget = QtWidgets.QWidget()
    ui = Ui_yolo_train_basic_setting_Form()
    ui.setupUi(QWidget)
    QWidget.show()
    sys.exit(app.exec_())