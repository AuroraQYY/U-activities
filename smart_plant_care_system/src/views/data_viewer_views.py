# src/views/data_viewer_views.py
import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import Config
from utils.window_utils import create_child_window

class DataViewerView:
    def __init__(self, parent):
        self.parent = parent
    
    def show_data_viewer(self):
        """显示图形化数据查看器"""
        viewer_window = create_child_window(self.parent, "📊 数据查看器", "1000x700")
        
        # 创建选项卡
        tabview = ctk.CTkTabview(viewer_window)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        tabview.add("植物品种")
        tabview.add("我的植物")
        tabview.add("养护记录")
        tabview.add("生长记录")
        
        # 植物品种选项卡
        self._create_species_tab(tabview.tab("植物品种"))
        
        # 我的植物选项卡
        self._create_plants_tab(tabview.tab("我的植物"))
        
        # 养护记录选项卡
        self._create_care_logs_tab(tabview.tab("养护记录"))
        
        # 生长记录选项卡
        self._create_growth_records_tab(tabview.tab("生长记录"))
    
    def _create_species_tab(self, parent):
        """创建植物品种选项卡"""
        try:
            conn = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                port=Config.MYSQL_PORT
            )
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM plant_species ORDER BY name")
            species = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            if not species:
                ctk.CTkLabel(parent, text="暂无植物品种数据").pack(pady=50)
                return
            
            # 创建滚动框架
            scroll_frame = ctk.CTkScrollableFrame(parent)
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # 表头
            headers = ["ID", "名称", "学名", "类型", "难度", "光照", "浇水频率"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(scroll_frame, text=header, font=ctk.CTkFont(weight="bold")).grid(
                    row=0, column=i, padx=10, pady=5, sticky="w"
                )
            
            # 数据行
            for row, s in enumerate(species, 1):
                ctk.CTkLabel(scroll_frame, text=str(s['id'])).grid(
                    row=row, column=0, padx=10, pady=2, sticky="w"
                )
                ctk.CTkLabel(scroll_frame, text=s['name']).grid(
                    row=row, column=1, padx=10, pady=2, sticky="w"
                )
                ctk.CTkLabel(scroll_frame, text=s.get('scientific_name', '')).grid(
                    row=row, column=2, padx=10, pady=2, sticky="w"
                )
                ctk.CTkLabel(scroll_frame, text=s['plant_type']).grid(
                    row=row, column=3, padx=10, pady=2, sticky="w"
                )
                ctk.CTkLabel(scroll_frame, text=s['difficulty_level']).grid(
                    row=row, column=4, padx=10, pady=2, sticky="w"
                )
                ctk.CTkLabel(scroll_frame, text=s['light_requirements']).grid(
                    row=row, column=5, padx=10, pady=2, sticky="w"
                )
                watering_text = f"夏{s['watering_frequency_summer']}天/冬{s['watering_frequency_winter']}天"
                ctk.CTkLabel(scroll_frame, text=watering_text).grid(
                    row=row, column=6, padx=10, pady=2, sticky="w"
                )
            
        except Exception as e:
            ctk.CTkLabel(parent, text=f"数据库错误: {e}").pack(pady=50)
    
    def _create_plants_tab(self, parent):
        """创建我的植物选项卡"""
        try:
            conn = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                port=Config.MYSQL_PORT
            )
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT mp.*, ps.name as species_name 
                FROM my_plants mp 
                JOIN plant_species ps ON mp.species_id = ps.id 
                ORDER BY mp.nickname
            """)
            plants = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            if not plants:
                ctk.CTkLabel(parent, text="暂无植物数据").pack(pady=50)
                return
            
            # 创建滚动框架
            scroll_frame = ctk.CTkScrollableFrame(parent)
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # 表头
            headers = ["ID", "昵称", "品种", "位置", "健康状态", "生长阶段", "最后浇水"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(scroll_frame, text=header, font=ctk.CTkFont(weight="bold")).grid(
                    row=0, column=i, padx=10, pady=5, sticky="w"
                )
            
            # 数据行
            for row, p in enumerate(plants, 1):
                ctk.CTkLabel(scroll_frame, text=str(p['id'])).grid(
                    row=row, column=0, padx=10, pady=2, sticky="w"
                )
                ctk.CTkLabel(scroll_frame, text=p['nickname']).grid(
                    row=row, column=1, padx=10, pady=2, sticky="w"
                )
                ctk.CTkLabel(scroll_frame, text=p['species_name']).grid(
                    row=row, column=2, padx=10, pady=2, sticky="w"
                )
                ctk.CTkLabel(scroll_frame, text=p['location']).grid(
                    row=row, column=3, padx=10, pady=2, sticky="w"
                )
                
                # 健康状态（带颜色）
                health_color = {
                    '非常健康': '#2E8B57',
                    '健康': '#32CD32', 
                    '一般': '#FFA500',
                    '需关注': '#FF6B6B',
                    '生病': '#DC143C',
                    '濒危': '#8B0000'
                }.get(p['health_status'], '#000000')
                
                health_label = ctk.CTkLabel(scroll_frame, text=p['health_status'], text_color=health_color)
                health_label.grid(row=row, column=4, padx=10, pady=2, sticky="w")
                
                ctk.CTkLabel(scroll_frame, text=p['growth_stage']).grid(
                    row=row, column=5, padx=10, pady=2, sticky="w"
                )
                
                last_watered = p['last_watered'] if p['last_watered'] else "从未浇水"
                ctk.CTkLabel(scroll_frame, text=str(last_watered)).grid(
                    row=row, column=6, padx=10, pady=2, sticky="w"
                )
            
        except Exception as e:
            ctk.CTkLabel(parent, text=f"数据库错误: {e}").pack(pady=50)
    
    def _create_care_logs_tab(self, parent):
        """创建养护记录选项卡"""
        try:
            conn = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                port=Config.MYSQL_PORT
            )
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT cl.*, mp.nickname as plant_nickname, ps.name as species_name
                FROM care_logs cl
                JOIN my_plants mp ON cl.plant_id = mp.id
                JOIN plant_species ps ON mp.species_id = ps.id
                ORDER BY cl.care_date DESC
                LIMIT 50
            """)
            care_logs = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            if not care_logs:
                ctk.CTkLabel(parent, text="暂无养护记录").pack(pady=50)
                return
            
            # 创建滚动框架
            scroll_frame = ctk.CTkScrollableFrame(parent)
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # 表头
            headers = ["ID", "植物", "养护类型", "时间", "详情", "效果"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(scroll_frame, text=header, font=ctk.CTkFont(weight="bold")).grid(
                    row=0, column=i, padx=10, pady=5, sticky="w"
                )
            
            # 数据行
            for row, log in enumerate(care_logs, 1):
                ctk.CTkLabel(scroll_frame, text=str(log['id'])).grid(
                    row=row, column=0, padx=10, pady=2, sticky="w"
                )
                
                plant_text = f"{log['plant_nickname']}({log['species_name']})"
                ctk.CTkLabel(scroll_frame, text=plant_text).grid(
                    row=row, column=1, padx=10, pady=2, sticky="w"
                )
                
                ctk.CTkLabel(scroll_frame, text=log['care_type']).grid(
                    row=row, column=2, padx=10, pady=2, sticky="w"
                )
                
                ctk.CTkLabel(scroll_frame, text=str(log['care_date'])[:16]).grid(
                    row=row, column=3, padx=10, pady=2, sticky="w"
                )
                
                details = log.get('details', '')[:20] + "..." if len(log.get('details', '')) > 20 else log.get('details', '')
                ctk.CTkLabel(scroll_frame, text=details).grid(
                    row=row, column=4, padx=10, pady=2, sticky="w"
                )
                
                effect = log.get('observed_effect', '无变化')
                ctk.CTkLabel(scroll_frame, text=effect).grid(
                    row=row, column=5, padx=10, pady=2, sticky="w"
                )
            
        except Exception as e:
            ctk.CTkLabel(parent, text=f"数据库错误: {e}").pack(pady=50)
    
    def _create_growth_records_tab(self, parent):
        """创建生长记录选项卡"""
        try:
            conn = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                port=Config.MYSQL_PORT
            )
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT gr.*, mp.nickname as plant_nickname
                FROM growth_records gr
                JOIN my_plants mp ON gr.plant_id = mp.id
                ORDER BY gr.record_date DESC
                LIMIT 50
            """)
            growth_records = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            if not growth_records:
                ctk.CTkLabel(parent, text="暂无生长记录").pack(pady=50)
                return
            
            # 创建滚动框架
            scroll_frame = ctk.CTkScrollableFrame(parent)
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # 表头
            headers = ["ID", "植物", "记录日期", "高度(cm)", "叶片数", "健康评分"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(scroll_frame, text=header, font=ctk.CTkFont(weight="bold")).grid(
                    row=0, column=i, padx=10, pady=5, sticky="w"
                )
            
            # 数据行
            for row, record in enumerate(growth_records, 1):
                ctk.CTkLabel(scroll_frame, text=str(record['id'])).grid(
                    row=row, column=0, padx=10, pady=2, sticky="w"
                )
                
                ctk.CTkLabel(scroll_frame, text=record['plant_nickname']).grid(
                    row=row, column=1, padx=10, pady=2, sticky="w"
                )
                
                ctk.CTkLabel(scroll_frame, text=str(record['record_date'])).grid(
                    row=row, column=2, padx=10, pady=2, sticky="w"
                )
                
                height = record.get('height_cm', '无')
                ctk.CTkLabel(scroll_frame, text=str(height)).grid(
                    row=row, column=3, padx=10, pady=2, sticky="w"
                )
                
                leaves = record.get('leaf_count', '无')
                ctk.CTkLabel(scroll_frame, text=str(leaves)).grid(
                    row=row, column=4, padx=10, pady=2, sticky="w"
                )
                
                health = record.get('health_score', '无')
                ctk.CTkLabel(scroll_frame, text=str(health)).grid(
                    row=row, column=5, padx=10, pady=2, sticky="w"
                )
            
        except Exception as e:
            ctk.CTkLabel(parent, text=f"数据库错误: {e}").pack(pady=50)