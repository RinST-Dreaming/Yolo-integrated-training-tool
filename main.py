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
        
        # 初始化时加载默认翻译
        self.load_translation(self.current_language)
        
    def setup_language_switch(self):
        # 假设界面中有一个名为languageComboBox的组合框用于选择语言
        if hasattr(self.ui, 'languageComboBox'):
            self.ui.languageComboBox.currentTextChanged.connect(self.change_language)
    
    def load_translation(self, language_code):
        """加载指定语言的翻译文件"""
        # 移除旧的翻译
        QtWidgets.QApplication.removeTranslator(self.translator)
        
        # 构建翻译文件路径
        translation_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'translations')
        
        if language_code == "zh_CN":
            translation_file = 'zh_CN.qm'
        else:  # English
            translation_file = 'en.qm'  # 注意：通常英文翻译文件是 en.qm，而不是 en_US.qm
            
        # 完整的文件路径
        full_path = os.path.join(translation_dir, translation_file)
        
        print(f"尝试加载翻译文件: {full_path}")
        
        # 检查文件是否存在
        if not os.path.exists(full_path):
            print(f"翻译文件不存在: {full_path}")
            return False
        
        # 加载翻译文件
        if self.translator.load(full_path):
            QtWidgets.QApplication.installTranslator(self.translator)
            self.current_language = language_code
            print(f"已加载 {language_code} 翻译文件")
            
            # 重新翻译界面
            self.ui.retranslateUi(self)
            return True
        else:
            print(f"无法加载 {language_code} 翻译文件")
            return False
        
    def change_language(self, language_text):
        """根据用户选择的语言文本切换语言"""
        if language_text == "中文":
            self.load_translation("zh_CN")
        else:  # English
            self.load_translation("en")

if __name__ == "__main__":
    # 添加调试代码
    translation_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'translations')
    print(f"翻译文件目录: {translation_dir}")
    print(f"中文翻译文件存在: {os.path.exists(os.path.join(translation_dir, 'zh_CN.qm'))}")
    print(f"英文翻译文件存在: {os.path.exists(os.path.join(translation_dir, 'en.qm'))}")
    
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())