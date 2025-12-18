#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import glob
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QSlider, QLineEdit,
    QFrame, QGroupBox, QFileDialog, QMessageBox, QInputDialog,
    QApplication
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor


class ConfigUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.overlay_window = None
        self.is_shown = False
        
        # 语言配置
        self.language = "zh"
        self.strings = {
            "zh": {
                "title": "准星程序",
                "author": "B站：林晓CCC",
                "config_management": "配置管理",
                "preset_config": "预设配置:",
                "config_location": "设置配置文件位置:",
                "new_preset": "新建预设",
                "load_preset": "加载预设",
                "save_preset": "保存预设",
                "delete_preset": "删除预设",
                "open_folder": "打开文件夹",
                "show_crosshair": "显示准星",
                "hide_crosshair": "隐藏准星",
                "crosshair_settings": "准星设置",
                "shape": "形状:",
                "size": "大小:",
                "thickness": "粗细:",
                "opacity": "透明度:",
                "color": "颜色:",
                "choose_color": "选择颜色",
                "position": "位置:",
                "center": "居中",
                "drag_mode": "拖动模式",
                "normal_mode": "正常模式",
                "hollow_cross_settings": "空心十字设置:",
                "center_dot_size": "中心点大小:",
                "hollow_cross_dot_settings": "空心十字加点设置:",
                "hollow_gap": "中心距离:",
                "hollow_length": "直线长度:",
                "hollow_thickness": "直线粗细:",
                "save_current": "保存当前配置",
                "language": "语言:",
                "invalid_address": "地址无效！",
                "warning": "警告",
                "success": "成功",
                "error": "错误",
                "confirm": "确认",
                "preset_exists": "预设 '{name}' 已存在！",
                "preset_created": "预设 '{name}' 创建成功！",
                "select_preset": "请先选择一个预设！",
                "preset_loaded": "已加载预设：{name}",
                "config_saved": "配置已保存到：{path}",
                "cannot_delete_default": "默认配置不能删除！",
                "delete_confirm": "确定要删除预设 '{name}' 吗？",
                "preset_deleted": "预设已删除",
                "delete_failed": "删除失败：{error}",
                "cannot_open_folder": "无法打开文件夹：{error}",
                "new_preset_name": "请输入预设名称：",
                "program_error": "程序运行出错：{error}",
            },
            "en": {
                "title": "Crosshair Program",
                "author": "Bilibili: 林晓CCC",
                "config_management": "Configuration Management",
                "preset_config": "Preset Config:",
                "config_location": "Set Config Location:",
                "new_preset": "New Preset",
                "load_preset": "Load Preset",
                "save_preset": "Save Preset",
                "delete_preset": "Delete Preset",
                "open_folder": "Open Folder",
                "show_crosshair": "Show Crosshair",
                "hide_crosshair": "Hide Crosshair",
                "crosshair_settings": "Crosshair Settings",
                "shape": "Shape:",
                "size": "Size:",
                "thickness": "Thickness:",
                "opacity": "Opacity:",
                "color": "Color:",
                "choose_color": "Choose Color",
                "position": "Position:",
                "center": "Center",
                "drag_mode": "Drag Mode",
                "normal_mode": "Normal Mode",
                "save_current": "Save Current Config",
                "language": "Language:",
                "invalid_address": "Invalid Address!",
                "warning": "Warning",
                "success": "Success",
                "error": "Error",
                "confirm": "Confirm",
                "preset_exists": "Preset '{name}' already exists!",
                "preset_created": "Preset '{name}' created successfully!",
                "select_preset": "Please select a preset first!",
                "preset_loaded": "Preset loaded: {name}",
                "config_saved": "Configuration saved to: {path}",
                "cannot_delete_default": "Default configuration cannot be deleted!",
                "delete_confirm": "Are you sure you want to delete preset '{name}'?",
                "preset_deleted": "Preset deleted",
                "delete_failed": "Delete failed: {error}",
                "cannot_open_folder": "Cannot open folder: {error}",
                "new_preset_name": "Please enter preset name:",
                "program_error": "Program error: {error}",
            }
        }
        
        # 配置文件管理
        self.config_dir = os.path.join(os.environ['APPDATA'], 'CrosshairApp')
        os.makedirs(self.config_dir, exist_ok=True)
        self.current_config_file = "default.json"
        self.config_file_path = os.path.join(self.config_dir, self.current_config_file)
        
        # 默认配置
        self.config = {
            "size": 20,
            "color": "#FF0000",
            "shape": "cross",
            "thickness": 2,
            "opacity": 0.8,
            "position": {"x": "center", "y": "center"}
        }
        
        self.load_config()
        self.setup_ui()
        
        # 程序启动后默认显示准星
        QTimer.singleShot(500, self.show_crosshair)
        
    def t(self, key):
        """获取当前语言的字符串"""
        return self.strings[self.language].get(key, key)
    
    def format_text(self, key, **kwargs):
        """格式化字符串"""
        text = self.t(key)
        for k, v in kwargs.items():
            text = text.replace(f"{{{k}}}", str(v))
        return text
    
    def get_config_path(self, config_name):
        """获取指定配置文件的完整路径"""
        if not config_name.endswith('.json'):
            return os.path.join(self.config_dir, config_name + '.json')
        else:
            return os.path.join(self.config_dir, config_name)
    
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file_path):
                with open(self.config_file_path, 'r', encoding='utf-8') as f:
                    self.config.update(json.load(f))
        except Exception as e:
            print(f"加载配置文件失败: {e}")
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get_available_presets(self):
        """获取可用的预设配置列表"""
        preset_files = glob.glob(os.path.join(self.config_dir, '*.json'))
        presets = []
        for file in preset_files:
            preset_name = os.path.basename(file)[:-5]
            presets.append(preset_name)
        return sorted(presets)
    
    def setup_ui(self):
        """设置用户界面"""
        self.setWindowTitle(f"{self.t('title')} v1.1.1")
        self.setGeometry(100, 100, 570, 780)
        self.setFixedSize(570, 780)
        
        # 设置字体
        self.setup_fonts()
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(8, 8, 8, 8)
        
        # 标题
        title_label = QLabel(self.t("title"))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #0066cc; margin-bottom: 5px;")
        main_layout.addWidget(title_label)
        
        # 作者信息
        author_label = QLabel(self.t("author"))
        author_label.setAlignment(Qt.AlignCenter)
        author_label.setStyleSheet("font-size: 10px; color: #0066cc; margin-bottom: 8px;")
        main_layout.addWidget(author_label)
        
        # 语言切换
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel(self.t("language")))
        self.language_var = self.language
        self.language_combo = QComboBox()
        self.language_combo.addItems(["zh", "en"])
        self.language_combo.setCurrentText(self.language)
        self.language_combo.currentTextChanged.connect(self.change_language)
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        main_layout.addLayout(lang_layout)
        
        # 配置文件管理
        config_group = QGroupBox(self.t("config_management"))
        config_layout = QVBoxLayout(config_group)
        
        # 预设配置
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel(self.t("preset_config")))
        self.preset_var = self.current_config_file.replace('.json', '')
        self.preset_combo = QComboBox()
        self.update_preset_list()
        self.preset_combo.currentTextChanged.connect(self.on_preset_selected)
        preset_layout.addWidget(self.preset_combo)
        config_layout.addLayout(preset_layout)
        
        # 配置文件路径
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel(self.t("config_location")))
        self.config_path_var = self.config_file_path
        self.config_path_entry = QLineEdit(self.config_file_path)
        self.config_path_entry.textChanged.connect(self.validate_config_path)
        path_layout.addWidget(self.config_path_entry)
        config_layout.addLayout(path_layout)
        
        # 错误提示
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red; font-size: 9px;")
        config_layout.addWidget(self.error_label)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addWidget(QPushButton(self.t("new_preset")))
        button_layout.addWidget(QPushButton(self.t("load_preset")))
        button_layout.addWidget(QPushButton(self.t("save_preset")))
        button_layout.addWidget(QPushButton(self.t("delete_preset")))
        button_layout.addWidget(QPushButton(self.t("open_folder")))
        
        # 连接按钮信号
        button_layout.itemAt(0).widget().clicked.connect(self.create_preset)
        button_layout.itemAt(1).widget().clicked.connect(self.load_preset)
        button_layout.itemAt(2).widget().clicked.connect(self.save_preset)
        button_layout.itemAt(3).widget().clicked.connect(self.delete_preset)
        button_layout.itemAt(4).widget().clicked.connect(self.open_config_folder)
        
        config_layout.addLayout(button_layout)
        main_layout.addWidget(config_group)
        
        # 控制按钮
        self.show_button = QPushButton(self.t("show_crosshair"))
        self.show_button.clicked.connect(self.toggle_crosshair)
        self.show_button.setStyleSheet("QPushButton { font-size: 14px; padding: 8px; }")
        main_layout.addWidget(self.show_button)
        
        # 设置区域
        settings_group = QGroupBox(self.t("crosshair_settings"))
        settings_layout = QGridLayout(settings_group)
        
        # 形状选择
        settings_layout.addWidget(QLabel(self.t("shape")), 0, 0)
        self.shape_var = self.config["shape"]
        self.shape_combo = QComboBox()
        self.shape_combo.addItems(["cross", "dot", "square", "circle", "triangle", "hollow_cross", "hollow_square", "hollow_cross_dot"])
        self.shape_combo.setCurrentText(self.shape_var)
        self.shape_combo.currentTextChanged.connect(self.on_shape_changed)
        settings_layout.addWidget(self.shape_combo, 0, 1, 1, 2)
        
        # 大小设置
        settings_layout.addWidget(QLabel(self.t("size")), 1, 0)
        self.size_var = float(self.config["size"])
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setRange(1, 100)
        self.size_slider.setValue(int(self.size_var))
        self.size_slider.valueChanged.connect(self.update_size_label)
        self.size_entry = QLineEdit(str(self.size_var))
        self.size_entry.setFixedWidth(60)
        settings_layout.addWidget(self.size_slider, 1, 1)
        settings_layout.addWidget(self.size_entry, 1, 2)
        
        # 粗细设置
        settings_layout.addWidget(QLabel(self.t("thickness")), 2, 0)
        self.thickness_var = float(self.config["thickness"])
        self.thickness_slider = QSlider(Qt.Horizontal)
        self.thickness_slider.setRange(1, 20)
        self.thickness_slider.setValue(int(self.thickness_var))
        self.thickness_slider.valueChanged.connect(self.update_thickness_label)
        self.thickness_entry = QLineEdit(str(self.thickness_var))
        self.thickness_entry.setFixedWidth(60)
        settings_layout.addWidget(self.thickness_slider, 2, 1)
        settings_layout.addWidget(self.thickness_entry, 2, 2)
        
        # 透明度设置
        settings_layout.addWidget(QLabel(self.t("opacity")), 3, 0)
        self.opacity_var = self.config["opacity"]
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(10, 100)
        self.opacity_slider.setValue(int(self.opacity_var * 100))
        self.opacity_slider.valueChanged.connect(self.update_opacity_label)
        self.opacity_entry = QLineEdit(str(self.opacity_var))
        self.opacity_entry.setFixedWidth(60)
        settings_layout.addWidget(self.opacity_slider, 3, 1)
        settings_layout.addWidget(self.opacity_entry, 3, 2)
        
        # 颜色选择
        settings_layout.addWidget(QLabel(self.t("color")), 4, 0)
        self.color_button = QPushButton(self.t("choose_color"))
        self.color_button.setStyleSheet(f"background-color: {self.config['color']};")
        self.color_button.clicked.connect(self.choose_color)
        settings_layout.addWidget(self.color_button, 4, 1, 1, 2)
        
        # 中心点大小设置（用于空心十字加点）
        self.center_dot_layout = QHBoxLayout()
        self.center_dot_layout.addWidget(QLabel(self.t("center_dot_size")))
        self.center_dot_size_var = self.config.get("center_dot_size", 3)
        self.center_dot_size_slider = QSlider(Qt.Horizontal)
        self.center_dot_size_slider.setRange(1, 10)
        self.center_dot_size_slider.setValue(int(self.center_dot_size_var))
        self.center_dot_size_slider.valueChanged.connect(self.update_center_dot_size_label)
        self.center_dot_size_entry = QLineEdit(str(self.center_dot_size_var))
        self.center_dot_size_entry.setFixedWidth(60)
        self.center_dot_layout.addWidget(self.center_dot_size_slider)
        self.center_dot_layout.addWidget(self.center_dot_size_entry)
        settings_layout.addLayout(self.center_dot_layout, 5, 0, 1, 3)
        
        # 空心十字专用设置
        self.hollow_cross_group = QGroupBox(self.t("hollow_cross_settings"))
        hollow_layout = QGridLayout(self.hollow_cross_group)
        
        # 中心距离设置
        hollow_layout.addWidget(QLabel(self.t("hollow_gap")), 0, 0)
        self.hollow_gap_var = self.config.get("hollow_gap", 0)  # 默认值改为0
        self.hollow_gap_slider = QSlider(Qt.Horizontal)
        self.hollow_gap_slider.setRange(0, 50)  # 改为最小值0
        self.hollow_gap_slider.setValue(int(self.hollow_gap_var))
        self.hollow_gap_slider.valueChanged.connect(self.update_hollow_gap_label)
        self.hollow_gap_entry = QLineEdit(str(self.hollow_gap_var))
        self.hollow_gap_entry.setFixedWidth(60)
        hollow_layout.addWidget(self.hollow_gap_slider, 0, 1)
        hollow_layout.addWidget(self.hollow_gap_entry, 0, 2)
        
        # 直线长度设置
        hollow_layout.addWidget(QLabel(self.t("hollow_length")), 1, 0)
        self.hollow_length_var = self.config.get("hollow_length", 30)
        self.hollow_length_slider = QSlider(Qt.Horizontal)
        self.hollow_length_slider.setRange(10, 100)
        self.hollow_length_slider.setValue(int(self.hollow_length_var))
        self.hollow_length_slider.valueChanged.connect(self.update_hollow_length_label)
        self.hollow_length_entry = QLineEdit(str(self.hollow_length_var))
        self.hollow_length_entry.setFixedWidth(60)
        hollow_layout.addWidget(self.hollow_length_slider, 1, 1)
        hollow_layout.addWidget(self.hollow_length_entry, 1, 2)
        
        # 直线粗细设置
        hollow_layout.addWidget(QLabel(self.t("hollow_thickness")), 2, 0)
        self.hollow_thickness_var = self.config.get("hollow_thickness", 2)
        self.hollow_thickness_slider = QSlider(Qt.Horizontal)
        self.hollow_thickness_slider.setRange(1, 10)
        self.hollow_thickness_slider.setValue(int(self.hollow_thickness_var))
        self.hollow_thickness_slider.valueChanged.connect(self.update_hollow_thickness_label)
        self.hollow_thickness_entry = QLineEdit(str(self.hollow_thickness_var))
        self.hollow_thickness_entry.setFixedWidth(60)
        hollow_layout.addWidget(self.hollow_thickness_slider, 2, 1)
        hollow_layout.addWidget(self.hollow_thickness_entry, 2, 2)
        
        settings_layout.addWidget(self.hollow_cross_group, 6, 0, 1, 3)
        
        # 位置设置
        position_layout = QHBoxLayout()
        position_layout.addWidget(QLabel(self.t("position")))
        self.center_button = QPushButton(self.t("center"))
        self.center_button.clicked.connect(self.center_crosshair)
        position_layout.addWidget(self.center_button)
        
        self.drag_button = QPushButton(self.t("drag_mode"))
        self.drag_button.clicked.connect(self.toggle_drag_mode)
        self.drag_button.setStyleSheet("QPushButton { background-color: #ff6b6b; color: white; }")
        position_layout.addWidget(self.drag_button)
        
        position_layout.addStretch()
        settings_layout.addLayout(position_layout, 7, 0, 1, 3)
        
        main_layout.addWidget(settings_group)
        
        # 初始状态设置空心十字控件可见性
        self.update_hollow_cross_visibility()
        
        # 保存配置按钮
        save_button = QPushButton(self.t("save_current"))
        save_button.clicked.connect(self.save_settings)
        main_layout.addWidget(save_button)
        
        # 说明文字
        info_text = "1. 选择预设并自定义参数\n2. 点击显示准星\n3. 调整设置实时更新\n4. 支持全屏游戏使用"
        info_label = QLabel(info_text)
        info_label.setStyleSheet("color: gray; font-size: 9px;")
        info_label.setWordWrap(True)
        main_layout.addWidget(info_label)
        
        main_layout.addStretch()
        
    def setup_fonts(self):
        """设置字体"""
        if self.language == "zh":
            font = QFont("Microsoft YaHei", 9)
        else:
            font = QFont("Times New Roman", 9)
        
        self.setFont(font)
        
    def change_language(self, lang):
        """切换语言"""
        self.language = lang
        
    def validate_config_path(self, path):
        """验证配置文件路径"""
        if not path.strip():
            self.error_label.setText("")
            return
        
        if os.path.isdir(path):
            self.error_label.setText("")
            old_config_dir = self.config_dir
            self.config_dir = path
            
            if old_config_dir != self.config_dir:
                self.config_file_path = self.get_config_path(self.preset_var)
                self.update_config_from_ui()
                self.save_config()
                self.update_preset_list()
        else:
            self.error_label.setText(self.t("invalid_address"))
    
    def on_preset_selected(self, preset_name):
        """预设选择事件"""
        if preset_name:
            self.load_preset()
    
    def update_preset_list(self):
        """更新预设列表"""
        presets = self.get_available_presets()
        self.preset_combo.clear()
        self.preset_combo.addItems(presets)
        if self.preset_var in presets:
            self.preset_combo.setCurrentText(self.preset_var)
    
    def create_preset(self):
        """创建新的预设配置"""
        preset_name, ok = QInputDialog.getText(self, self.t("new_preset"), self.t("new_preset_name"))
        if ok and preset_name.strip():
            preset_name = preset_name.strip()
            if preset_name in self.get_available_presets():
                QMessageBox.warning(self, self.t("warning"), self.format_text("preset_exists", name=preset_name))
                return
            
            self.current_config_file = preset_name + '.json'
            self.config_file_path = self.get_config_path(preset_name)
            
            self.config = {
                "size": 20,
                "color": "#FF0000",
                "shape": "cross",
                "thickness": 2,
                "opacity": 0.8,
                "position": {"x": "center", "y": "center"}
            }
            
            self.save_config()
            self.update_ui_from_config()
            self.update_preset_list()
            self.preset_combo.setCurrentText(preset_name)
            self.config_path_entry.setText(self.config_file_path)
            
            QMessageBox.information(self, self.t("success"), self.format_text("preset_created", name=preset_name))
    
    def load_preset(self):
        """加载预设配置"""
        preset_name = self.preset_combo.currentText()
        if not preset_name:
            QMessageBox.warning(self, self.t("warning"), self.t("select_preset"))
            return
        
        self.current_config_file = preset_name + '.json'
        self.config_file_path = self.get_config_path(preset_name)
        
        # 先加载配置文件内容
        try:
            config_path = self.get_config_path(preset_name)
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
            else:
                loaded_config = {}
        except Exception as e:
            QMessageBox.critical(self, self.t("error"), f"加载预设失败: {e}")
            return
        
        # 设置默认配置，然后用加载的配置覆盖
        self.config = {
            "size": 20,
            "color": "#FF0000",
            "shape": "cross",
            "thickness": 2,
            "opacity": 0.8,
            "position": {"x": "center", "y": "center"},
            "hollow_gap": 0,
            "hollow_length": 30,
            "hollow_thickness": 2,
            "center_dot_size": 3
        }
        
        # 用加载的配置覆盖默认配置
        self.config.update(loaded_config)
        
        # 更新UI
        self.update_ui_from_config()
        self.config_path_entry.setText(self.config_file_path)
        
        # 更新准星显示
        if self.overlay_window:
            self.overlay_window.updateConfig(self.config)
        
        # 如果准星已显示，重新显示以应用新配置
        if self.is_shown:
            self.hide_crosshair()
            self.show_crosshair()
    
    def save_preset(self):
        """保存预设配置"""
        self.update_config_from_ui()
        
        # 确保保存准星位置信息
        if self.overlay_window and hasattr(self.overlay_window, 'get_crosshair_position'):
            pos = self.overlay_window.get_crosshair_position()
            # 只有在非居中位置时才保存具体坐标
            if pos[0] != QApplication.primaryScreen().size().width() // 2 or \
               pos[1] != QApplication.primaryScreen().size().height() // 2:
                self.config["position"] = {"x": pos[0], "y": pos[1]}
            else:
                self.config["position"] = {"x": "center", "y": "center"}
        
        self.save_config()
        QMessageBox.information(self, self.t("success"), self.format_text("config_saved", path=self.config_file_path))
    
    def delete_preset(self):
        """删除预设配置"""
        preset_name = self.preset_combo.currentText()
        if not preset_name:
            QMessageBox.warning(self, self.t("warning"), self.t("select_preset"))
            return
        
        if preset_name == 'default':
            QMessageBox.warning(self, self.t("warning"), self.t("cannot_delete_default"))
            return
        
        reply = QMessageBox.question(self, self.t("confirm"), self.format_text("delete_confirm", name=preset_name))
        if reply == QMessageBox.Yes:
            preset_file = self.get_config_path(preset_name)
            try:
                if os.path.exists(preset_file):
                    os.remove(preset_file)
                    QMessageBox.information(self, self.t("success"), self.t("preset_deleted"))
                    self.update_preset_list()
                    self.preset_combo.setCurrentText('default')
                    self.on_preset_selected()
            except Exception as e:
                QMessageBox.critical(self, self.t("error"), self.format_text("delete_failed", error=str(e)))
    
    def open_config_folder(self):
        """打开配置文件夹"""
        try:
            os.startfile(self.config_dir)
        except Exception as e:
            QMessageBox.critical(self, self.t("error"), self.format_text("cannot_open_folder", error=str(e)))
    
    
    def update_size_label(self, value):
        """更新大小标签"""
        self.size_entry.setText(str(value))
        self.update_crosshair()
    
    def update_thickness_label(self, value):
        """更新粗细标签"""
        self.thickness_entry.setText(str(value))
        self.update_crosshair()
    
    def update_opacity_label(self, value):
        """更新透明度标签"""
        self.opacity_entry.setText(str(value / 100.0))
        self.update_crosshair()
    
    def choose_color(self):
        """选择颜色"""
        from PySide6.QtWidgets import QColorDialog
        color = QColorDialog.getColor()
        if color.isValid():
            self.config["color"] = color.name()
            self.color_button.setStyleSheet(f"background-color: {color.name()};")
            self.update_crosshair()
    
    def toggle_crosshair(self):
        """切换准星显示/隐藏"""
        if not self.is_shown:
            self.show_crosshair()
        else:
            self.hide_crosshair()
    
    def show_crosshair(self):
        """显示准星"""
        if self.overlay_window is None:
            from overlay_window_pyside6 import OverlayWindow
            self.overlay_window = OverlayWindow(self.config)
        
        self.overlay_window.showFullScreen()
        self.overlay_window.updateConfig(self.config)
        self.show_button.setText(self.t("hide_crosshair"))
        self.is_shown = True
    
    def hide_crosshair(self):
        """隐藏准星"""
        if self.overlay_window:
            self.overlay_window.hide()
        self.show_button.setText(self.t("show_crosshair"))
        self.is_shown = False
    
    def update_crosshair(self):
        """更新准星"""
        self.update_config_from_ui()
        if self.overlay_window and self.is_shown:
            self.overlay_window.updateConfig(self.config)
    
    def refresh_crosshair_display(self):
        """刷新准星显示"""
        self.update_crosshair()
    
    def center_crosshair(self):
        """将准星居中"""
        self.config["position"] = {"x": "center", "y": "center"}
        if self.overlay_window:
            self.overlay_window.center_crosshair()
            # 同时更新配置到UI
            self.update_config_from_ui()
            self.save_config()
    
    def toggle_drag_mode(self):
        """切换拖动模式"""
        if not self.is_shown:
            QMessageBox.warning(self, self.t("warning"), "请先显示准星！")
            return
        
        if self.overlay_window:
            is_drag_mode = self.overlay_window.toggleDragMode()
            if is_drag_mode:
                self.drag_button.setText(self.t("normal_mode"))
                self.drag_button.setStyleSheet("QPushButton { background-color: #51cf66; color: white; }")
            else:
                self.drag_button.setText(self.t("drag_mode"))
                self.drag_button.setStyleSheet("QPushButton { background-color: #ff6b6b; color: white; }")
                # 退出拖动模式时保存位置
                if hasattr(self.overlay_window, 'get_crosshair_position'):
                    pos = self.overlay_window.get_crosshair_position()
                    self.config["position"] = {"x": pos[0], "y": pos[1]}
                    self.save_config()
    
    def save_settings(self):
        """保存设置"""
        self.update_config_from_ui()
        self.save_config()
        QMessageBox.information(self, self.t("success"), self.format_text("config_saved", path=self.config_file_path))
    
    def on_shape_changed(self, shape):
        """形状改变事件"""
        self.update_hollow_cross_visibility()
        self.update_crosshair()
    
    def update_hollow_cross_visibility(self):
        """更新空心十字控件可见性"""
        is_hollow_cross = self.shape_combo.currentText() in ["hollow_cross", "hollow_cross_dot"]
        self.hollow_cross_group.setVisible(is_hollow_cross)
        
        # 中心点大小控件只在空心十字加点时显示
        is_hollow_cross_dot = self.shape_combo.currentText() == "hollow_cross_dot"
        for i in range(self.center_dot_layout.count()):
            widget = self.center_dot_layout.itemAt(i).widget()
            if widget:
                widget.setVisible(is_hollow_cross_dot)
    
    def update_center_dot_size_label(self, value):
        """更新中心点大小标签"""
        self.center_dot_size_entry.setText(str(value))
        self.update_crosshair()
    
    def update_hollow_gap_label(self, value):
        """更新空心十字中心距离标签"""
        self.hollow_gap_entry.setText(str(value))
        self.update_crosshair()
    
    def update_hollow_length_label(self, value):
        """更新空心十字直线长度标签"""
        self.hollow_length_entry.setText(str(value))
        self.update_crosshair()
    
    def update_hollow_thickness_label(self, value):
        """更新空心十字直线粗细标签"""
        self.hollow_thickness_entry.setText(str(value))
        self.update_crosshair()
    
    def update_config_from_ui(self):
        """从UI更新配置"""
        self.config["shape"] = self.shape_combo.currentText()
        self.config["size"] = self.size_slider.value()
        self.config["thickness"] = self.thickness_slider.value()
        self.config["opacity"] = self.opacity_slider.value() / 100.0
        
        # 保存空心十字专用参数
        if self.shape_combo.currentText() in ["hollow_cross", "hollow_cross_dot"]:
            self.config["hollow_gap"] = self.hollow_gap_slider.value()
            self.config["hollow_length"] = self.hollow_length_slider.value()
            self.config["hollow_thickness"] = self.hollow_thickness_slider.value()
        
        # 保存中心点大小参数
        if self.shape_combo.currentText() == "hollow_cross_dot":
            self.config["center_dot_size"] = self.center_dot_size_slider.value()
        
        # 修复颜色解析
        style_sheet = self.color_button.styleSheet()
        if "background-color:" in style_sheet:
            self.config["color"] = style_sheet.split("background-color:")[1].split(";")[0].strip()
        else:
            self.config["color"] = "#FF0000"
    
    def update_ui_from_config(self):
        """从配置更新UI"""
        # 暂时断开信号连接，避免触发不必要的更新
        self.shape_combo.blockSignals(True)
        self.size_slider.blockSignals(True)
        self.thickness_slider.blockSignals(True)
        self.opacity_slider.blockSignals(True)
        self.hollow_gap_slider.blockSignals(True)
        self.hollow_length_slider.blockSignals(True)
        self.hollow_thickness_slider.blockSignals(True)
        self.center_dot_size_slider.blockSignals(True)
        
        try:
            # 更新形状
            shape = self.config.get("shape", "cross")
            self.shape_combo.setCurrentText(shape)
            
            # 更新大小
            size = int(self.config.get("size", 20))
            self.size_slider.setValue(size)
            self.size_entry.setText(str(size))
            
            # 更新粗细
            thickness = int(self.config.get("thickness", 2))
            self.thickness_slider.setValue(thickness)
            self.thickness_entry.setText(str(thickness))
            
            # 更新透明度
            opacity = float(self.config.get("opacity", 0.8))
            self.opacity_slider.setValue(int(opacity * 100))
            self.opacity_entry.setText(str(opacity))
            
            # 更新颜色
            color = self.config.get("color", "#FF0000")
            self.color_button.setStyleSheet(f"background-color: {color};")
            
            # 更新空心十字专用设置
            hollow_gap = self.config.get("hollow_gap", 0)
            self.hollow_gap_slider.setValue(hollow_gap)
            self.hollow_gap_entry.setText(str(hollow_gap))
            
            hollow_length = self.config.get("hollow_length", 30)
            self.hollow_length_slider.setValue(hollow_length)
            self.hollow_length_entry.setText(str(hollow_length))
            
            hollow_thickness = self.config.get("hollow_thickness", 2)
            self.hollow_thickness_slider.setValue(hollow_thickness)
            self.hollow_thickness_entry.setText(str(hollow_thickness))
            
            # 更新中心点大小设置
            center_dot_size = self.config.get("center_dot_size", 3)
            self.center_dot_size_slider.setValue(center_dot_size)
            self.center_dot_size_entry.setText(str(center_dot_size))
            
            # 更新控件可见性
            self.update_hollow_cross_visibility()
            
        finally:
            # 重新连接信号
            self.shape_combo.blockSignals(False)
            self.size_slider.blockSignals(False)
            self.thickness_slider.blockSignals(False)
            self.opacity_slider.blockSignals(False)
            self.hollow_gap_slider.blockSignals(False)
            self.hollow_length_slider.blockSignals(False)
            self.hollow_thickness_slider.blockSignals(False)
            self.center_dot_size_slider.blockSignals(False)
    
    def closeEvent(self, event):
        """关闭事件"""
        if self.overlay_window:
            self.overlay_window.close()
        event.accept()
