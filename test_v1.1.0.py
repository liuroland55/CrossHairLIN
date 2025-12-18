#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试准星程序 v1.1.0 新功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_version_number():
    """测试版本号是否正确更新"""
    print("=" * 50)
    print("测试 v1.1.0 版本号")
    print("=" * 50)
    
    try:
        from config_ui_pyside6 import ConfigUI
        from PySide6.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        main_window = ConfigUI()
        
        title = main_window.windowTitle()
        print(f"窗口标题: {title}")
        
        if "v1.1.1" in title:
            print("[OK] 版本号正确更新为 v1.1.1")
            return True
        else:
            print("[ERROR] 版本号未正确更新")
            return False
            
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        return False

def test_drag_functionality():
    """测试拖动功能相关方法"""
    print("\n" + "=" * 50)
    print("测试拖动功能")
    print("=" * 50)
    
    try:
        from overlay_window_pyside6 import OverlayWindow
        from PySide6.QtWidgets import QApplication
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        config = {
            "size": 20,
            "color": "#FF0000",
            "shape": "cross",
            "thickness": 2,
            "opacity": 0.8,
            "position": {"x": "center", "y": "center"}
        }
        
        overlay = OverlayWindow(config)
        
        # 检查拖动相关方法是否存在
        methods_to_check = [
            'toggleDragMode',
            'get_crosshair_position',
            'center_crosshair'
        ]
        
        all_methods_exist = True
        for method_name in methods_to_check:
            if hasattr(overlay, method_name):
                print(f"[OK] 方法存在: {method_name}")
            else:
                print(f"[ERROR] 方法缺失: {method_name}")
                all_methods_exist = False
        
        return all_methods_exist
        
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        return False

def test_ui_drag_controls():
    """测试UI拖动控制"""
    print("\n" + "=" * 50)
    print("测试UI拖动控制")
    print("=" * 50)
    
    try:
        from config_ui_pyside6 import ConfigUI
        from PySide6.QtWidgets import QApplication
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        main_window = ConfigUI()
        
        # 检查拖动相关UI元素
        ui_elements_to_check = [
            ('drag_button', '拖动按钮'),
            ('center_button', '居中按钮'),
            ('toggle_drag_mode', '切换拖动模式方法'),
            ('center_crosshair', '居中方法')
        ]
        
        all_elements_exist = True
        for attr_name, description in ui_elements_to_check:
            if hasattr(main_window, attr_name):
                print(f"[OK] {description} 存在")
            else:
                print(f"[ERROR] {description} 缺失")
                all_elements_exist = False
        
        return all_elements_exist
        
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("准星程序 v1.1.0 功能测试")
    print("=" * 50)
    
    tests = [
        ("版本号测试", test_version_number),
        ("拖动功能测试", test_drag_functionality),
        ("UI拖动控制测试", test_ui_drag_controls),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n开始执行: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"[ERROR] {test_name} 执行异常: {e}")
            results.append((test_name, False))
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("[SUCCESS] 所有测试通过！v1.1.0 功能完整")
        return True
    else:
        print("[WARNING] 部分测试失败，需要检查")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
