# src/views/visualization_views.py
import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# 导入必要的库
from datetime import datetime, date, timedelta
import random

from models.plant_models import MyPlants, GrowthRecords
from utils.window_utils import create_child_window

class VisualizationView:
    def __init__(self, parent):
        self.parent = parent
        self.my_plants_model = MyPlants()
        self.growth_records_model = GrowthRecords()
    
    def show_growth_tracking(self, plant_id=None):
        """显示生长追踪界面"""
        print(f"🔍 生长追踪入口，plant_id: {plant_id}")
        
        plants = self.my_plants_model.get_all_plants()
        if not plants:
            messagebox.showinfo("提示", "请先添加植物")
            return
        
        # 如果直接指定了plant_id，直接打开
        if plant_id is not None:
            plant = self._get_plant_by_id(plant_id)
            if plant:
                self._create_growth_tracker(plant['id'], plant['nickname'])
            else:
                messagebox.showerror("错误", "找不到指定的植物")
            return
        
        # 否则显示选择界面
        selection_window = create_child_window(self.parent, "选择植物", "500x600")
        
        ctk.CTkLabel(selection_window, 
                    text="🌱 选择要追踪的植物",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        scroll_frame = ctk.CTkScrollableFrame(selection_window)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 存储植物列表供回调使用
        self._plants_list = plants
        
        for i, plant in enumerate(plants):
            plant_card = ctk.CTkFrame(scroll_frame)
            plant_card.pack(fill="x", pady=8, padx=5)
            
            # 植物信息
            info_frame = ctk.CTkFrame(plant_card, fg_color="transparent")
            info_frame.pack(fill="x", padx=15, pady=10)
            
            # 左侧信息
            left_info = ctk.CTkFrame(info_frame, fg_color="transparent")
            left_info.pack(side="left", fill="x", expand=True)
            
            plant_name = f"🌿 {plant['nickname']} ({plant['species_name']})"
            ctk.CTkLabel(left_info, text=plant_name, 
                        font=ctk.CTkFont(weight="bold")).pack(anchor="w")
            
            status_text = f"📍 {plant['location']} | ❤️ {plant['health_status']} | 🌱 {plant['growth_stage']}"
            ctk.CTkLabel(left_info, text=status_text).pack(anchor="w", pady=(5,0))
            
            # 检查是否有生长记录
            growth_data = self.growth_records_model.get_plant_growth_records(plant['id'])
            record_count = len(growth_data) if growth_data else 0
            record_text = f"📊 已有 {record_count} 条生长记录"
            ctk.CTkLabel(left_info, text=record_text, 
                        text_color="#666666", font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(5,0))
            
            # 右侧按钮
            button_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            button_frame.pack(side="right")
            
            # 使用索引来避免闭包问题
            track_btn = ctk.CTkButton(button_frame, 
                                    text="生长追踪", 
                                    command=lambda idx=i: self._on_plant_selected(idx, selection_window),
                                    width=100, height=35)
            track_btn.pack(pady=5)
    
    def _on_plant_selected(self, plant_index, selection_window):
        """植物选择回调"""
        if hasattr(self, '_plants_list') and plant_index < len(self._plants_list):
            plant = self._plants_list[plant_index]
            print(f"🎯 用户选择了植物: {plant['nickname']} (ID: {plant['id']})")
            selection_window.destroy()
            self._create_growth_tracker(plant['id'], plant['nickname'])
        else:
            messagebox.showerror("错误", "植物选择失败")
    
    def _get_plant_by_id(self, plant_id):
        """根据ID获取植物信息"""
        plants = self.my_plants_model.get_all_plants()
        for plant in plants:
            if plant['id'] == plant_id:
                return plant
        return None
    
    def _create_growth_tracker(self, plant_id, plant_nickname):
        """创建生长追踪器界面"""
        print(f"🎨 创建生长追踪器: {plant_nickname} (ID: {plant_id})")
        
        tracker_window = create_child_window(self.parent, f"{plant_nickname} - 生长追踪", "1000x700")
        
        # 获取生长数据
        growth_data = self.growth_records_model.get_growth_statistics(plant_id)
        growth_records = self.growth_records_model.get_plant_growth_records(plant_id)
        
        print(f"📈 生长数据: {len(growth_records)} 条记录")
        
        # 创建选项卡视图
        tabview = ctk.CTkTabview(tracker_window)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 添加选项卡
        tabview.add("📈 生长图表")
        tabview.add("📊 生长统计") 
        tabview.add("➕ 记录生长")
        
        # 设置选项卡
        self._create_growth_charts_tab(tabview.tab("📈 生长图表"), plant_id, plant_nickname, growth_records)
        self._create_statistics_tab(tabview.tab("📊 生长统计"), growth_data, plant_nickname, len(growth_records))
        self._create_record_tab(tabview.tab("➕ 记录生长"), plant_id, plant_nickname, tracker_window)
    
    def _create_growth_charts_tab(self, parent, plant_id, plant_nickname, growth_records):
        """创建生长图表选项卡"""
        if not growth_records:
            ctk.CTkLabel(parent, text="暂无生长记录数据\n请在'记录生长'选项卡中添加数据", 
                        font=ctk.CTkFont(size=14)).pack(pady=100)
            return
        
        # 创建滚动框架
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 提取数据
        dates = []
        heights = []
        leaves = []
        health_scores = []
        
        for record in growth_records:
            # 处理日期
            record_date = record['record_date']
            if isinstance(record_date, str):
                record_date = datetime.strptime(record_date, '%Y-%m-%d')
            dates.append(record_date)
            
            # 处理数值数据
            if record.get('height_cm') is not None:
                heights.append(float(record['height_cm']))
            if record.get('leaf_count') is not None:
                leaves.append(int(record['leaf_count']))
            if record.get('health_score') is not None:
                health_scores.append(int(record['health_score']))
        
        # 高度图表
        if heights:
            height_frame = ctk.CTkFrame(scroll_frame)
            height_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(height_frame, 
                        text="📏 the curve of height",
                        font=ctk.CTkFont(weight="bold")).pack(pady=10)
            
            fig1, ax1 = plt.subplots(figsize=(10, 4))
            ax1.plot(dates[:len(heights)], heights, 'o-', color='#2E8B57', linewidth=2, markersize=6)
            ax1.set_title(f'{plant_nickname} - the curve of height', fontsize=14, fontweight='bold')
            ax1.set_ylabel('height (cm)', fontsize=12)
            ax1.grid(True, alpha=0.3)
            ax1.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            canvas1 = FigureCanvasTkAgg(fig1, height_frame)
            canvas1.draw()
            canvas1.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # 叶片数量图表
        if leaves:
            leaf_frame = ctk.CTkFrame(scroll_frame)
            leaf_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(leaf_frame, 
                        text="🍃 changes of leaves number",
                        font=ctk.CTkFont(weight="bold")).pack(pady=10)
            
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            ax2.plot(dates[:len(leaves)], leaves, 's-', color='#FF6B6B', linewidth=2, markersize=6)
            ax2.set_title('changes of leaves number', fontsize=14, fontweight='bold')
            ax2.set_ylabel('the number of leaves', fontsize=12)
            ax2.set_xlabel('date', fontsize=12)
            ax2.grid(True, alpha=0.3)
            ax2.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            canvas2 = FigureCanvasTkAgg(fig2, leaf_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # 健康评分图表
        if health_scores:
            health_frame = ctk.CTkFrame(scroll_frame)
            health_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(health_frame, 
                        text="❤️ trendy of health-score",
                        font=ctk.CTkFont(weight="bold")).pack(pady=10)
            
            fig3, ax3 = plt.subplots(figsize=(10, 4))
            ax3.plot(dates[:len(health_scores)], health_scores, '^-', color='#FFA500', linewidth=2, markersize=8)
            ax3.set_title('trendy of health-score', fontsize=14, fontweight='bold')
            ax3.set_ylabel('score of health (1-10)', fontsize=12)
            ax3.set_xlabel('date', fontsize=12)
            ax3.set_ylim(0, 10)
            ax3.grid(True, alpha=0.3)
            ax3.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            canvas3 = FigureCanvasTkAgg(fig3, health_frame)
            canvas3.draw()
            canvas3.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def _create_statistics_tab(self, parent, growth_data, plant_nickname, record_count):
        """创建生长统计选项卡"""
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(scroll_frame, 
                    text=f"📊 {plant_nickname} - 生长统计",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        if not growth_data or not growth_data['statistics'] or record_count == 0:
            ctk.CTkLabel(scroll_frame, text="暂无统计信息\n请先记录生长数据", 
                        font=ctk.CTkFont(size=14)).pack(pady=100)
            return
        
        stats = growth_data['statistics']
        
        # 统计信息卡片
        stats_cards = [
            ("总记录数", f"{stats['total_records']} 次", "📝"),
            ("记录时间范围", f"{stats['first_record']} 至 {stats['last_record']}", "📅"),
            ("平均高度", f"{float(stats['avg_height']):.1f} cm", "📏"),
            ("平均叶片数", f"{float(stats['avg_leaves']):.1f} 片", "🍃"),
            ("平均健康评分", f"{float(stats['avg_health']):.1f}/10", "❤️")
        ]
        
        for title, value, icon in stats_cards:
            card_frame = ctk.CTkFrame(scroll_frame)
            card_frame.pack(fill="x", padx=10, pady=5)
            
            content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
            content_frame.pack(fill="x", padx=15, pady=10)
            
            ctk.CTkLabel(content_frame, text=icon, font=ctk.CTkFont(size=20)).pack(side="left", padx=(0, 10))
            
            text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            text_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(text_frame, text=title, font=ctk.CTkFont(weight="bold")).pack(anchor="w")
            ctk.CTkLabel(text_frame, text=value).pack(anchor="w")
    
    def _create_record_tab(self, parent, plant_id, plant_nickname, tracker_window):
        """创建记录生长选项卡"""
        ctk.CTkLabel(parent, 
                    text=f"记录 {plant_nickname} 的生长数据",
                    font=ctk.CTkFont(weight="bold")).pack(pady=20)
        
        # 创建滚动框架
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 记录表单
        form_frame = ctk.CTkFrame(scroll_frame)
        form_frame.pack(pady=20, padx=50, fill="x")
        
        row = 0
        
        # 记录日期
        ctk.CTkLabel(form_frame, text="记录日期:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        date_entry = ctk.CTkEntry(form_frame, width=200, placeholder_text="YYYY-MM-DD")
        date_entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        row += 1
        
        # 高度
        ctk.CTkLabel(form_frame, text="高度 (cm):").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        height_entry = ctk.CTkEntry(form_frame, width=200, placeholder_text="例如：25.5")
        height_entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        row += 1
        
        # 宽度
        ctk.CTkLabel(form_frame, text="宽度 (cm):").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        width_entry = ctk.CTkEntry(form_frame, width=200, placeholder_text="例如：30.0")
        width_entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        row += 1
        
        # 叶片数量
        ctk.CTkLabel(form_frame, text="叶片数量:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        leaf_entry = ctk.CTkEntry(form_frame, width=200, placeholder_text="例如：15")
        leaf_entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        row += 1
        
        # 新叶数量
        ctk.CTkLabel(form_frame, text="新叶数量:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        new_leaf_entry = ctk.CTkEntry(form_frame, width=200, placeholder_text="例如：3")
        new_leaf_entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        row += 1
        
        # 健康评分
        ctk.CTkLabel(form_frame, text="健康评分 (1-10):").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        health_slider = ctk.CTkSlider(form_frame, from_=1, to=10, number_of_steps=9, width=200)
        health_slider.set(8)
        health_slider.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        
        health_value = ctk.CTkLabel(form_frame, text="8")
        health_value.grid(row=row, column=2, padx=10, pady=10)
        row += 1
        
        def update_health_value(value):
            health_value.configure(text=str(int(float(value))))
        
        health_slider.configure(command=update_health_value)
        
        # 观察记录
        ctk.CTkLabel(form_frame, text="观察记录:").grid(row=row, column=0, padx=10, pady=10, sticky="nw")
        observations_text = ctk.CTkTextbox(form_frame, width=300, height=100)
        observations_text.grid(row=row, column=1, columnspan=2, padx=10, pady=10, sticky="ew")
        observations_text.insert("1.0", "记录植物的生长变化、健康状况等...")
        
        # 配置网格权重
        form_frame.columnconfigure(1, weight=1)
        
        def save_growth_record():
            """保存生长记录"""
            try:
                # 验证日期
                record_date = date.today()
                if date_entry.get().strip():
                    record_date = datetime.strptime(date_entry.get().strip(), "%Y-%m-%d").date()
                
                # 验证数字字段
                height_cm = float(height_entry.get()) if height_entry.get().strip() else None
                width_cm = float(width_entry.get()) if width_entry.get().strip() else None
                leaf_count = int(leaf_entry.get()) if leaf_entry.get().strip() else None
                new_leaf_count = int(new_leaf_entry.get()) if new_leaf_entry.get().strip() else None
            except ValueError as e:
                messagebox.showerror("错误", f"请输入有效的数字或日期格式 (YYYY-MM-DD)")
                return
            
            # 至少需要填写一项数据
            if not any([height_cm, width_cm, leaf_count, new_leaf_count]):
                messagebox.showerror("错误", "请至少填写一项生长数据")
                return
            
            record_data = {
                'plant_id': plant_id,
                'record_date': record_date,
                'height_cm': height_cm,
                'width_cm': width_cm,
                'leaf_count': leaf_count,
                'new_leaf_count': new_leaf_count,
                'health_score': int(health_slider.get()),
                'observations': observations_text.get("1.0", "end-1c").strip()
            }
            
            if self.growth_records_model.add_growth_record(record_data):
                messagebox.showinfo("成功", "生长记录保存成功！")
                # 清空表单（保留日期）
                height_entry.delete(0, 'end')
                width_entry.delete(0, 'end')
                leaf_entry.delete(0, 'end')
                new_leaf_entry.delete(0, 'end')
                observations_text.delete("1.0", "end")
                health_slider.set(8)
                health_value.configure(text="8")
                
                # 刷新追踪器以显示新数据
                tracker_window.destroy()
                self.show_growth_tracking(plant_id)
            else:
                messagebox.showerror("错误", "保存生长记录失败，请重试")
        
        def add_sample_data():
            """快速添加示例生长数据"""
            base_height = 15.0
            base_leaves = 8
            
            for i in range(5):  # 添加5条示例记录
                record_date = datetime.now() - timedelta(days=20 - i * 5)
                
                # 模拟生长
                height_growth = random.uniform(0.2, 0.8)
                leaf_growth = random.randint(0, 2)
                
                base_height += height_growth
                base_leaves += leaf_growth
                
                record_data = {
                    'plant_id': plant_id,
                    'record_date': record_date.date(),
                    'height_cm': round(base_height, 1),
                    'leaf_count': base_leaves,
                    'new_leaf_count': leaf_growth,
                    'health_score': random.randint(7, 10),
                    'observations': '示例生长数据'
                }
                
                self.growth_records_model.add_growth_record(record_data)
            
            messagebox.showinfo("成功", "已添加5条示例生长记录！")
            tracker_window.destroy()
            self.show_growth_tracking(plant_id)
        
        # 按钮框架
        button_frame = ctk.CTkFrame(scroll_frame)
        button_frame.pack(pady=20)
        
        save_btn = ctk.CTkButton(button_frame, text="💾 保存记录", command=save_growth_record, width=120)
        save_btn.pack(side="left", padx=10)
        
        sample_btn = ctk.CTkButton(button_frame, text="🎲 添加示例数据", 
                                  command=add_sample_data, width=120)
        sample_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(button_frame, text="❌ 关闭", 
                                 command=tracker_window.destroy, width=120)
        cancel_btn.pack(side="left", padx=10)