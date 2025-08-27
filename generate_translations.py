#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import glob
import subprocess
from xml.etree import ElementTree as ET
from xml.dom import minidom
from googletrans import Translator

class QtTranslationGenerator:
    def __init__(self):
        self.translator = Translator()
        self.messages = []
        
    def scan_project_files(self):
        """扫描项目中的所有Python和UI文件"""
        project_root = r"G:\Yolo-integrated-training-tool\Yolo-integrated-training-tool"
        file_list = []
        
        for ext in ['.py', '.ui']:
            pattern = os.path.join(project_root, '**', f'*{ext}')
            file_list.extend(glob.glob(pattern, recursive=True))
            
        # 过滤掉虚拟环境和其他不需要的目录
        exclude_dirs = ['venv', 'env', '.git', '__pycache__', 'build', 'dist']
        filtered_files = []
        for file_path in file_list:
            if not any(exclude_dir in file_path for exclude_dir in exclude_dirs):
                filtered_files.append(file_path)
                
        return filtered_files
    
    def extract_from_py_file(self, file_path):
        """从Python文件中提取可翻译字符串"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 匹配各种翻译函数调用
            patterns = [
                r'_translate\s*\(\s*["\'](.*?)["\']\s*,\s*["\'](.*?)["\']\s*\)',
                r'QtCore\.QCoreApplication\.translate\s*\(\s*["\'](.*?)["\']\s*,\s*["\'](.*?)["\']\s*\)',
            ]
            
            extracted = []
            for pattern in patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    context = match.group(1)
                    source_text = match.group(2)
                    # 获取行号
                    line_num = content[:match.start()].count('\n') + 1
                    extracted.append((source_text, context, file_path, line_num))
            
            return extracted
        except Exception as e:
            print(f"处理Python文件 {file_path} 时出错: {e}")
            return []
    
    def extract_from_ui_file(self, file_path):
        """从UI文件中提取字符串"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 使用正则表达式查找所有需要翻译的文本
            patterns = [
                r'<string[^>]*>(.*?)</string>',
                r'setText\(_translate\(.*?,\s*"(.*?)"\)\)',
                r'setTitle\(_translate\(.*?,\s*"(.*?)"\)\)',
                r'setPlaceholderText\(_translate\(.*?,\s*"(.*?)"\)\)',
                r'setToolTip\(_translate\(.*?,\s*"(.*?)"\)\)',
                r'setStatusTip\(_translate\(.*?,\s*"(.*?)"\)\)',
                r'setWhatsThis\(_translate\(.*?,\s*"(.*?)"\)\)',
            ]
            
            extracted = []
            for pattern in patterns:
                matches = re.finditer(pattern, content, re.DOTALL)
                for match in matches:
                    source_text = match.group(1)
                    # 清理文本，移除转义字符
                    clean_text = source_text.replace('\\"', '"').replace('\\n', '\n')
                    if clean_text and not clean_text.isspace():
                        # 获取行号（近似值）
                        line_num = content[:match.start()].count('\n') + 1
                        extracted.append((clean_text, "UI", file_path, line_num))
            
            return extracted
        except Exception as e:
            print(f"处理UI文件 {file_path} 时出错: {e}")
            return []
    
    def extract_translatable_strings(self):
        """从所有项目文件中提取可翻译字符串"""
        print("扫描项目文件...")
        files = self.scan_project_files()
        print(f"找到 {len(files)} 个文件进行处理")
        
        all_messages = []
        for file_path in files:
            if file_path.endswith('.py'):
                messages = self.extract_from_py_file(file_path)
            elif file_path.endswith('.ui'):
                messages = self.extract_from_ui_file(file_path)
            else:
                continue
                
            if messages:
                print(f"从 {os.path.basename(file_path)} 中提取了 {len(messages)} 个字符串")
                all_messages.extend(messages)
        
        # 去重但保留位置信息
        unique_messages = []
        seen = set()
        for msg in all_messages:
            identifier = (msg[0], msg[1])
            if identifier not in seen:
                seen.add(identifier)
                unique_messages.append(msg)
        
        self.messages = unique_messages
        print(f"总共提取了 {len(unique_messages)} 个唯一可翻译字符串")
        return unique_messages
    
    def translate_texts(self, texts, target_lang='en'):
        """使用Google翻译API翻译文本"""
        translations = {}
        
        for i, text in enumerate(texts):
            if not text.strip():
                translations[text] = ""
                continue
                
            try:
                # 翻译文本
                result = self.translator.translate(text, dest=target_lang)
                translations[text] = result.text
                print(f"[{i+1}/{len(texts)}] 已翻译: '{text}' -> '{result.text}'")
                
                # 添加延迟以避免请求过于频繁
                if (i + 1) % 5 == 0:
                    import time
                    time.sleep(0.5)
            except Exception as e:
                print(f"翻译失败: '{text}' - {e}")
                translations[text] = text
        
        return translations
    
    def generate_ts_file(self, output_path, language_code, translations=None):
        """生成TS文件，包含源代码位置信息"""
        # 创建TS文档结构
        ts = ET.Element("TS")
        ts.set("version", "2.1")
        ts.set("language", language_code)
        ts.set("sourcelanguage", "zh_CN")
        
        # 按上下文分组消息
        context_groups = {}
        for source, context, filename, line in self.messages:
            if context not in context_groups:
                context_groups[context] = []
            
            # 使用相对路径
            rel_path = os.path.relpath(filename, os.path.dirname(output_path))
            context_groups[context].append({
                "source": source,
                "translation": translations.get(source, "") if translations else "",
                "filename": rel_path,
                "line": line
            })
        
        # 为每个上下文创建元素
        for context_name, messages in context_groups.items():
            context_elem = ET.SubElement(ts, "context")
            name_elem = ET.SubElement(context_elem, "name")
            name_elem.text = context_name
            
            for msg in messages:
                message_elem = ET.SubElement(context_elem, "message")
                
                # 添加位置信息
                location_elem = ET.SubElement(message_elem, "location")
                location_elem.set("filename", msg["filename"])
                location_elem.set("line", str(msg["line"]))
                
                # 添加源文本
                source_elem = ET.SubElement(message_elem, "source")
                source_elem.text = msg["source"]
                
                # 添加翻译文本
                translation_elem = ET.SubElement(message_elem, "translation")
                if msg["translation"]:
                    translation_elem.text = msg["translation"]
                else:
                    translation_elem.set("type", "unfinished")
        
        # 美化XML输出
        rough_string = ET.tostring(ts, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="    ", encoding="utf-8")
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 写入文件
        with open(output_path, 'wb') as f:
            f.write(pretty_xml)
        
        print(f"已生成TS文件: {output_path}")
        return output_path
    
    def compile_ts_to_qm(self, ts_path, qm_path):
        """使用lrelease编译TS文件为QM文件"""
        try:
            # 尝试使用lrelease工具
            result = subprocess.run(['lrelease', ts_path, '-qm', qm_path], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"已生成QM文件: {qm_path}")
                return True
            else:
                print(f"lrelease失败: {result.stderr}")
                return False
        except FileNotFoundError:
            print("未找到lrelease工具，无法编译QM文件")
            print("请安装Qt Linguist工具或手动运行: lrelease translations/*.ts")
            return False
    
    def generate_translations(self):
        """生成所有语言的翻译文件"""
        languages = ['en', 'zh_CN']
        
        # 提取所有可翻译字符串
        self.extract_translatable_strings()
        if not self.messages:
            print("未找到可翻译的字符串")
            return False
        
        # 提取唯一的源文本
        source_texts = list(set([msg[0] for msg in self.messages]))
        
        # 创建输出目录
        output_dir = r"G:\Yolo-integrated-training-tool\Yolo-integrated-training-tool\translations"
        os.makedirs(output_dir, exist_ok=True)
        
        # 为每种语言生成翻译
        for lang in languages:
            print(f"\n处理 {lang} 语言...")
            
            # 获取翻译
            if lang == 'zh_CN':
                # 中文使用原文
                translations = {text: text for text in source_texts}
            else:
                # 其他语言使用翻译
                translations = self.translate_texts(source_texts, lang)
            
            # 生成TS文件
            ts_file = os.path.join(output_dir, f'{lang}.ts')
            self.generate_ts_file(ts_file, lang, translations)
            
            # 编译为QM文件
            qm_file = os.path.join(output_dir, f'{lang}.qm')
            self.compile_ts_to_qm(ts_file, qm_file)
        
        print(f"\n翻译完成! 文件保存在: {output_dir}")
        return True

if __name__ == "__main__":
    generator = QtTranslationGenerator()
    generator.generate_translations()