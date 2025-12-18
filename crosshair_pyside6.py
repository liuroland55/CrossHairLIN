#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from config_ui_pyside6 import ConfigUI


def main():
    """主函数"""
    try:
        # 创建应用程序
        app = QApplication(sys.argv)
        
        # 设置应用程序样式
        app.setStyle("Fusion")
        
        # 设置应用程序信息
        app.setApplicationName("准星程序")
        app.setApplicationVersion("1.0.1")
        app.setOrganizationName("林晓CCC")
        
        # 启用高DPI支持（新版PySide6不需要这些设置）
        # app.setAttribute(Qt.AA_EnableHighDpiScaling)  # 已弃用
        # app.setAttribute(Qt.AA_UseHighDpiPixmaps)    # 已弃用
        
        # 创建并显示主窗口
        main_window = ConfigUI()
        main_window.show()
        
        # 运行应用程序
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"程序运行出错：{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
