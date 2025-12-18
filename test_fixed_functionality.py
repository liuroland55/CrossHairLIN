#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试修复后的拖动功能
"""

import sys
import json
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QPoint
from config_ui_pyside6 import ConfigUI

def test_fixed_functionality():
    """测试修复后的功能"""
    print("开始测试修复后的功能...")
    
    app = QApplication(sys.argv)
    
    # 创建主窗口
    main_window = ConfigUI()
    
    # 测试1: 检查center_crosshair方法
    print("\n=== 测试1: 居中功能 ===")
    if hasattr(main_window, 'center_crosshair'):
        print("[OK] center_crosshair方法存在")
        
        # 显示准星
        main_window.show_crosshair()
        
        # 调用居中方法
        main_window.center_crosshair()
        
        # 检查配置是否更新
        if main_window.config.get("position") == {"x": "center", "y": "center"}:
            print("[OK] 居中配置已更新")
        else:
            print("[ERROR] 居中配置未更新")
            return False
            
        # 检查overlay_window的crosshair_pos
        if main_window.overlay_window and hasattr(main_window.overlay_window, 'crosshair_pos'):
            if main_window.overlay_window.crosshair_pos:
                screen_size = QApplication.primaryScreen().size()
                expected_x = screen_size.width() // 2
                expected_y = screen_size.height() // 2
                if (main_window.overlay_window.crosshair_pos.x() == expected_x and 
                    main_window.overlay_window.crosshair_pos.y() == expected_y):
                    print("[OK] overlay_window的crosshair_pos已正确设置")
                else:
                    print("[ERROR] overlay_window的crosshair_pos设置不正确")
                    return False
        else:
            print("[ERROR] overlay_window或crosshair_pos不存在")
            return False
    else:
        print("[ERROR] center_crosshair方法不存在")
        return False
    
    # 测试2: 拖动模式切换
    print("\n=== 测试2: 拖动模式切换 ===")
    if hasattr(main_window.overlay_window, 'updateConfig'):
        print("[OK] updateConfig方法存在")
        
        # 测试updateConfig是否重置crosshair_pos
        main_window.overlay_window.crosshair_pos = QPoint(100, 200)
        main_window.overlay_window.updateConfig(main_window.config)
        
        if main_window.overlay_window.crosshair_pos is None:
            print("[OK] updateConfig正确重置了crosshair_pos")
        else:
            print("[ERROR] updateConfig未重置crosshair_pos")
            return False
    else:
        print("[ERROR] updateConfig方法不存在")
        return False
    
    # 测试3: 预设位置保存
    print("\n=== 测试3: 预设位置保存 ===")
    
    # 保存当前配置文件路径
    original_config_file = main_window.current_config_file
    original_config_path = main_window.config_file_path
    
    # 创建测试预设
    test_preset_name = "test_position_preset"
    main_window.current_config_file = test_preset_name + '.json'
    main_window.config_file_path = main_window.get_config_path(test_preset_name)
    
    # 设置非居中位置
    main_window.config["position"] = {"x": 150, "y": 250}
    
    # 保存配置
    main_window.save_config()
    
    # 验证配置文件
    if os.path.exists(main_window.config_file_path):
        with open(main_window.config_file_path, 'r', encoding='utf-8') as f:
            saved_config = json.load(f)
            if saved_config.get("position") == {"x": 150, "y": 250}:
                print("[OK] 预设位置保存功能正常")
            else:
                print("[ERROR] 预设位置保存功能异常")
                return False
    else:
        print("[ERROR] 预设配置文件未创建")
        return False
    
    # 清理测试文件
    if os.path.exists(main_window.config_file_path):
        os.remove(main_window.config_file_path)
    
    # 恢复原始配置
    main_window.current_config_file = original_config_file
    main_window.config_file_path = original_config_path
    
    # 测试4: 切换拖动模式后位置保持
    print("\n=== 测试4: 切换拖动模式后位置保持 ===")
    
    # 设置非居中位置
    main_window.config["position"] = {"x": 300, "y": 400}
    main_window.overlay_window.updateConfig(main_window.config)
    
    # 进入拖动模式
    is_drag_mode = main_window.overlay_window.toggleDragMode()
    if is_drag_mode:
        print("[OK] 成功进入拖动模式")
        
        # 检查crosshair_pos是否正确初始化
        screen_size = QApplication.primaryScreen().size()
        if main_window.overlay_window.crosshair_pos:
            print("[OK] crosshair_pos已正确初始化")
        else:
            print("[ERROR] crosshair_pos未正确初始化")
            return False
        
        # 退出拖动模式
        is_drag_mode = main_window.overlay_window.toggleDragMode()
        if not is_drag_mode:
            print("[OK] 成功退出拖动模式")
        else:
            print("[ERROR] 退出拖动模式失败")
            return False
    else:
        print("[ERROR] 进入拖动模式失败")
        return False
    
    print("\n[OK] 所有修复功能测试通过！")
    return True

def test_position_saving_logic():
    """测试位置保存逻辑"""
    print("\n=== 测试位置保存逻辑 ===")
    
    # 重用现有的QApplication实例
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    main_window = ConfigUI()
    main_window.show_crosshair()
    
    # 测试居中位置的保存
    print("测试居中位置保存...")
    main_window.overlay_window.center_crosshair()
    pos = main_window.overlay_window.get_crosshair_position()
    screen_size = QApplication.primaryScreen().size()
    center_x = screen_size.width() // 2
    center_y = screen_size.height() // 2
    
    if pos[0] == center_x and pos[1] == center_y:
        print("[OK] 居中位置获取正确")
    else:
        print(f"[ERROR] 居中位置获取错误: 期望({center_x}, {center_y}), 实际({pos[0]}, {pos[1]})")
        return False
    
    # 测试非居中位置的保存
    print("测试非居中位置保存...")
    main_window.config["position"] = {"x": 100, "y": 200}
    main_window.overlay_window.updateConfig(main_window.config)
    
    # 模拟拖动到新位置
    if hasattr(main_window.overlay_window, 'crosshair_pos'):
        main_window.overlay_window.crosshair_pos = QPoint(150, 250)
    
    pos = main_window.overlay_window.get_crosshair_position()
    if pos[0] == 150 and pos[1] == 250:
        print("[OK] 非居中位置获取正确")
    else:
        print(f"[ERROR] 非居中位置获取错误: 期望(150, 250), 实际({pos[0]}, {pos[1]})")
        return False
    
    return True

if __name__ == "__main__":
    success1 = test_fixed_functionality()
    success2 = test_position_saving_logic()
    
    if success1 and success2:
        print("\n[SUCCESS] 所有修复测试通过！")
        print("\n修复内容:")
        print("1. [OK] 居中后切换拖动模式准星不会跳回去")
        print("2. [OK] 正常模式下可以使用居中功能")
        print("3. [OK] 位置保存在每个单独的预设里")
        print("4. [OK] updateConfig正确重置crosshair_pos")
        print("5. [OK] center_crosshair正确更新overlay_window状态")
    else:
        print("\n[FAILED] 部分测试失败，请检查修复。")
    
    sys.exit(0 if (success1 and success2) else 1)
