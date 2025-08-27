from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from ultralytics import YOLO
from pathlib import Path
import sys
import cv2
import subprocess
import random
import os
import threading
import stat

from ui_interface.main_menu import Ui_MainWindow
from ui_function.yolo_train_basic_setting_function import Ui_yolo_train_basic_setting_Form_function
from ui_function.yolo_train_command_setting_function import Ui_yolo_train_command_setting_Form_function
from tools import xml_to_txt
from tools import xml_convert_examine

class ProgressSignal(QtCore.QObject):
    message_updated = QtCore.pyqtSignal(str)   # 消息文本
    progress_updated = QtCore.pyqtSignal(int)  # 进度百分比
    train_button_status = QtCore.pyqtSignal(bool)
    

class Ui_MainWindow_function(Ui_MainWindow):
    #-------------------------------------初始化配置---------------------------------------------------
    def setupfunction(self, MainWindow):
        self.MainWindow = MainWindow
        self.browse_pushButton.clicked.connect(self.browse_workspace_directory_function)
        self.subfolder_create_pushButton.clicked.connect(self.subfolder_create_function)
        self.yaml_create_pushButton.clicked.connect(self.yaml_create_function)
        self.ramdom_classify_pushButton.clicked.connect(self.ramdom_classify_function)
        self.xml_to_txt_pushButton.clicked.connect(self.xml_to_txt_function)
        self.xml_convert_examine_pushButton.clicked.connect(self.xml_convert_examine_function)
        self.rolabelimg_pushButton.clicked.connect(self.rolabelimg_function)
        self.yolo_train_basic_setting_pushButton.clicked.connect(self.Ui_yolo_train_basic_setting_function)
        self.yolo_train_command_setting_pushButton.clicked.connect(self.Ui_yolo_train_command_setting_function)
        self.yolo_train_start_pushButton.clicked.connect(self.yolo_train_start_function)
        self.yolo_test_start_pushButton.clicked.connect(self.yolo_test_start_function)

        self.yolo_train_basic_setting_window = QtWidgets.QWidget()
        self.yolo_train_basic_setting_ui = Ui_yolo_train_basic_setting_Form_function()
        self.yolo_train_basic_setting_ui.setupUi(self.yolo_train_basic_setting_window)
        self.yolo_train_basic_setting_ui.setupfunction(self.yolo_train_basic_setting_window)

        self.yolo_train_command_setting_window = QtWidgets.QWidget()
        self.yolo_train_command_setting_ui = Ui_yolo_train_command_setting_Form_function()
        self.yolo_train_command_setting_ui.setupUi(self.yolo_train_command_setting_window)
        self.yolo_train_command_setting_ui.setupfunction(self.yolo_train_command_setting_window)

        self.yolo_train_cmd=self.yolo_train_command_setting_ui.train_command_textEdit.toPlainText()

        self.progress_signal = ProgressSignal()
        self.progress_signal.message_updated.connect(self.task_onrunning_textBrowser.setPlainText)
        self.progress_signal.progress_updated.connect(self.progress_update)
        self.progress_signal.train_button_status.connect(self.train_button_status_update)

        self.ui_translator=Ui_MainWindow()
        self.actionEnglish.triggered.connect(lambda: self.load_translation("en"))
        self.actionChinese.triggered.connect(lambda: self.load_translation("zh_CN"))
        # 初始化翻译器
        self.translator = QtCore.QTranslator()
        self.current_language = "zh_CN"  # 默认中文
        
        # 初始化时加载默认翻译
        self.load_translation(self.current_language)

    #-------------------------------------信号配置---------------------------------------------------
    def information_update(self,information):
        self.information_textBrowser.moveCursor(QtGui.QTextCursor.End)
        self.information_textBrowser.insertPlainText(information)
        self.information_textBrowser.ensureCursorVisible()

    def progress_update(self,progress):
        self.progressBar.setProperty("value", progress)

    def train_button_status_update(self,status):
        self.yolo_train_start_pushButton.setEnabled(status)
        self.yolo_train_start_pushButton.setText("yolo模型训练完成(√)")

