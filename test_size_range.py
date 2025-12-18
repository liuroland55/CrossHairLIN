#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试准星大小范围修改
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_size_range():
    """测试准星大小范围"""
    try:
        from config_ui_pyside6 import ConfigUI
        from PySide6.QtWidgets import QApplication
        
        app = QApplication([])
        main_window = ConfigUI()
        
        # 检查大小滑块范围
        min_size = main_window.size_slider.minimum()
        max_size = main_window.size_slider.maximum()
        current_size = main_window.size_slider.value()
        
        print(f"准星大小滑块范围: {min_size} - {max_size}")
        print(f"当前大小值: {current_size}")
        
        if min_size == 1:
            print("[OK] 准星大小最小值已成功设置为1")
            return True
        else:
            print(f"[ERROR] 准星大小最小值设置失败，当前为: {min_size}")
            return False
            
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        return False

if __name__ == "__main__":
    print("测试准星大小范围修改")
    print("=" * 40)
    
    success = test_size_range()
    
    if success:
        print("\n[SUCCESS] 准星大小最小值修改成功！")
    else:
        print("\n[FAILED] 准星大小最小值修改失败！")
    
    sys.exit(0 if success else 1)
