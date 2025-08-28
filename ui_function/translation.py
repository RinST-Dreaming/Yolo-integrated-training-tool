from PyQt5 import QtCore, QtWidgets
import os
import sys

from ui_interface.main_menu import Ui_MainWindow
from ui_interface.yolo_train_basic_setting import Ui_yolo_train_basic_setting_Form
from ui_interface.yolo_train_command_setting import Ui_yolo_train_command_setting_Form


class Ui_trainslation(Ui_MainWindow, Ui_yolo_train_basic_setting_Form, Ui_yolo_train_command_setting_Form):
    #-------------------------------------翻译功能配置---------------------------------------------------
    def setup_translation(self):
        self.Ui_MainWindow = Ui_MainWindow()
        self.Ui_yolo_train_basic_setting_Form = Ui_yolo_train_basic_setting_Form()
        self.Ui_yolo_train_command_setting_Form = Ui_yolo_train_command_setting_Form()
        self.actionEnglish.triggered.connect(lambda: self.load_translation("en"))
        self.actionChinese.triggered.connect(lambda: self.load_translation("zh_CN"))

        # 初始化翻译器
        self.translator = QtCore.QTranslator()
        self.current_language = "zh_CN"  # 默认中文
        
        # 初始化时加载默认翻译
        self.load_translation(self.current_language)

    def load_translation(self, language_code):
        """加载指定语言的翻译文件"""
        # 移除旧的翻译
        QtWidgets.QApplication.removeTranslator(self.translator)
        
        # 获取文件所在目录
        file_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        translation_dir = os.path.join(file_dir, 'translations')
        
        # 确保翻译目录存在
        if not os.path.exists(translation_dir):
            self.information_update("翻译目录不存在！\n")
            return
        
        if language_code == "zh_CN":
            translation_file = 'zh_CN.qm'
        else:  # English
            translation_file = 'en.qm'

        # 完整的文件路径
        full_path = os.path.join(translation_dir, translation_file)
        
        # 加载翻译文件
        if self.translator.load(full_path):
            QtWidgets.QApplication.installTranslator(self.translator)
            self.current_language = language_code
            self.information_update(f"已加载 {language_code} 翻译文件\n")
            
            # 重新翻译界面
            self.retranslate_ui()
            return True
        else:
            self.information_update(f"无法加载 {language_code} 翻译文件\n")
            return False
    
    def retranslate_ui(self):
        """重新翻译界面"""
        # 对实际的窗口实例调用 retranslateUi，而不是 UI 类
        self.retranslateUi(self.MainWindow)
        self.yolo_train_basic_setting_ui.retranslateUi(self.yolo_train_basic_setting_window)
        self.yolo_train_command_setting_ui.retranslateUi(self.yolo_train_command_setting_window)