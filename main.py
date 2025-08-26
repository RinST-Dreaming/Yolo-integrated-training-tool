from PyQt5 import QtCore, QtWidgets
from ui_function.main_menu_function import Ui_MainWindow_function
import os
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_function()
        self.ui.setupUi(self)
        self.ui.setupfunction(self)
        
        # 初始化翻译器
        self.translator = QtCore.QTranslator()
        self.current_language = "zh_CN"  # 默认中文
        
        # 设置语言切换信号
        self.setup_language_switch()
        
    def setup_language_switch(self):
        # 假设界面中有一个名为languageComboBox的组合框用于选择语言
        if hasattr(self.ui, 'languageComboBox'):
            self.ui.languageComboBox.currentTextChanged.connect(self.change_language)
        
    def change_language(self, language):
        # 移除旧的翻译
        QtWidgets.QApplication.removeTranslator(self.translator)
        
        # 根据选择加载新的翻译
        translation_dir = os.path.join(os.path.dirname(__file__), 'translations')
        if language == "中文":
            translation_file = 'zh_CN.qm'
            self.current_language = "zh_CN"
        else:  # English
            translation_file = 'en_US.qm'
            self.current_language = "en_US"
            
        if self.translator.load(translation_file, translation_dir):
            QtWidgets.QApplication.installTranslator(self.translator)
            
        # 重新翻译界面
        self.ui.retranslateUi(self)

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())