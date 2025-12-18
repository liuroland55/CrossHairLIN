#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QPainter, QColor, QBrush, QPen


class OverlayWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        
        # 拖动相关变量
        self.is_drag_mode = False
        self.is_dragging = False
        self.drag_start_pos = QPoint()
        self.crosshair_pos = None  # 准星的当前位置
        
        # 设置窗口属性
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # 无边框
            Qt.WindowStaysOnTopHint |  # 置顶
            Qt.Tool  # 工具窗口
        )
        
        # 设置窗口透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # 设置全屏
        self.showFullScreen()
        
        # 初始化鼠标穿透
        self.setMouseTracking(False)
        self.setWindowFlag(Qt.WindowTransparentForInput, True)
        
        # 定时器用于重绘
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # 20 FPS
    
    def updateConfig(self, config):
        """更新配置"""
        self.config = config
        # 重置crosshair_pos，让准星位置跟随配置
        self.crosshair_pos = None
        self.update()
    
    def center_crosshair(self):
        """将准星居中"""
        screen_size = QApplication.primaryScreen().size()
        self.crosshair_pos = QPoint(screen_size.width() // 2, screen_size.height() // 2)
        self.config["position"] = {"x": "center", "y": "center"}
        self.update()
    
    def draw_cross(self, painter, center, size, thickness, color):
        """绘制十字准星"""
        painter.setPen(QPen(color, thickness))
        painter.drawLine(center[0] - size, center[1], center[0] + size, center[1])  # 水平线
        painter.drawLine(center[0], center[1] - size, center[0], center[1] + size)  # 垂直线
    
    def draw_dot(self, painter, center, size, color):
        """绘制圆点准星"""
        painter.setPen(QPen(color, 1))
        painter.setBrush(QBrush(color))
        painter.drawEllipse(center[0], center[1], size, size)
    
    def draw_square(self, painter, center, size, color):
        """绘制方块准星"""
        painter.setPen(QPen(color, 2))
        painter.setBrush(QBrush(color))
        painter.drawRect(center[0] - size//2, center[1] - size//2, size, size)
    
    def draw_circle(self, painter, center, size, color):
        """绘制圆圈准星"""
        painter.setPen(QPen(color, 2))
        painter.setBrush(QBrush(Qt.transparent))
        painter.drawEllipse(center[0], center[1], size, size)
    
    def draw_triangle(self, painter, center, size, color):
        """绘制三角形准星"""
        painter.setPen(QPen(color, 2))
        painter.setBrush(QBrush(color))
        
        # 计算三角形顶点
        points = [
            (center[0], center[1] - size),  # 顶点
            (center[0] - size, center[1] + size),  # 左下角
            (center[0] + size, center[1] + size)   # 右下角
        ]
        
        # 绘制三角形
        from PySide6.QtCore import QPoint
        from PySide6.QtGui import QPolygon
        
        polygon = QPolygon([QPoint(p[0], p[1]) for p in points])
        painter.drawPolygon(polygon)
    
    def draw_hollow_cross(self, painter, center, gap_size, line_length, line_thickness, color):
        """绘制空心十字准星"""
        painter.setPen(QPen(color, line_thickness))
        
        # 绘制四段分离的直线
        # 上半部分
        painter.drawLine(center[0], center[1] - gap_size, center[0], center[1] - gap_size - line_length)
        # 下半部分
        painter.drawLine(center[0], center[1] + gap_size, center[0], center[1] + gap_size + line_length)
        # 左半部分
        painter.drawLine(center[0] - gap_size, center[1], center[0] - gap_size - line_length, center[1])
        # 右半部分
        painter.drawLine(center[0] + gap_size, center[1], center[0] + gap_size + line_length, center[1])
    
    def draw_hollow_square(self, painter, center, size, thickness, color):
        """绘制空心方框准星"""
        painter.setPen(QPen(color, thickness))
        painter.setBrush(QBrush(Qt.transparent))
        painter.drawRect(center[0] - size//2, center[1] - size//2, size, size)
    
    def draw_hollow_cross_dot(self, painter, center, gap_size, line_length, line_thickness, dot_size, color):
        """绘制空心十字加中心点准星"""
        # 先绘制空心十字
        self.draw_hollow_cross(painter, center, gap_size, line_length, line_thickness, color)
        
        # 再绘制中心点
        painter.setPen(QPen(color, 1))
        painter.setBrush(QBrush(color))
        painter.drawEllipse(center[0], center[1], dot_size, dot_size)
    
    def toggleDragMode(self):
        """切换拖动模式"""
        self.is_drag_mode = not self.is_drag_mode
        
        if self.is_drag_mode:
            # 进入拖动模式：禁用鼠标穿透，启用鼠标跟踪
            self.setWindowFlag(Qt.WindowTransparentForInput, False)
            self.setMouseTracking(True)
            self.setCursor(Qt.OpenHandCursor)
            
            # 初始化准星位置
            if self.crosshair_pos is None:
                screen_size = QApplication.primaryScreen().size()
                position = self.config.get("position", {"x": "center", "y": "center"})
                if position["x"] == "center":
                    center_x = screen_size.width() // 2
                else:
                    center_x = int(position["x"])
                
                if position["y"] == "center":
                    center_y = screen_size.height() // 2
                else:
                    center_y = int(position["y"])
                
                self.crosshair_pos = QPoint(center_x, center_y)
        else:
            # 退出拖动模式：启用鼠标穿透，禁用鼠标跟踪
            self.setWindowFlag(Qt.WindowTransparentForInput, True)
            self.setMouseTracking(False)
            self.setCursor(Qt.ArrowCursor)
        
        # 重新显示窗口以应用窗口标志更改
        self.hide()
        self.showFullScreen()
        
        return self.is_drag_mode
    
    def get_crosshair_position(self):
        """获取准星当前位置"""
        if self.crosshair_pos:
            return (self.crosshair_pos.x(), self.crosshair_pos.y())
        else:
            # 如果没有拖动过，返回配置中的位置
            position = self.config.get("position", {"x": "center", "y": "center"})
            if position["x"] == "center" and position["y"] == "center":
                screen_size = QApplication.primaryScreen().size()
                return (screen_size.width() // 2, screen_size.height() // 2)
            else:
                return (int(position["x"]), int(position["y"]))
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if self.is_drag_mode and event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_start_pos = event.position().toPoint()
            self.setCursor(Qt.ClosedHandCursor)
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if self.is_drag_mode and event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.setCursor(Qt.OpenHandCursor)
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.is_drag_mode and self.is_dragging:
            # 计算移动距离
            current_pos = event.position().toPoint()
            delta = current_pos - self.drag_start_pos
            
            # 更新准星位置
            if self.crosshair_pos:
                self.crosshair_pos += delta
            
            # 更新拖动起始位置
            self.drag_start_pos = current_pos
            
            # 更新配置中的位置
            if self.crosshair_pos:
                self.config["position"] = {
                    "x": self.crosshair_pos.x(), 
                    "y": self.crosshair_pos.y()
                }
            
            # 触发重绘
            self.update()
    
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 获取配置参数
        shape = self.config.get("shape", "cross")
        size = self.config.get("size", 20)
        thickness = self.config.get("thickness", 2)
        opacity = self.config.get("opacity", 0.8)
        color = self.config.get("color", "#FF0000")
        position = self.config.get("position", {"x": "center", "y": "center"})
        
        # 设置颜色和透明度
        qcolor = QColor(color)
        qcolor.setAlphaF(opacity)
        
        # 计算中心位置
        if self.is_drag_mode and self.crosshair_pos:
            # 在拖动模式下，使用拖动后的位置
            center_x = self.crosshair_pos.x()
            center_y = self.crosshair_pos.y()
        else:
            # 正常模式下，使用配置中的位置
            screen_size = QApplication.primaryScreen().size()
            if position["x"] == "center":
                center_x = screen_size.width() // 2
            else:
                center_x = int(position["x"])
            
            if position["y"] == "center":
                center_y = screen_size.height() // 2
            else:
                center_y = int(position["y"])
        
        center = (center_x, center_y)
        
        # 根据形状绘制准星
        if shape == "cross":
            self.draw_cross(painter, center, size, thickness, qcolor)
        elif shape == "dot":
            self.draw_dot(painter, center, size, qcolor)
        elif shape == "square":
            self.draw_square(painter, center, size, qcolor)
        elif shape == "circle":
            self.draw_circle(painter, center, size, qcolor)
        elif shape == "triangle":
            self.draw_triangle(painter, center, size, qcolor)
        elif shape == "hollow_cross":
            gap_size = self.config.get("hollow_gap", size // 3)
            line_length = self.config.get("hollow_length", size)
            line_thickness = self.config.get("hollow_thickness", thickness)
            self.draw_hollow_cross(painter, center, gap_size, line_length, line_thickness, qcolor)
        elif shape == "hollow_square":
            self.draw_hollow_square(painter, center, size, thickness, qcolor)
        elif shape == "hollow_cross_dot":
            gap_size = self.config.get("hollow_gap", size // 3)
            line_length = self.config.get("hollow_length", size)
            line_thickness = self.config.get("hollow_thickness", thickness)
            dot_size = self.config.get("center_dot_size", 3)
            self.draw_hollow_cross_dot(painter, center, gap_size, line_length, line_thickness, dot_size, qcolor)
        
        # 在拖动模式下绘制额外的提示信息
        if self.is_drag_mode:
            # 绘制拖动模式提示
            painter.setPen(QPen(QColor(255, 255, 255, 128), 1))
            painter.setFont(painter.font())  # 使用默认字体
            hint_text = "拖动模式 - 拖动准星到想要的位置"
            text_rect = painter.boundingRect(10, 10, 300, 30, Qt.AlignLeft, hint_text)
            painter.fillRect(text_rect.adjusted(-5, -5, 5, 5), QColor(0, 0, 0, 128))
            painter.drawText(10, 10, hint_text)
