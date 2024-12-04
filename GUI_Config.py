from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QTabWidget, QTableWidget, QTableWidgetItem,
                           QComboBox, QMessageBox, QGroupBox)
from PyQt5.QtCore import Qt
import json
import os

class ConfigWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("API服务器配置")
        self.setGeometry(100, 100, 800, 600)
        
        # 变量映射字典
        self.var_mappings = {
            "Type": {
                "DT": "大田作物",
                "WS": "温室作物"
            }
            # 可以添加更多映射
        }
        
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建选项卡
        tabs = QTabWidget()
        
        # API配置选项卡
        api_tab = QWidget()
        api_layout = QVBoxLayout(api_tab)
        
        # IP和端口配置
        ip_group = QGroupBox("API服务器配置")
        ip_layout = QVBoxLayout()
        
        ip_input = QHBoxLayout()
        ip_input.addWidget(QLabel("IP地址:"))
        self.ip_edit = QLineEdit("0.0.0.0")
        ip_input.addWidget(self.ip_edit)
        
        port_input = QHBoxLayout()
        port_input.addWidget(QLabel("端口:"))
        self.port_edit = QLineEdit("6017")
        port_input.addWidget(self.port_edit)
        
        self.start_btn = QPushButton("启动服务器")
        self.start_btn.clicked.connect(self.toggle_server)
        
        ip_layout.addLayout(ip_input)
        ip_layout.addLayout(port_input)
        ip_layout.addWidget(self.start_btn)
        ip_group.setLayout(ip_layout)
        api_layout.addWidget(ip_group)
        
        # 数据库操作选项卡
        db_tab = QWidget()
        db_layout = QVBoxLayout(db_tab)
        
        # 数据库文件选择
        db_select = QHBoxLayout()
        db_select.addWidget(QLabel("选择数据库:"))
        self.db_combo = QComboBox()
        self.load_db_files()
        db_select.addWidget(self.db_combo)
        db_layout.addLayout(db_select)
        
        # 数据表格
        self.table = QTableWidget()
        db_layout.addWidget(self.table)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("添加")
        edit_btn = QPushButton("修改")
        delete_btn = QPushButton("删除")
        save_btn = QPushButton("保存")
        
        add_btn.clicked.connect(self.add_row)
        edit_btn.clicked.connect(self.edit_row)
        delete_btn.clicked.connect(self.delete_row)
        save_btn.clicked.connect(self.save_db)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(save_btn)
        db_layout.addLayout(btn_layout)
        
        # 添加选项卡
        tabs.addTab(api_tab, "API配置")
        tabs.addTab(db_tab, "数据库管理")
        
        layout.addWidget(tabs)
        
        # 连接信号
        self.db_combo.currentTextChanged.connect(self.load_db_data)
        
    def load_db_files(self):
        """加载DB文件夹下的所有json文件"""
        self.db_combo.clear()
        db_path = "./DB"
        if os.path.exists(db_path):
            for file in os.listdir(db_path):
                if file.endswith('.json'):
                    self.db_combo.addItem(file)
                    
    def load_db_data(self):
        """加载选中的数据库文件内容到表格"""
        current_db = self.db_combo.currentText()
        if not current_db:
            return
            
        try:
            with open(f"./DB/{current_db}", 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 设置表格
            if isinstance(data, list):
                if data:
                    headers = list(data[0].keys())
                    self.table.setColumnCount(len(headers))
                    self.table.setHorizontalHeaderLabels(headers)
                    self.table.setRowCount(len(data))
                    
                    for row, item in enumerate(data):
                        for col, key in enumerate(headers):
                            value = item.get(key, '')
                            # 检查是否需要进行变量映射转换
                            if key in self.var_mappings:
                                for db_val, display_val in self.var_mappings[key].items():
                                    if value == db_val:
                                        value = display_val
                                        break
                            
                            cell = QTableWidgetItem(str(value))
                            self.table.setItem(row, col, cell)
                            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"加载数据库失败: {str(e)}")
            
    def toggle_server(self):
        """切换服务器状态"""
        if self.start_btn.text() == "启动服务器":
            # 获取配置的IP和端口
            ip = self.ip_edit.text()
            port = self.port_edit.text()
            
            # TODO: 实现服务器启动逻辑
            
            self.start_btn.setText("停止服务器")
        else:
            # TODO: 实现服务器停止逻辑
            
            self.start_btn.setText("启动服务器")
            
    def add_row(self):
        """添加新行"""
        current_row = self.table.rowCount()
        self.table.insertRow(current_row)
        
    def edit_row(self):
        """编辑选中的行"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择要编辑的行")
            return
            
        # TODO: 实现编辑逻辑
        
    def delete_row(self):
        """删除选中的行"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择要删除的行")
            return
            
        self.table.removeRow(current_row)
        
    def save_db(self):
        """保存数据到json文件"""
        current_db = self.db_combo.currentText()
        if not current_db:
            return
            
        try:
            data = []
            for row in range(self.table.rowCount()):
                row_data = {}
                for col in range(self.table.columnCount()):
                    header = self.table.horizontalHeaderItem(col).text()
                    value = self.table.item(row, col).text()
                    
                    # 检查是否需要进行变量映射转换回数据库值
                    if header in self.var_mappings:
                        for db_val, display_val in self.var_mappings[header].items():
                            if value == display_val:
                                value = db_val
                                break
                                
                    row_data[header] = value
                data.append(row_data)
                
            with open(f"./DB/{current_db}", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            QMessageBox.information(self, "成功", "数据保存成功")
            
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存数据失败: {str(e)}") 