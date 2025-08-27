#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QTranslator, QCoreApplication
from PyQt5.QtWidgets import QApplication

def test_translation():
    app = QApplication(sys.argv)
    
    # 创建翻译器
    translator = QTranslator()
    
    # 加载翻译文件
    translation_file = "translations/zh_CN.qm"  # 或 "translations/en.qm"
    if translator.load(translation_file):
        app.installTranslator(translator)
        print(f"成功加载翻译文件: {translation_file}")
        
        # 测试翻译
        translated_text = QCoreApplication.translate("MainWindow", "窗口标题")
        print(f"翻译测试: '窗口标题' -> '{translated_text}'")
        
        # 测试更多字符串
        test_strings = [
            "按钮文本",
            "菜单项",
            "标签文本",
            # 添加您界面中使用的其他字符串
        ]
        
        for text in test_strings:
            translated = QCoreApplication.translate("MainWindow", text)
            print(f"'{text}' -> '{translated}'")
    else:
        print(f"无法加载翻译文件: {translation_file}")
    
    sys.exit(0)

if __name__ == "__main__":
    test_translation()