# translations.py
from PyQt5 import QtCore

class Translator:
    def __init__(self):
        self.translator_cn = QtCore.QTranslator()
        self.translator_en = QtCore.QTranslator()
        self.current_language = 'cn'  # 默认中文
        
    def load_translations(self, app):
        # 加载中文翻译
        self.translator_cn.load(QtCore.QLocale(), ':/translations/translations_cn.qm')
        # 加载英文翻译
        self.translator_en.load(QtCore.QLocale(), ':/translations/translations_en.qm')
        
    def set_language(self, app, language):
        # 移除现有的翻译
        app.removeTranslator(self.translator_cn)
        app.removeTranslator(self.translator_en)
        
        # 设置新语言
        if language == 'cn':
            app.installTranslator(self.translator_cn)
            self.current_language = 'cn'
        else:
            app.installTranslator(self.translator_en)
            self.current_language = 'en'
            
    def get_current_language(self):
        return self.current_language