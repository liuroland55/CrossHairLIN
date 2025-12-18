#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
准星程序 v1.1.1 打包脚本
使用 PyInstaller 打包成独立的可执行文件
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime

def build_executable():
    """打包可执行文件"""
    print("=" * 50)
    print("准星程序 v1.1.1 打包工具")
    print("=" * 50)
    
    # 检查 PyInstaller
    try:
        import PyInstaller
        print(f"[OK] PyInstaller 已安装: {PyInstaller.__version__}")
    except ImportError:
        print("[ERROR] PyInstaller 未安装，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        import PyInstaller
        print(f"[OK] PyInstaller 安装成功: {PyInstaller.__version__}")
    
    # 检查 PySide6
    try:
        import PySide6
        print(f"[OK] PySide6 已安装: {PySide6.__version__}")
    except ImportError:
        print("[ERROR] PySide6 未安装，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyside6"])
        import PySide6
        print(f"[OK] PySide6 安装成功: {PySide6.__version__}")
    
    # 构建参数
    app_name = "准星程序"
    main_script = "crosshair_pyside6.py"
    icon_path = None  # 如果有图标文件，可以在这里指定
    
    # PyInstaller 命令参数
    pyinstaller_args = [
        "--name", app_name,
        "--onefile",  # 打包成单个文件
        "--windowed",  # 无控制台窗口
        "--clean",  # 清理临时文件
        "--noconfirm",  # 不询问确认
        "--distpath", ".",  # 输出到当前目录
        "--workpath", "build",  # 临时构建目录
    ]
    
    # 如果有图标文件，添加图标参数
    if icon_path and os.path.exists(icon_path):
        pyinstaller_args.extend(["--icon", icon_path])
        print(f"[OK] 使用图标: {icon_path}")
    
    # 添加主脚本
    pyinstaller_args.append(main_script)
    
    # 执行打包
    print("\n[INFO] 开始打包...")
    try:
        subprocess.check_call([sys.executable, "-m", "PyInstaller"] + pyinstaller_args)
        print("[OK] 打包完成！")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] 打包失败: {e}")
        return False
    
    # 检查输出文件
    exe_name = f"{app_name}.exe"
    if os.path.exists(exe_name):
        file_size = os.path.getsize(exe_name) / (1024 * 1024)  # MB
        print(f"[OK] 生成文件: {exe_name} ({file_size:.1f} MB)")
    else:
        print("[ERROR] 未找到生成的可执行文件")
        return False
    
    # 清理构建文件
    if os.path.exists("build"):
        shutil.rmtree("build")
        print("[OK] 清理临时文件")
    
    # 创建发布包
    release_dir = f"准星程序_v1.1.1_发布包"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    
    os.makedirs(release_dir)
    
    # 复制文件到发布包
    files_to_copy = [
        exe_name,
        "README.md",
        "安装使用说明.txt", 
        "拖动功能使用说明.md",
        "预设加载功能修复报告.md",
    ]
    
    print(f"\n[INFO] 创建发布包: {release_dir}")
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(release_dir, file))
            print(f"[OK] 复制: {file}")
        else:
            print(f"[WARNING] 文件不存在: {file}")
    
    # 创建版本信息文件
    version_info = f"""准星程序 v1.1.1 版本信息

发布时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

新功能:
- 新增准星拖动功能，可以自由调整准星位置
- 新增拖动模式切换按钮
- 新增准星居中功能
- 新增实时坐标显示
- 智能位置保存和恢复

修复:
- 修复预设加载功能，确保所有参数正确加载
- 修复UI界面同步问题
- 修复空心十字参数丢失问题
- 优化配置文件路径处理

改进:
- 准星大小最小值调整为1（原为5）
- 提供更精细的准星大小控制
- 添加信号阻塞机制避免UI更新冲突
- 完善异常处理和错误提示

技术改进:
- 添加信号阻塞机制避免UI更新冲突
- 完善异常处理和错误提示
- 优化内存使用和性能

文件说明:
- 准星程序.exe: 主程序文件
- README.md: 程序说明文档
- 安装使用说明.txt: 安装和使用指南
- 拖动功能使用说明.md: 拖动功能详细说明
- 预设加载功能修复报告.md: 技术修复报告

作者: B站：林晓CCC
"""
    
    with open(os.path.join(release_dir, "版本说明_v1.1.1.txt"), "w", encoding="utf-8") as f:
        f.write(version_info)
    
    print("[OK] 创建版本说明文件")
    
    # 压缩发布包
    zip_name = f"准星程序_v1.1.1.zip"
    if os.path.exists(zip_name):
        os.remove(zip_name)
    
    print(f"\n[INFO] 压缩发布包: {zip_name}")
    shutil.make_archive(release_dir[:-4], "zip", release_dir)
    
    if os.path.exists(zip_name):
        zip_size = os.path.getsize(zip_name) / (1024 * 1024)  # MB
        print(f"[OK] 压缩完成: {zip_name} ({zip_size:.1f} MB)")
    
    print(f"\n[SUCCESS] 准星程序 v1.1.1 打包完成！")
    print(f"[INFO] 发布包位置: {os.path.abspath(release_dir)}")
    print(f"[INFO] 压缩包位置: {os.path.abspath(zip_name)}")
    
    return True

if __name__ == "__main__":
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 执行打包
    success = build_executable()
    
    if success:
        print("\n[SUCCESS] 打包成功！可以分发使用了。")
    else:
        print("\n[ERROR] 打包失败，请检查错误信息。")
        sys.exit(1)
