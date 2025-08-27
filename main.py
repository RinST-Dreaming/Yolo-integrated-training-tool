from PyQt5 import QtCore, QtWidgets
from ui_function.main_menu_function import Ui_MainWindow_function
import os
import sys
import stat

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
    
    def check_file_permissions(self, file_path):
        """检查文件权限"""
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return False
        
        # 检查读取权限
        if not os.access(file_path, os.R_OK):
            print(f"文件没有读取权限: {file_path}")
            
            # 尝试获取当前权限
            current_permissions = stat.S_IMODE(os.lstat(file_path).st_mode)
            print(f"当前文件权限: {oct(current_permissions)}")
            
            # 尝试添加读取权限
            try:
                os.chmod(file_path, current_permissions | stat.S_IREAD)
                print(f"已添加读取权限: {file_path}")
            except Exception as e:
                print(f"无法添加读取权限: {e}")
                return False
        
        return True
    
    def load_translation(self, language_code):
        """加载指定语言的翻译文件"""
        # 移除旧的翻译
        QtWidgets.QApplication.removeTranslator(self.translator)
        
        # 构建翻译文件路径
        base_dir = os.path.dirname(os.path.abspath(__file__))
        translation_dir = os.path.join(base_dir, 'translations')
        
        print(f"基础目录: {base_dir}")
        print(f"翻译目录: {translation_dir}")
        
        # 确保翻译目录存在
        if not os.path.exists(translation_dir):
            print(f"翻译目录不存在: {translation_dir}")
            try:
                os.makedirs(translation_dir, exist_ok=True)
                print(f"已创建翻译目录: {translation_dir}")
            except Exception as e:
                print(f"创建翻译目录失败: {e}")
                return False
        
        if language_code == "zh_CN":
            translation_file = 'zh_CN.qm'
        else:  # English
            translation_file = 'en.qm'
            
        # 完整的文件路径
        full_path = os.path.join(translation_dir, translation_file)
        
        print(f"尝试加载翻译文件: {full_path}")
        
        # 检查文件是否存在和权限
        if not self.check_file_permissions(full_path):
            # 尝试从源代码目录查找 .ts 文件
            ts_file_path = os.path.join(base_dir, f"{language_code}.ts")
            print(f"尝试查找 .ts 文件: {ts_file_path}")
            
            if os.path.exists(ts_file_path):
                print(f"找到 .ts 文件: {ts_file_path}")
                # 检查是否有编译工具
                try:
                    # 尝试使用 lrelease 编译 .ts 文件
                    import subprocess
                    qm_path = os.path.join(translation_dir, translation_file)
                    result = subprocess.run(['lrelease', ts_file_path, '-qm', qm_path], 
                                          capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print(f"成功编译 .ts 文件到: {qm_path}")
                        # 重新检查权限
                        if self.check_file_permissions(qm_path):
                            full_path = qm_path
                        else:
                            return False
                    else:
                        print(f"编译失败: {result.stderr}")
                        return False
                except Exception as e:
                    print(f"无法编译 .ts 文件: {e}")
                    return False
            else:
                print(f".ts 文件也不存在: {ts_file_path}")
                return False
        
        # 加载翻译文件
        if self.translator.load(full_path):
            QtWidgets.QApplication.installTranslator(self.translator)
            self.current_language = language_code
            print(f"已加载 {language_code} 翻译文件")
            
            # 重新翻译界面
            self.retranslate_ui()
            return True
        else:
            print(f"无法加载 {language_code} 翻译文件")
            return False
    
    def retranslate_ui(self):
        """重新翻译界面"""
        # 保存当前状态
        current_states = {}
        
        # 保存标签页状态
        if hasattr(self.ui, 'tabWidget'):
            current_states['tab_index'] = self.ui.tabWidget.currentIndex()
        
        # 保存文本输入框内容
        text_edits = self.findChildren(QtWidgets.QTextEdit)
        for i, text_edit in enumerate(text_edits):
            current_states[f'text_edit_{i}'] = text_edit.toPlainText()
        
        # 保存复选框状态
        check_boxes = self.findChildren(QtWidgets.QCheckBox)
        for i, check_box in enumerate(check_boxes):
            current_states[f'check_box_{i}'] = check_box.isChecked()
        
        # 保存下拉框状态
        combo_boxes = self.findChildren(QtWidgets.QComboBox)
        for i, combo_box in enumerate(combo_boxes):
            current_states[f'combo_box_{i}'] = combo_box.currentIndex()
        
        # 重新设置UI
        self.ui = Ui_MainWindow_function()
        self.ui.setupUi(self)
        self.ui.setupfunction(self)
        
        # 恢复状态
        if 'tab_index' in current_states and hasattr(self.ui, 'tabWidget'):
            self.ui.tabWidget.setCurrentIndex(current_states['tab_index'])
        
        # 恢复文本输入框内容
        text_edits = self.findChildren(QtWidgets.QTextEdit)
        for i, text_edit in enumerate(text_edits):
            if f'text_edit_{i}' in current_states:
                text_edit.setPlainText(current_states[f'text_edit_{i}'])
        
        # 恢复复选框状态
        check_boxes = self.findChildren(QtWidgets.QCheckBox)
        for i, check_box in enumerate(check_boxes):
            if f'check_box_{i}' in current_states:
                check_box.setChecked(current_states[f'check_box_{i}'])
        
        # 恢复下拉框状态
        combo_boxes = self.findChildren(QtWidgets.QComboBox)
        for i, combo_box in enumerate(combo_boxes):
            if f'combo_box_{i}' in current_states:
                combo_box.setCurrentIndex(current_states[f'combo_box_{i}'])
        
        # 重新设置语言切换信号
        self.setup_language_switch()
        
    def change_language(self, language_text):
        """根据用户选择的语言文本切换语言"""
        if language_text == "中文":
            self.load_translation("zh_CN")
        else:  # English
            self.load_translation("en")

from PyQt5 import QtCore, QtWidgets
from ui_interface.main_menu import MainWindow
import sys

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    
    # 直接创建 main_menu.py 中的 MainWindow
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())