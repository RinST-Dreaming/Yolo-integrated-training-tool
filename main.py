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
        
        # 加载默认翻译
        self.load_translation(self.current_language)
        
    def setup_language_switch(self):
        # 假设界面中有一个名为languageComboBox的组合框用于选择语言
        if hasattr(self.ui, 'languageComboBox'):
            self.ui.languageComboBox.currentTextChanged.connect(self.change_language)
        
    def change_language(self, language):
        # 移除旧的翻译
        QtWidgets.QApplication.removeTranslator(self.translator)
        
        # 根据选择加载新的翻译
        if language == self.tr("中文"):
            self.load_translation("zh_CN")
        else:  # English
            self.load_translation("en_US")
            
        # 重新翻译界面
        self.ui.retranslateUi(self)
        
    def load_translation(self, language_code):
        # 获取翻译文件路径
        translation_dir = os.path.join(os.path.dirname(__file__), 'translations')
        translation_file = f'{language_code}.qm'
        translation_path = os.path.join(translation_dir, translation_file)
        
        # 加载翻译文件
        if os.path.exists(translation_path):
            if self.translator.load(translation_path):
                QtWidgets.QApplication.installTranslator(self.translator)
                self.current_language = language_code
            else:
                print(self.tr("加载翻译文件失败: {file}").format(file=translation_path))
        else:
            print(self.tr("翻译文件不存在: {file}").format(file=translation_path))

    def changeEvent(self, event):
        # 处理语言更改事件
        if event.type() == QtCore.QEvent.LanguageChange:
            self.ui.retranslateUi(self)
        super(MainWindow, self).changeEvent(event)

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())