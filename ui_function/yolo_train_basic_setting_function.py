from PyQt5 import QtWidgets
from ui_interface.yolo_train_basic_setting import Ui_Form

class Ui_Form_function(Ui_Form):
    def setupfunction(self):
        self.yolo_train_basic_setting_QWidget = QtWidgets.QWidget()
        self.yolo_train_basic_setting_ui = Ui_Form()
        self.yolo_train_basic_setting_ui.setupUi(self.yolo_train_basic_setting_QWidget)