#-------------------------------------信号配置---------------------------------------------------
    def information_update(self,information):
        self.information_textBrowser.moveCursor(QtGui.QTextCursor.End)
        self.information_textBrowser.insertPlainText(information)
        self.information_textBrowser.ensureCursorVisible()

    def progress_update(self,progress):
        self.progressBar.setProperty("value", progress)

    def train_button_status_update(self,status):
        self.yolo_train_start_pushButton.setEnabled(status)
        self.yolo_train_start_pushButton.setText("yolo模型训练完成(√)")

    #-------------------------------------翻译功能配置---------------------------------------------------
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
        # 保存当前状态
        current_states = {}
        
        # 保存文本输入框内容
        text_edits = self.MainWindow.findChildren(QtWidgets.QTextEdit)
        for i, text_edit in enumerate(text_edits):
            current_states[f'text_edit_{i}'] = text_edit.toPlainText()
        
        # 保存复选框状态
        check_boxes = self.MainWindow.findChildren(QtWidgets.QCheckBox)
        for i, check_box in enumerate(check_boxes):
            current_states[f'check_box_{i}'] = check_box.isChecked()
        
        # 保存下拉框状态
        combo_boxes = self.MainWindow.findChildren(QtWidgets.QComboBox)
        for i, combo_box in enumerate(combo_boxes):
            current_states[f'combo_box_{i}'] = combo_box.currentIndex()
        
        # 保存spinbox状态
        spin_boxes = self.MainWindow.findChildren(QtWidgets.QSpinBox)
        for i, spin_box in enumerate(spin_boxes):
            current_states[f'spin_box_{i}'] = spin_box.value()
        
        # 重新调用父类的retranslateUi方法
        super().retranslateUi(self.MainWindow)
        
        # 恢复状态
        # 恢复文本输入框内容
        text_edits = self.MainWindow.findChildren(QtWidgets.QTextEdit)
        for i, text_edit in enumerate(text_edits):
            if f'text_edit_{i}' in current_states:
                text_edit.setPlainText(current_states[f'text_edit_{i}'])
        
        # 恢复复选框状态
        check_boxes = self.MainWindow.findChildren(QtWidgets.QCheckBox)
        for i, check_box in enumerate(check_boxes):
            if f'check_box_{i}' in current_states:
                check_box.setChecked(current_states[f'check_box_{i}'])
        
        # 恢复下拉框状态
        combo_boxes = self.MainWindow.findChildren(QtWidgets.QComboBox)
        for i, combo_box in enumerate(combo_boxes):
            if f'combo_box_{i}' in current_states:
                combo_box.setCurrentIndex(current_states[f'combo_box_{i}'])
        
        # 恢复spinbox状态
        spin_boxes = self.MainWindow.findChildren(QtWidgets.QSpinBox)
        for i, spin_box in enumerate(spin_boxes):
            if f'spin_box_{i}' in current_states:
                spin_box.setValue(current_states[f'spin_box_{i}'])

    #-------------------------------------主要功能配置---------------------------------------------------
    def browse_workspace_directory_function(self):
        self.task_onrunning_textBrowser.setText("设置工作区路径")
        self.progressBar.setProperty("value", 0)

        """浏览并选择工作目录"""
        # 弹出目录选择对话框
        directory = QFileDialog.getExistingDirectory(
            None,  # 父窗口
            "选择工作目录",  # 对话框标题
            "",  # 默认起始目录（空字符串表示当前目录）
            QFileDialog.ShowDirsOnly  # 只显示目录
        )
        
        # 如果用户选择了目录（没有点击取消）
        if directory:
            # 将选择的目录路径设置到文本编辑框中
            self.workspace_textEdit.setPlainText(directory)
            self.information_update(f"成功设置工作目录:{directory}\n")
            self.progressBar.setProperty("value", 100)

    def subfolder_create_function(self):
        self.task_onrunning_textBrowser.setText("创建工作区目录")
        self.progressBar.setProperty("value", 0)

        if self.workspace_textEdit.toPlainText():
            if os.path.exists(self.workspace_textEdit.toPlainText()):
                if(not os.path.exists(self.workspace_textEdit.toPlainText()+"/train/images")):
                    os.makedirs(self.workspace_textEdit.toPlainText()+"/train/images")
                self.progressBar.setProperty("value", 10)

                if(not os.path.exists(self.workspace_textEdit.toPlainText()+"/train/labels")):
                    os.makedirs(self.workspace_textEdit.toPlainText()+"/train/labels")
                self.progressBar.setProperty("value", 20)

                if(not os.path.exists(self.workspace_textEdit.toPlainText()+"/train/labels_xml")):
                    os.makedirs(self.workspace_textEdit.toPlainText()+"/train/labels_xml")
                self.progressBar.setProperty("value", 25)

                if(not os.path.exists(self.workspace_textEdit.toPlainText()+"/val/images")):
                    os.makedirs(self.workspace_textEdit.toPlainText()+"/val/images")
                self.progressBar.setProperty("value", 30)

                if(not os.path.exists(self.workspace_textEdit.toPlainText()+"/val/labels")):
                    os.makedirs(self.workspace_textEdit.toPlainText()+"/val/labels")
                self.progressBar.setProperty("value", 40)

                if(not os.path.exists(self.workspace_textEdit.toPlainText()+"/val/labels_xml")):
                    os.makedirs(self.workspace_textEdit.toPlainText()+"/val/labels_xml")
                self.progressBar.setProperty("value", 50)

                if(not os.path.exists(self.workspace_textEdit.toPlainText()+"/test/images")):
                    os.makedirs(self.workspace_textEdit.toPlainText()+"/test/images")
                self.progressBar.setProperty("value", 60)

                if(not os.path.exists(self.workspace_textEdit.toPlainText()+"/test/labels")):
                    os.makedirs(self.workspace_textEdit.toPlainText()+"/test/labels")
                self.progressBar.setProperty("value", 70)

                if(not os.path.exists(self.workspace_textEdit.toPlainText()+"/test/labels_xml")):
                    os.makedirs(self.workspace_textEdit.toPlainText()+"/test/labels_xml")
                self.progressBar.setProperty("value", 75)

                if(not os.path.exists(self.workspace_textEdit.toPlainText()+"/files_waiting_for_classify/images")):
                    os.makedirs(self.workspace_textEdit.toPlainText()+"/files_waiting_for_classify/images")
                self.progressBar.setProperty("value", 80)

                if(not os.path.exists(self.workspace_textEdit.toPlainText()+"/files_waiting_for_classify/labels")):
                    os.makedirs(self.workspace_textEdit.toPlainText()+"/files_waiting_for_classify/labels")
                self.progressBar.setProperty("value", 90)

                if(not os.path.exists(self.workspace_textEdit.toPlainText()+"/files_waiting_for_classify/labels_xml")):
                    os.makedirs(self.workspace_textEdit.toPlainText()+"/files_waiting_for_classify/labels_xml")
                self.progressBar.setProperty("value", 100)

                self.information_update(f"成功创建子文件夹\n")
            else:
                self.information_update(f"无效的工作目录\n")
        else:
            self.information_update(f"在创建子文件夹前请先选择工作目录\n")

    def yaml_create_function(self):
        self.task_onrunning_textBrowser.setText("创建yolo训练yaml配置文件")
        self.progressBar.setProperty("value", 0)

        if self.workspace_textEdit.toPlainText():
            if os.path.exists(self.workspace_textEdit.toPlainText()):
                if self.target_adding_textEdit.toPlainText():
                    names="','".join(list(str(self.target_adding_textEdit.toPlainText()).splitlines()))
                    yaml_content=[
                        f"path: {self.workspace_textEdit.toPlainText()}",
                        f"train: train/images",
                        f"val: val/images",
                        f"nc: {len(str(self.target_adding_textEdit.toPlainText()).splitlines())}",
                        f"names: ['{names}']"
                    ]
                    self.progressBar.setProperty("value", 50)
                    with open(self.workspace_textEdit.toPlainText()+"/dataset.yaml", 'w', encoding='utf-8') as file:
                        file.write('\n'.join(yaml_content))
                    self.information_update(f"yaml文件创建成功\n")
                    self.progressBar.setProperty("value", 100)
                else:
                    self.information_update(f"在创建yaml配置文件前,你需要先添加标注名,用回车隔开\n")
            else:
                self.information_update(f"无效的工作目录\n")
        else:
            self.information_update(f"在创建yaml文件前请先选择工作目录\n")


    def ramdom_classify_function(self):
        self.task_onrunning_textBrowser.setText("对数据集进行随机分配")
        self.progressBar.setProperty("value", 0)
        count=0

        # 支持的图片扩展名
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}

        rand_value_1 = int(self.classify_train_spinBox.text())
        rand_value_2 = int(self.classify_val_spinBox.text())
        rand_value_3 = int(self.classify_test_spinBox.text())
        
        if(rand_value_1 + rand_value_2 + rand_value_3 != 100):
            self.information_update(f"无效的随机分配概率值,三个值的和不为100\n")
            return

        divide_line_1 = rand_value_1/100
        divide_line_2 = (rand_value_1+rand_value_2)/100
        

        if os.path.exists(self.workspace_textEdit.toPlainText()):
            all_count=len(os.listdir(self.workspace_textEdit.toPlainText()+"/files_waiting_for_classify/images"))
            if os.path.exists(self.workspace_textEdit.toPlainText()+"/files_waiting_for_classify"):
                for image_file in os.listdir(self.workspace_textEdit.toPlainText()+"/files_waiting_for_classify/images"):

                    image_file_suffix = Path(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/images/{image_file}").suffix
                    image_file_name = image_file[:-len(image_file_suffix)]

                    if(image_file_suffix in image_extensions):

                        if(random.random()<=divide_line_1):
                            Path(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/images/{image_file}").rename(
                                self.workspace_textEdit.toPlainText()+f"/train/images/{image_file}")
                            if os.path.exists(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels/{image_file_name}.txt"):
                                Path(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels/{image_file_name}.txt").rename(
                                    self.workspace_textEdit.toPlainText()+f"/train/labels/{image_file_name}.txt")
                            if os.path.exists(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels_xml/{image_file_name}.xml"):
                                Path(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels_xml/{image_file_name}.xml").rename(
                                    self.workspace_textEdit.toPlainText()+f"/train/labels_xml/{image_file_name}.xml")
                                
                        elif(random.random()<=divide_line_2):
                            Path(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/images/{image_file}").rename(
                                self.workspace_textEdit.toPlainText()+f"/val/images/{image_file}")
                            if os.path.exists(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels/{image_file_name}.txt"):
                                Path(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels/{image_file_name}.txt").rename(
                                    self.workspace_textEdit.toPlainText()+f"/val/labels/{image_file_name}.txt")
                            if os.path.exists(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels_xml/{image_file_name}.xml"):
                                Path(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels_xml/{image_file_name}.xml").rename(
                                    self.workspace_textEdit.toPlainText()+f"/val/labels_xml/{image_file_name}.xml")

                        else:
                            Path(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/images/{image_file}").rename(
                                self.workspace_textEdit.toPlainText()+f"/test/images/{image_file}")
                            if os.path.exists(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels/{image_file_name}.txt"):
                                Path(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels/{image_file_name}.txt").rename(
                                    self.workspace_textEdit.toPlainText()+f"/test/labels/{image_file_name}.txt")
                            if os.path.exists(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels_xml/{image_file_name}.xml"):
                                Path(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels_xml/{image_file_name}.xml").rename(
                                    self.workspace_textEdit.toPlainText()+f"/test/labels_xml/{image_file_name}.xml")
                                
                    count+=1
                    self.progressBar.setProperty("value", count/all_count*100)
            else:
                self.information_update(f"未检测到子文件夹\n")
                return
        else:
            self.information_update(f"无效的工作目录\n")
            return
        
        self.information_update(f"文件随机分配命令执行完成\n")
        self.progressBar.setProperty("value", 100)

    def xml_to_txt_function(self):
        self.task_onrunning_textBrowser.setText("转换标注xml文件为txt文件")
        self.progressBar.setProperty("value", 0)
        count=0
        
        # 支持的图片扩展名
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}

        if os.path.exists(self.workspace_textEdit.toPlainText()):
            all_count=len(os.listdir(self.workspace_textEdit.toPlainText()+"/files_waiting_for_classify/images")+
                      os.listdir(self.workspace_textEdit.toPlainText()+"/train/images")+
                      os.listdir(self.workspace_textEdit.toPlainText()+"/val/images")+
                      os.listdir(self.workspace_textEdit.toPlainText()+"/test/images"))

            if self.target_adding_textEdit.toPlainText():

                self.information_update(f"开始进行files_waiting_for_classify文件夹内的xml标注转换\n")
                for image_file in os.listdir(self.workspace_textEdit.toPlainText()+"/files_waiting_for_classify/images"):
                    image_file_suffix = Path(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/images/{image_file}").suffix
                    image_file_name = image_file[:-len(image_file_suffix)]
                    if(image_file_suffix in image_extensions):
                        if(os.path.exists(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels_xml/{image_file_name}.xml")):
                            xml_to_txt.function(xml_path=self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels_xml/{image_file_name}.xml",
                                    txt_path=self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels/{image_file_name}.txt",
                                    classnames=list(str(self.target_adding_textEdit.toPlainText()).splitlines()))
                        elif(not os.path.exists(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels/{image_file_name}.txt")):
                            xml_to_txt.function(xml_path=None,
                                    txt_path=self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels/{image_file_name}.txt",
                                    classnames=list(str(self.target_adding_textEdit.toPlainText()).splitlines()))
                    
                    count+=1
                    self.progressBar.setProperty("value", count/all_count*100)
                            
                self.information_update(f"开始进行train文件夹内的xml标注转换\n")
                for image_file in os.listdir(self.workspace_textEdit.toPlainText()+"/train/images"):
                    image_file_suffix = Path(self.workspace_textEdit.toPlainText()+f"/train/images/{image_file}").suffix
                    image_file_name = image_file[:-len(image_file_suffix)]
                    if(image_file_suffix in image_extensions):
                        if(os.path.exists(self.workspace_textEdit.toPlainText()+f"/train/labels_xml/{image_file_name}.xml")):
                            xml_to_txt.function(xml_path=self.workspace_textEdit.toPlainText()+f"/train/labels_xml/{image_file_name}.xml",
                                    txt_path=self.workspace_textEdit.toPlainText()+f"/train/labels/{image_file_name}.txt",
                                    classnames=list(str(self.target_adding_textEdit.toPlainText()).splitlines()))
                        elif(not os.path.exists(self.workspace_textEdit.toPlainText()+f"/train/labels/{image_file_name}.txt")):
                            xml_to_txt.function(xml_path=None,
                                    txt_path=self.workspace_textEdit.toPlainText()+f"/train/labels/{image_file_name}.txt",
                                    classnames=list(str(self.target_adding_textEdit.toPlainText()).splitlines()))
                            
                    count+=1
                    self.progressBar.setProperty("value", count/all_count*100)
                            
                self.information_update(f"开始进行val文件夹内的xml标注转换\n")
                for image_file in os.listdir(self.workspace_textEdit.toPlainText()+"/val/images"):
                    image_file_suffix = Path(self.workspace_textEdit.toPlainText()+f"/val/images/{image_file}").suffix
                    image_file_name = image_file[:-len(image_file_suffix)]
                    if(image_file_suffix in image_extensions):
                        if(os.path.exists(self.workspace_textEdit.toPlainText()+f"/val/labels_xml/{image_file_name}.xml")):
                            xml_to_txt.function(xml_path=self.workspace_textEdit.toPlainText()+f"/val/labels_xml/{image_file_name}.xml",
                                    txt_path=self.workspace_textEdit.toPlainText()+f"/val/labels/{image_file_name}.txt",
                                    classnames=list(str(self.target_adding_textEdit.toPlainText()).splitlines()))
                        elif(not os.path.exists(self.workspace_textEdit.toPlainText()+f"/val/labels/{image_file_name}.txt")):
                            xml_to_txt.function(xml_path=None,
                                    txt_path=self.workspace_textEdit.toPlainText()+f"/val/labels/{image_file_name}.txt",
                                    classnames=list(str(self.target_adding_textEdit.toPlainText()).splitlines()))
                    count+=1
                    self.progressBar.setProperty("value", count/all_count*100)
                            
                self.information_update(f"开始进行test文件夹内的xml标注转换\n")
                for image_file in os.listdir(self.workspace_textEdit.toPlainText()+"/test/images"):
                    image_file_suffix = Path(self.workspace_textEdit.toPlainText()+f"/test/images/{image_file}").suffix
                    image_file_name = image_file[:-len(image_file_suffix)]
                    if(image_file_suffix in image_extensions):
                        if(os.path.exists(self.workspace_textEdit.toPlainText()+f"/test/labels_xml/{image_file_name}.xml")):
                            xml_to_txt.function(xml_path=self.workspace_textEdit.toPlainText()+f"/test/labels_xml/{image_file_name}.xml",
                                    txt_path=self.workspace_textEdit.toPlainText()+f"/test/labels/{image_file_name}.txt",
                                    classnames=list(str(self.target_adding_textEdit.toPlainText()).splitlines()))
                        elif(not os.path.exists(self.workspace_textEdit.toPlainText()+f"/test/labels/{image_file_name}.txt")):
                            xml_to_txt.function(xml_path=None,
                                    txt_path=self.workspace_textEdit.toPlainText()+f"/test/labels/{image_file_name}.txt",
                                    classnames=list(str(self.target_adding_textEdit.toPlainText()).splitlines()))
                            
                    count+=1
                    self.progressBar.setProperty("value", count/all_count*100)
                
                self.information_update(f"xml_to_txt命令执行完成\n")
                self.progressBar.setProperty("value", 100)
            else:
                self.information_update(f"在创建txt文件前,你需要先添加标注名,用回车隔开\n")
        else:
            self.information_update(f"无效的工作目录\n")

    def xml_convert_examine_function(self):
        self.task_onrunning_textBrowser.setText("进行txt文件转换正确性检验")
        self.progressBar.setProperty("value", 0)
        count=0

        # 支持的图片扩展名
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}

        if not self.target_adding_textEdit.toPlainText():
            self.information_update(f"在进行模型检验之前,推荐先添加标注名,用回车隔开\n")
        
        if os.path.exists(self.workspace_textEdit.toPlainText()):

            all_count=len(os.listdir(self.workspace_textEdit.toPlainText()+"/files_waiting_for_classify/images")+
                      os.listdir(self.workspace_textEdit.toPlainText()+"/train/images")+
                      os.listdir(self.workspace_textEdit.toPlainText()+"/val/images")+
                      os.listdir(self.workspace_textEdit.toPlainText()+"/test/images"))

            self.information_update(f"开始进行files_waiting_for_classify文件夹内的图片标注检验\n")
            for image_file in os.listdir(self.workspace_textEdit.toPlainText()+"/files_waiting_for_classify/images"):
                image_file_suffix = Path(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/images/{image_file}").suffix
                image_file_name = image_file[:-len(image_file_suffix)]
                if(image_file_suffix in image_extensions):
                    if(os.path.exists(self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels/{image_file_name}.txt")):
                        if not xml_convert_examine.function(pic_path=self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/images/{image_file}",
                                txt_path=self.workspace_textEdit.toPlainText()+f"/files_waiting_for_classify/labels/{image_file_name}.txt",
                                classnames=list(str(self.target_adding_textEdit.toPlainText()).splitlines())):
                            break
                    else:
                        self.information_update(f"{image_file_name}.txt文件不存在\n")
                
                count+=1
                self.progressBar.setProperty("value", count/all_count*100)

            self.information_update(f"开始进行train文件夹内的图片标注检验\n")
            for image_file in os.listdir(self.workspace_textEdit.toPlainText()+"/train/images"):
                image_file_suffix = Path(self.workspace_textEdit.toPlainText()+f"/train/images/{image_file}").suffix
                image_file_name = image_file[:-len(image_file_suffix)]
                if(image_file_suffix in image_extensions):
                    if(os.path.exists(self.workspace_textEdit.toPlainText()+f"/train/labels/{image_file_name}.txt")):
                        if not xml_convert_examine.function(pic_path=self.workspace_textEdit.toPlainText()+f"/train/images/{image_file}",
                                txt_path=self.workspace_textEdit.toPlainText()+f"/train/labels/{image_file_name}.txt",
                                classnames=list(str(self.target_adding_textEdit.toPlainText()).splitlines())):
                            break
                    else:
                        self.information_update(f"{image_file_name}.txt文件不存在\n")

                count+=1
                self.progressBar.setProperty("value", count/all_count*100)

            self.information_update(f"开始进行val文件夹内的图片标注检验\n")
            for image_file in os.listdir(self.workspace_textEdit.toPlainText()+"/val/images"):
                image_file_suffix = Path(self.workspace_textEdit.toPlainText()+f"/val/images/{image_file}").suffix
                image_file_name = image_file[:-len(image_file_suffix)]
                if(image_file_suffix in image_extensions):
                    if(os.path.exists(self.workspace_textEdit.toPlainText()+f"/val/labels/{image_file_name}.txt")):
                        if not xml_convert_examine.function(pic_path=self.workspace_textEdit.toPlainText()+f"/val/images/{image_file}",
                                txt_path=self.workspace_textEdit.toPlainText()+f"/val/labels/{image_file_name}.txt",
                                classnames=list(str(self.target_adding_textEdit.toPlainText()).splitlines())):
                            break
                    else:
                        self.information_update(f"{image_file_name}.txt文件不存在\n")

                count+=1
                self.progressBar.setProperty("value", count/all_count*100)

            self.information_update(f"开始进行test文件夹内的图片标注检验\n")
            for image_file in os.listdir(self.workspace_textEdit.toPlainText()+"/test/images"):
                image_file_suffix = Path(self.workspace_textEdit.toPlainText()+f"/test/images/{image_file}").suffix
                image_file_name = image_file[:-len(image_file_suffix)]
                if(image_file_suffix in image_extensions):
                    if(os.path.exists(self.workspace_textEdit.toPlainText()+f"/test/labels/{image_file_name}.txt")):
                        if not xml_convert_examine.function(pic_path=self.workspace_textEdit.toPlainText()+f"/test/images/{image_file}",
                                txt_path=self.workspace_textEdit.toPlainText()+f"/test/labels/{image_file_name}.txt",
                                classnames=list(str(self.target_adding_textEdit.toPlainText()).splitlines())):
                            break
                    else:
                        self.information_update(f"{image_file_name}.txt文件不存在\n")

                count+=1
                self.progressBar.setProperty("value", count/all_count*100)
            
            self.information_update(f"标注图片检验命令执行完成\n")
            self.progressBar.setProperty("value", 100)
            cv2.destroyAllWindows()

        else:
            self.information_update(f"无效的工作目录\n")

    def rolabelimg_function(self):
        self.task_onrunning_textBrowser.setText("打开yolo模型标注软件")
        self.progressBar.setProperty("value", 0)

        def rolabelimg_function_threading():
            # 获取当前文件的完整路径
            current_file = sys.argv[0]
            # 获取文件所在目录
            current_dir = os.path.dirname(current_file)
            cmd=f"python {current_dir}/tools/roLabelImg-master/roLabelImg.py"
            subprocess.run(cmd, shell=True)

        threading.Thread(target=rolabelimg_function_threading).start()
        self.progressBar.setProperty("value", 100)

    def Ui_yolo_train_basic_setting_function(self):
        self.yolo_train_basic_setting_window.show()

    def Ui_yolo_train_command_setting_function(self):
        self.yolo_train_command_setting_window.show()

    def yolo_train_start_function(self):
        self.task_onrunning_textBrowser.setText("进行yolo模型训练")
        self.progressBar.setProperty("value", 0)
        self.yolo_train_start_pushButton.setEnabled(False)
        self.yolo_train_start_pushButton.setText("正在处理......")

        cmd=""

        if(self.yolo_train_command_setting_ui.train_command_textEdit.toPlainText()):
            self.task_onrunning_textBrowser.setText("采用高级命令进行训练")
            cmd=self.yolo_train_command_setting_ui.train_command_textEdit.toPlainText()

        else:
            self.task_onrunning_textBrowser.setText("采用基础设置进行训练")
            cmd = (f"yolo train model={self.yolo_train_basic_setting_ui.train_model_comboBox.currentText()} "+
                    f"data={self.workspace_textEdit.toPlainText()}/dataset.yaml "+
                    f"epochs={self.yolo_train_basic_setting_ui.train_epochs_comboBox.currentText()} "+
                    f"patience={self.yolo_train_basic_setting_ui.train_patience_comboBox.currentText()} "+
                    f"device={self.yolo_train_basic_setting_ui.train_device_comboBox.currentText()} "+
                    f"task={self.yolo_train_basic_setting_ui.train_task_comboBox.currentText()} "
                    )
            
        def yolo_train_start_function_threading(cmd):
            # 启动子进程并捕获输出
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8',  # 明确指定编码
                errors='replace',  # 遇到无法解码的字符时替换为问号
                bufsize=1  # 行缓冲
            )

            training_start = False
            while True:
                output = process.stdout.readline()
                self.progress_signal.message_updated.emit(output)
                print(output)

                if output == '' and process.poll() is not None:
                    break
                if output:
                    # 解析进度（匹配Epoch信息）
                    if "Epoch" in output:
                        training_start=True

                    if "/" in output and training_start:
                        parts = output.split()
                        for part in parts:
                            if "/" in part:
                                try:
                                    current, total = part.split("/")
                                    progress = int(current) / int(total) * 100
                                    if(progress!=100):
                                        self.progress_signal.progress_updated.emit(int(progress))
                                    break
                                except:
                                    pass

            self.progress_signal.message_updated.emit("yolo模型训练完成")
            self.progress_signal.progress_updated.emit(int(100))
            self.progress_signal.train_button_status.emit(True)
            process.poll()

        threading.Thread(target=yolo_train_start_function_threading, args=(cmd,)).start()
    
    def yolo_test_start_function(self):
        self.task_onrunning_textBrowser.setText("进行yolo模型检验\n")
        self.progressBar.setProperty("value", 0)

        # 支持的图片扩展名
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}

        if os.path.exists(self.workspace_textEdit.toPlainText()+"/best.pt"):
            model=YOLO(self.workspace_textEdit.toPlainText()+"/best.pt")
            for image_file in os.listdir(self.workspace_textEdit.toPlainText()+"/test/images"):
                image_file_suffix = Path(self.workspace_textEdit.toPlainText()+f"/test/images/{image_file}").suffix
                if(image_file_suffix in image_extensions):
                    results = model(self.workspace_textEdit.toPlainText()+"/test/images/"+image_file)
                    cv2.imshow("yolo模型检验", results[0].plot())
                    if cv2.waitKey(0) == ord("q"):
                        break

            self.information_update("yolo模型检验结束\n")
            self.progressBar.setProperty("value", 100)
            cv2.destroyAllWindows()
        else:
            self.information_update("请先将best.pt文件放到工作目录中\n")



if __name__ == "__main__":
    import sys
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_function()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())