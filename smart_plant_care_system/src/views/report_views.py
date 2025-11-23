# src/views/report_views.py
import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, date, timedelta
from utils.reminder_engine import SmartReminderEngine
from utils.window_utils import create_child_window
from models.plant_models import MyPlants, CareLogs, PlantSpecies
from utils.report_exporter import ReportExporter
class ReportView:
    def __init__(self, parent):
        self.parent = parent
        self.reminder_engine = SmartReminderEngine()
        self.my_plants_model = MyPlants()
        self.care_logs_model = CareLogs()
        self.plant_species_model = PlantSpecies()
        self.report_exporter = ReportExporter()
    
    def show_smart_reminders(self):
        """Show Smart Reminders Interface"""
        reminders_window = create_child_window(self.parent, "🔔 Smart Reminders Center", "900x700")
        
        # Header and Statistics
        header_frame = ctk.CTkFrame(reminders_window, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(header_frame, text="🔔 Smart Reminders Center", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        
        def refresh_reminders():
            """Refresh reminders list"""
            for widget in main_scroll.winfo_children():
                widget.destroy()
            load_reminders_data()
        
        refresh_btn = ctk.CTkButton(header_frame, text="🔄 Refresh", 
                                  command=refresh_reminders, width=80)
        refresh_btn.pack(side="right", padx=10)
        
        # Main scroll frame
        main_scroll = ctk.CTkScrollableFrame(reminders_window)
        main_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        def load_reminders_data():
            """Load reminders data"""
            # Get statistics
            stats = self.reminder_engine.get_reminder_statistics()
            
            # Statistics card
            stats_frame = ctk.CTkFrame(main_scroll)
            stats_frame.pack(fill="x", pady=10, padx=5)
            
            stats_text = f"📊 Reminder Stats: Total {stats['total']} reminders | "
            stats_text += f"⚠️ Urgent {stats['urgent']} | "
            stats_text += f"🔶 Medium {stats['medium']} | "
            stats_text += f"💚 Low {stats['low']}"
            
            ctk.CTkLabel(stats_frame, text=stats_text, 
                        font=ctk.CTkFont(weight="bold")).pack(pady=10)
            
            # Get reminders list
            reminders = self.reminder_engine.get_smart_reminders()
            
            if not reminders:
                no_reminders_frame = ctk.CTkFrame(main_scroll)
                no_reminders_frame.pack(fill="x", pady=20, padx=5)
                
                ctk.CTkLabel(no_reminders_frame, 
                           text="🎉 Great! No pending reminders",
                           font=ctk.CTkFont(size=14, weight="bold")).pack(pady=20)
                ctk.CTkLabel(no_reminders_frame, 
                           text="Your plants are well cared for!",
                           text_color="#666666").pack(pady=5)
                return
            
            # Display reminders list
            for reminder in reminders:
                reminder_card = ctk.CTkFrame(main_scroll)
                reminder_card.pack(fill="x", pady=8, padx=5)
                
                # Set color based on urgency
                urgency_color = {
                    'Emergency': '#DC143C',
                    'High': '#FF6B6B',
                    'Medium': '#FFA500',
                    'Low': '#2E8B57'
                }.get(reminder['urgency'], '#000000')
                
                # Reminder header
                header_frame = ctk.CTkFrame(reminder_card, fg_color="transparent")
                header_frame.pack(fill="x", padx=15, pady=10)
                
                # Left info
                left_info = ctk.CTkFrame(header_frame, fg_color="transparent")
                left_info.pack(side="left", fill="x", expand=True)
                
                # Reminder type and plant name
                type_text = f"{reminder['type']} - {reminder['plant_name']}"
                ctk.CTkLabel(left_info, text=type_text, 
                            font=ctk.CTkFont(weight="bold")).pack(anchor="w")
                
                # Reminder message
                ctk.CTkLabel(left_info, text=reminder['message']).pack(anchor="w", pady=(5,0))
                
                # Suggested action
                action_text = f"💡 Suggestion: {reminder['suggested_action']}"
                ctk.CTkLabel(left_info, text=action_text, 
                            text_color="#666666", font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(5,0))
                
                # Right status and actions
                right_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
                right_frame.pack(side="right")
                
                # Urgency level
                urgency_label = ctk.CTkLabel(right_frame, text=reminder['urgency'],
                                           text_color=urgency_color, font=ctk.CTkFont(weight="bold"))
                urgency_label.pack(anchor="e")
                
                # Action button (for specific plant reminders)
                if reminder['plant_id']:
                    action_btn = ctk.CTkButton(right_frame, text="Handle Now",
                                             command=lambda pid=reminder['plant_id']: self._handle_reminder(pid, refresh_reminders),
                                             width=80, height=30)
                    action_btn.pack(pady=(5,0))
        
        # Initial data load
        load_reminders_data()
    
    def _handle_reminder(self, plant_id, refresh_callback):
        """Handle reminder - open care center"""
        from views.care_views import CareManagementView
        care_view = CareManagementView(self.parent)
        care_view.show_care_center()
    
    def show_report_dashboard(self):
        """Show Report Dashboard"""
        dashboard_window = create_child_window(self.parent, "📊 Report Center", "1100x750")
        
        # Create tabs
        tabview = ctk.CTkTabview(dashboard_window)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        tabview.add("📈 Care Statistics")
        tabview.add("🌿 Plant Health")
        tabview.add("💰 Cost Analysis")
        tabview.add("📅 Monthly Report")
        
        # Initialize tabs
        self._create_care_statistics_tab(tabview.tab("📈 Care Statistics"))
        self._create_plant_health_tab(tabview.tab("🌿 Plant Health"))
        self._create_cost_analysis_tab(tabview.tab("💰 Cost Analysis"))
        self._create_monthly_report_tab(tabview.tab("📅 Monthly Report"))
    
    def _create_care_statistics_tab(self, parent):
        """Create Care Statistics Tab"""
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(scroll_frame, text="📈 Care Statistics Analysis", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        # Get care statistics data
        care_stats = self._get_care_statistics()
        
        # Overall statistics cards
        overall_frame = ctk.CTkFrame(scroll_frame)
        overall_frame.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(overall_frame, text="📊 Overall Statistics", 
                    font=ctk.CTkFont(weight="bold", size=14)).pack(pady=10)
        
        stats_grid = ctk.CTkFrame(overall_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=20, pady=10)
        
        stats_data = [
            ("Total Plants", f"{care_stats['total_plants']} plants", "🌿"),
            ("Care Records", f"{care_stats['total_care_logs']} times", "📝"),
            ("Avg Health Score", f"{care_stats['avg_health_score']:.1f}/10", "❤️"),
            ("Active Plants", f"{care_stats['active_plants']} plants", "✅")
        ]
        
        for i, (title, value, icon) in enumerate(stats_data):
            stat_frame = ctk.CTkFrame(stats_grid)
            stat_frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="ew")
            
            ctk.CTkLabel(stat_frame, text=icon, font=ctk.CTkFont(size=20)).pack(side="left", padx=10)
            text_frame = ctk.CTkFrame(stat_frame, fg_color="transparent")
            text_frame.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(text_frame, text=title, font=ctk.CTkFont(weight="bold")).pack(anchor="w")
            ctk.CTkLabel(text_frame, text=value).pack(anchor="w")
        
        stats_grid.columnconfigure(0, weight=1)
        stats_grid.columnconfigure(1, weight=1)
        
        # Care type distribution chart
        if care_stats['care_type_distribution']:
            type_frame = ctk.CTkFrame(scroll_frame)
            type_frame.pack(fill="x", pady=20, padx=5)
            
            ctk.CTkLabel(type_frame, text="🔧 Care Type Distribution", 
                        font=ctk.CTkFont(weight="bold", size=14)).pack(pady=10)
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=(8, 6))
            care_types = list(care_stats['care_type_distribution'].keys())
            counts = list(care_stats['care_type_distribution'].values())
            
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
            wedges, texts, autotexts = ax.pie(counts, labels=care_types, autopct='%1.1f%%', 
                                            colors=colors[:len(care_types)], startangle=90)
            
            # Style text
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            ax.set_title('Care Type Distribution', fontsize=14, fontweight='bold')
            
            canvas = FigureCanvasTkAgg(fig, type_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=10)
        
        # Monthly care trend
        if care_stats['monthly_trend']:
            trend_frame = ctk.CTkFrame(scroll_frame)
            trend_frame.pack(fill="x", pady=20, padx=5)
            
            ctk.CTkLabel(trend_frame, text="📅 Monthly Care Trend", 
                        font=ctk.CTkFont(weight="bold", size=14)).pack(pady=10)
            
            # Create bar chart
            fig, ax = plt.subplots(figsize=(10, 5))
            months = list(care_stats['monthly_trend'].keys())
            counts = list(care_stats['monthly_trend'].values())
            
            bars = ax.bar(months, counts, color='#2E8B57', alpha=0.7)
            ax.set_title('Monthly Care Activities', fontsize=14, fontweight='bold')
            ax.set_ylabel('Care Count')
            ax.tick_params(axis='x', rotation=45)
            
            # Display values on bars
            for bar, count in zip(bars, counts):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{count}', ha='center', va='bottom')
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, trend_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=10)
    
    def _create_plant_health_tab(self, parent):
        """Create Plant Health Tab"""
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(scroll_frame, text="🌿 Plant Health Analysis", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        # Get plant health data
        health_data = self._get_plant_health_data()
        
        # Health status distribution
        if health_data['health_distribution']:
            dist_frame = ctk.CTkFrame(scroll_frame)
            dist_frame.pack(fill="x", pady=10, padx=5)
            
            ctk.CTkLabel(dist_frame, text="❤️ Health Status Distribution", 
                        font=ctk.CTkFont(weight="bold", size=14)).pack(pady=10)
            
            # Create health status pie chart
            fig, ax = plt.subplots(figsize=(8, 6))
            statuses = list(health_data['health_distribution'].keys())
            counts = list(health_data['health_distribution'].values())
            
            # Set colors based on health status
            color_map = {
                'Very Healthy': '#2E8B57',
                'Healthy': '#32CD32',
                'Average': '#FFA500',
                'Needs Attention': '#FF6B6B',
                'Sick': '#DC143C',
                'Critical': '#8B0000'
            }
            colors = [color_map.get(status, '#666666') for status in statuses]
            
            wedges, texts, autotexts = ax.pie(counts, labels=statuses, autopct='%1.1f%%', 
                                            colors=colors, startangle=90)
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            ax.set_title('Plant Health Status Distribution', fontsize=14, fontweight='bold')
            
            canvas = FigureCanvasTkAgg(fig, dist_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=10)
        
        # Plants needing care list
        if health_data['plants_need_care']:
            care_frame = ctk.CTkFrame(scroll_frame)
            care_frame.pack(fill="x", pady=20, padx=5)
            
            ctk.CTkLabel(care_frame, text="⚠️ Plants Needing Attention", 
                        font=ctk.CTkFont(weight="bold", size=14)).pack(pady=10)
            
            for plant in health_data['plants_need_care']:
                plant_card = ctk.CTkFrame(care_frame)
                plant_card.pack(fill="x", pady=5, padx=10)
                
                info_frame = ctk.CTkFrame(plant_card, fg_color="transparent")
                info_frame.pack(fill="x", padx=15, pady=10)
                
                plant_text = f"🌿 {plant['nickname']} ({plant['species_name']})"
                ctk.CTkLabel(info_frame, text=plant_text, 
                            font=ctk.CTkFont(weight="bold")).pack(anchor="w")
                
                status_text = f"Health: {plant['health_status']} | Location: {plant['location']}"
                status_color = '#DC143C' if plant['health_status'] in ['Sick', 'Critical'] else '#FFA500'
                ctk.CTkLabel(info_frame, text=status_text, text_color=status_color).pack(anchor="w", pady=(5,0))
                
                if plant.get('last_watered'):
                    water_text = f"Last Watered: {plant['last_watered']}"
                    ctk.CTkLabel(info_frame, text=water_text, 
                                text_color="#666666", font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2,0))
    
    def _create_cost_analysis_tab(self, parent):
        """Create Cost Analysis Tab"""
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(scroll_frame, text="💰 Cost Analysis", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        # Get cost data
        cost_data = self._get_cost_analysis_data()
        
        # Cost statistics
        cost_frame = ctk.CTkFrame(scroll_frame)
        cost_frame.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(cost_frame, text="💵 Cost Statistics", 
                    font=ctk.CTkFont(weight="bold", size=14)).pack(pady=10)
        
        cost_stats = [
            ("Total Investment", f"¥{cost_data['total_investment']:.2f}", "💰"),
            ("Avg Cost per Plant", f"¥{cost_data['avg_cost_per_plant']:.2f}", "🌿"),
            ("Most Expensive Plant", f"¥{cost_data['most_expensive_plant']['cost']:.2f}" if cost_data['most_expensive_plant'] else "None", "⭐"),
            ("Plant Count", f"{cost_data['plant_count']} plants", "📊")
        ]
        
        stats_frame = ctk.CTkFrame(cost_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        for i, (title, value, icon) in enumerate(cost_stats):
            stat_card = ctk.CTkFrame(stats_frame)
            stat_card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="ew")
            
            ctk.CTkLabel(stat_card, text=icon, font=ctk.CTkFont(size=18)).pack(side="left", padx=10)
            text_frame = ctk.CTkFrame(stat_card, fg_color="transparent")
            text_frame.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(text_frame, text=title, font=ctk.CTkFont(weight="bold")).pack(anchor="w")
            ctk.CTkLabel(text_frame, text=value).pack(anchor="w")
        
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        
        # Plant value distribution
        if cost_data['plants_with_cost']:
            value_frame = ctk.CTkFrame(scroll_frame)
            value_frame.pack(fill="x", pady=20, padx=5)
            
            ctk.CTkLabel(value_frame, text="📊 Plant Value Distribution", 
                        font=ctk.CTkFont(weight="bold", size=14)).pack(pady=10)
            
            # Create bar chart
            fig, ax = plt.subplots(figsize=(10, 6))
            plants = [p['nickname'] for p in cost_data['plants_with_cost']]
            costs = [p['cost'] for p in cost_data['plants_with_cost']]
            
            bars = ax.bar(plants, costs, color='#4ECDC4', alpha=0.7)
            ax.set_title('Plant Purchase Costs', fontsize=14, fontweight='bold')
            ax.set_ylabel('Cost (¥)')
            ax.tick_params(axis='x', rotation=45)
            
            # Display values on bars
            for bar, cost in zip(bars, costs):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'¥{cost:.1f}', ha='center', va='bottom', fontsize=9)
            
            plt.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, value_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=10)
    
    
    

 # 在 _create_monthly_report_tab 方法中修改，添加导出按钮：
    def _create_monthly_report_tab(self, parent):
        """创建月度报告选项卡 - 添加导出功能"""
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(scroll_frame, text="📅 月度报告", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        # 月度选择
        month_frame = ctk.CTkFrame(scroll_frame)
        month_frame.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(month_frame, text="选择月份:").pack(side="left", padx=10, pady=10)
        month_var = ctk.StringVar(value=datetime.now().strftime('%Y-%m'))
        month_entry = ctk.CTkEntry(month_frame, textvariable=month_var, width=120)
        month_entry.pack(side="left", padx=10, pady=10)
        
        # 格式选择
        format_frame = ctk.CTkFrame(scroll_frame)
        format_frame.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(format_frame, text="导出格式:").pack(side="left", padx=10, pady=10)
        format_var = ctk.StringVar(value="excel")
        format_combo = ctk.CTkComboBox(format_frame, 
                                     values=self.report_exporter.get_export_formats(),
                                     variable=format_var, width=120)
        format_combo.pack(side="left", padx=10, pady=10)
        
        # 导出按钮框架
        export_frame = ctk.CTkFrame(scroll_frame)
        export_frame.pack(fill="x", pady=20, padx=5)
        
        def export_care_report():
            """导出养护统计报告"""
            filepath = self.report_exporter.export_care_statistics(format_var.get())
            if filepath:
                messagebox.showinfo("导出成功", f"养护统计报告已导出到:\n{filepath}")
            else:
                messagebox.showerror("导出失败", "导出养护统计报告失败")
        
        def export_health_report():
            """导出健康报告"""
            filepath = self.report_exporter.export_health_report(format_var.get())
            if filepath:
                messagebox.showinfo("导出成功", f"健康报告已导出到:\n{filepath}")
            else:
                messagebox.showerror("导出失败", "导出健康报告失败")
        
        def export_monthly_report():
            """导出月度报告"""
            filepath = self.report_exporter.export_monthly_report(month_var.get(), format_var.get())
            if filepath:
                messagebox.showinfo("导出成功", f"月度报告已导出到:\n{filepath}")
            else:
                messagebox.showerror("导出失败", "导出月度报告失败")
        
        # 导出按钮
        care_export_btn = ctk.CTkButton(export_frame, text="📊 导出养护统计", 
                                      command=export_care_report, width=150, height=35)
        care_export_btn.pack(side="left", padx=10, pady=10)
        
        health_export_btn = ctk.CTkButton(export_frame, text="❤️ 导出健康报告", 
                                        command=export_health_report, width=150, height=35)
        health_export_btn.pack(side="left", padx=10, pady=10)
        
        monthly_export_btn = ctk.CTkButton(export_frame, text="📅 导出月度报告", 
                                         command=export_monthly_report, width=150, height=35)
        monthly_export_btn.pack(side="left", padx=10, pady=10)
        
        # 原有的月度报告内容...
        monthly_data = self._get_monthly_report_data()
        
        # 月度摘要
        summary_frame = ctk.CTkFrame(scroll_frame)
        summary_frame.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(summary_frame, text="📋 月度摘要", 
                    font=ctk.CTkFont(weight="bold", size=14)).pack(pady=10)
        
        summary_text = f"""报告月份: {monthly_data['report_month']}

植物状态:
• 总植物数量: {monthly_data['plant_count']} 株
• 新增植物: {monthly_data['new_plants']} 株  
• 健康植物: {monthly_data['healthy_plants']} 株
• 需关注植物: {monthly_data['plants_need_care']} 株

养护活动:
• 总养护次数: {monthly_data['total_care_actions']} 次
• 浇水次数: {monthly_data['watering_count']} 次
• 施肥次数: {monthly_data['fertilizing_count']} 次
• 其他养护: {monthly_data['other_care_count']} 次

生长记录:
• 新增生长记录: {monthly_data['growth_records']} 条
• 平均健康评分: {monthly_data['avg_health_score']:.1f}/10
"""
        
        textbox = ctk.CTkTextbox(summary_frame, width=800, height=250)
        textbox.pack(padx=20, pady=10)
        textbox.insert("1.0", summary_text)
        textbox.configure(state="disabled")



    def _get_care_statistics(self):
        """Get care statistics data"""
        # This should get real data from database
        # Returning mock data for now
        return {
            'total_plants': 8,
            'total_care_logs': 45,
            'avg_health_score': 8.2,
            'active_plants': 7,
            'care_type_distribution': {
                'Watering': 25,
                'Fertilizing': 8,
                'Pruning': 5,
                'Leaf Cleaning': 4,
                'Repotting': 2,
                'Other': 1
            },
            'monthly_trend': {
                'Jan': 12,
                'Feb': 15,
                'Mar': 18
            }
        }
    
    def _get_plant_health_data(self):
        """Get plant health data"""
        plants = self.my_plants_model.get_all_plants()
        
        # Translate health status to English
        status_translation = {
            '非常健康': 'Very Healthy',
            '健康': 'Healthy',
            '一般': 'Average',
            '需关注': 'Needs Attention',
            '生病': 'Sick',
            '濒危': 'Critical'
        }
        
        health_distribution = {}
        plants_need_care = []
        
        for plant in plants:
            original_status = plant['health_status']
            status = status_translation.get(original_status, original_status)
            health_distribution[status] = health_distribution.get(status, 0) + 1
            
            if status in ['Needs Attention', 'Sick', 'Critical']:
                plants_need_care.append(plant)
        
        return {
            'health_distribution': health_distribution,
            'plants_need_care': plants_need_care
        }
    
    def _get_cost_analysis_data(self):
        """Get cost analysis data"""
        plants = self.my_plants_model.get_all_plants()
        
        plants_with_cost = []
        total_investment = 0
        
        for plant in plants:
            cost = plant.get('purchase_price', 0) or 0
            if cost > 0:
                plants_with_cost.append({
                    'nickname': plant['nickname'],
                    'cost': float(cost)
                })
                total_investment += float(cost)
        
        # Find most expensive plant
        most_expensive = max(plants_with_cost, key=lambda x: x['cost']) if plants_with_cost else None
        
        return {
            'total_investment': total_investment,
            'avg_cost_per_plant': total_investment / len(plants) if plants else 0,
            'most_expensive_plant': most_expensive,
            'plant_count': len(plants),
            'plants_with_cost': plants_with_cost
        }
    
    def _get_monthly_report_data(self):
        """Get monthly report data"""
        current_month = datetime.now().strftime('%Y-%m')
        plants = self.my_plants_model.get_all_plants()
        
        # Translate health status for counting
        status_translation = {
            '非常健康': 'Very Healthy',
            '健康': 'Healthy',
            '一般': 'Average',
            '需关注': 'Needs Attention',
            '生病': 'Sick',
            '濒危': 'Critical'
        }
        
        # Count plants needing care
        plants_need_care = len([p for p in plants if p['health_status'] in ['需关注', '生病', '濒危']])
        healthy_plants = len([p for p in plants if p['health_status'] in ['非常健康', '健康']])
        
        return {
            'report_month': current_month,
            'plant_count': len(plants),
            'new_plants': 2,  # Mock data
            'healthy_plants': healthy_plants,
            'plants_need_care': plants_need_care,
            'total_care_actions': 18,  # Mock data
            'watering_count': 12,
            'fertilizing_count': 3,
            'other_care_count': 3,
            'growth_records': 8,  # Mock data
            'avg_health_score': 8.2
        }
    

    