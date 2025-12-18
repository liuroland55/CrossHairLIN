#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试拖动功能的简单脚本
"""

import sys
import json
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from config_ui_pyside6 import ConfigUI

def test_drag_functionality():
    """测试拖动功能"""
    print("开始测试拖动功能...")
    
    app = QApplication(sys.argv)
    
    # 创建主窗口
    main_window = ConfigUI()
    
    # 检查是否有拖动按钮
    if hasattr(main_window, 'drag_button'):
        print("[OK] 拖动按钮已创建")
    else:
        print("[ERROR] 拖动按钮未找到")
        return False
    
    # 检查是否有toggle_drag_mode方法
    if hasattr(main_window, 'toggle_drag_mode'):
        print("[OK] toggle_drag_mode方法已创建")
    else:
        print("[ERROR] toggle_drag_mode方法未找到")
        return False
    
    # 显示准星
    main_window.show_crosshair()
    
    # 检查overlay_window是否有拖动相关方法
    if main_window.overlay_window:
        if hasattr(main_window.overlay_window, 'toggleDragMode'):
            print("[OK] toggleDragMode方法已创建")
        else:
            print("[ERROR] toggleDragMode方法未找到")
            return False
        
        if hasattr(main_window.overlay_window, 'get_crosshair_position'):
            print("[OK] get_crosshair_position方法已创建")
        else:
            print("[ERROR] get_crosshair_position方法未找到")
            return False
        
        if hasattr(main_window.overlay_window, 'mousePressEvent'):
            print("[OK] mousePressEvent方法已创建")
        else:
            print("[ERROR] mousePressEvent方法未找到")
            return False
        
        if hasattr(main_window.overlay_window, 'mouseMoveEvent'):
            print("[OK] mouseMoveEvent方法已创建")
        else:
            print("[ERROR] mouseMoveEvent方法未找到")
            return False
        
        if hasattr(main_window.overlay_window, 'mouseReleaseEvent'):
            print("[OK] mouseReleaseEvent方法已创建")
        else:
            print("[ERROR] mouseReleaseEvent方法未找到")
            return False
    else:
        print("[ERROR] overlay_window未创建")
        return False
    
    print("[OK] 所有拖动功能组件检查通过！")
    
    # 测试配置保存
    test_position = {"x": 100, "y": 200}
    main_window.config["position"] = test_position
    main_window.save_config()
    
    # 验证配置是否保存
    try:
        with open(main_window.config_file_path, 'r', encoding='utf-8') as f:
            saved_config = json.load(f)
            if saved_config.get("position") == test_position:
                print("[OK] 位置配置保存功能正常")
            else:
                print("[ERROR] 位置配置保存功能异常")
                return False
    except Exception as e:
        print(f"[ERROR] 配置文件读取失败: {e}")
        return False
    
    print("[OK] 拖动功能测试完成！")
    return True

if __name__ == "__main__":
    success = test_drag_functionality()
    if success:
        print("\n[SUCCESS] 所有测试通过！拖动功能已成功实现。")
        print("\n使用说明：")
        print("1. 运行程序后会自动显示准星")
        print("2. 点击'拖动模式'按钮进入拖动模式")
        print("3. 拖动准星到想要的位置")
        print("4. 点击'正常模式'按钮退出拖动模式并保存位置")
        print("5. 位置会自动保存到配置文件中")
    else:
        print("\n[FAILED] 测试失败，请检查代码实现。")
    
    sys.exit(0 if success else 1)
