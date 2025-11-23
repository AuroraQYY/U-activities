# src/main.py
import sys
import os

# 修复导入路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

print(f"当前目录: {current_dir}")
print(f"父目录: {parent_dir}")

import customtkinter as ctk
from tkinter import messagebox
from views.data_viewer_views import DataViewerView

# 现在导入应该可以工作了
try:
    from models.plant_models import PlantSpecies, MyPlants
    from views.plant_views import PlantManagementView
    from views.care_views import CareManagementView
    from views.visualization_views import VisualizationView
    from views.species_views import SpeciesManagementView
    from views.report_views import ReportView
    print("✅ 所有模块导入成功！")
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    # 如果还是失败，使用备用方案
    from src.models.plant_models import PlantSpecies, MyPlants
    from src.views.plant_views import PlantManagementView
    from src.views.care_views import CareManagementView
    from src.views.visualization_views import VisualizationView
    from src.views.species_views import SpeciesManagementView
    from src.views.report_views import ReportView

# 设置主题
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class PlantCareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌿 智能家庭植物养护管理系统")
        self.root.geometry("900x700")
        
        # 初始化数据模型
        self.plant_species_model = PlantSpecies()
        self.my_plants_model = MyPlants()
        
        # 初始化视图
        self.plant_view = PlantManagementView(root)
        self.care_view = CareManagementView(root)
        self.visualization_view = VisualizationView(root)
        self.species_view = SpeciesManagementView(root)
        self.report_view = ReportView(root)
        self.data_viewer = DataViewerView(root)
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面 - 添加滚动条版本"""
        # 创建主滚动框架
        main_scroll = ctk.CTkScrollableFrame(self.root)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 主框架
        main_frame = ctk.CTkFrame(main_scroll)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ctk.CTkLabel(main_frame, 
                                  text="🌿 智能家庭植物养护管理系统", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)
        
        # 功能按钮框架
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=30)
        
        # 第一行按钮 - 数据库和基础功能
        test_db_btn = ctk.CTkButton(button_frame, 
                                   text="测试数据库连接", 
                                   command=self.test_database, 
                                   width=200, 
                                   height=40)
        test_db_btn.grid(row=0, column=0, padx=15, pady=10)
        
        view_species_btn = ctk.CTkButton(button_frame, 
                                        text="查看植物品种", 
                                        command=self.view_species, 
                                        width=200, 
                                        height=40)
        view_species_btn.grid(row=0, column=1, padx=15, pady=10)
        
        # 第二行按钮 - 植物管理
        add_species_btn = ctk.CTkButton(button_frame, 
                                       text="添加植物品种", 
                                       command=self.add_species, 
                                       width=200, 
                                       height=40)
        add_species_btn.grid(row=1, column=0, padx=15, pady=10)
        
        add_plant_btn = ctk.CTkButton(button_frame, 
                                     text="添加我的植物", 
                                     command=self.add_plant, 
                                     width=200, 
                                     height=40)
        add_plant_btn.grid(row=1, column=1, padx=15, pady=10)
        
        # 第三行按钮 - 查看功能
        view_plants_btn = ctk.CTkButton(button_frame, 
                                       text="查看我的植物", 
                                       command=self.view_plants, 
                                       width=200, 
                                       height=40)
        view_plants_btn.grid(row=2, column=0, padx=15, pady=10)
        
        view_data_btn = ctk.CTkButton(button_frame, 
                                     text="查看数据", 
                                     command=self.view_database_data, 
                                     width=200, 
                                     height=40)
        view_data_btn.grid(row=2, column=1, padx=15, pady=10)
        
        # 第四行按钮 - 养护管理
        care_reminders_btn = ctk.CTkButton(button_frame, 
                                          text="养护提醒", 
                                          command=self.show_care_reminders, 
                                          width=200, 
                                          height=40)
        care_reminders_btn.grid(row=3, column=0, padx=15, pady=10)
        
        care_history_btn = ctk.CTkButton(button_frame, 
                                        text="养护历史", 
                                        command=self.show_care_history, 
                                        width=200, 
                                        height=40)
        care_history_btn.grid(row=3, column=1, padx=15, pady=10)
        
        # 第五行按钮 - 生长追踪
        growth_tracking_btn = ctk.CTkButton(button_frame, 
                                           text="生长追踪", 
                                           command=self.show_growth_tracking, 
                                           width=200, 
                                           height=40)
        growth_tracking_btn.grid(row=4, column=0, padx=15, pady=10)
        
        # 在按钮框架中添加养护中心按钮
        care_center_btn = ctk.CTkButton(button_frame, 
                                    text="🏥 养护中心", 
                                    command=self.show_care_center, 
                                    width=200, height=40)
        care_center_btn.grid(row=4, column=1, padx=15, pady=10)     

        # 第六行按钮 - 报表功能
        smart_reminders_btn = ctk.CTkButton(button_frame, 
                                           text="智能提醒", 
                                           command=self.show_smart_reminders, 
                                           width=200, 
                                           height=40)
        smart_reminders_btn.grid(row=5, column=0, padx=15, pady=10)
        
        reports_btn = ctk.CTkButton(button_frame, 
                                   text="报表中心", 
                                   command=self.show_reports, 
                                   width=200, 
                                   height=40)
        reports_btn.grid(row=5, column=1, padx=15, pady=10)
        
        # 第七行按钮 - 管理功能
        manage_species_btn = ctk.CTkButton(button_frame, 
                                        text="🌿 管理品种", 
                                        command=self.manage_species, 
                                        width=200, height=40)
        manage_species_btn.grid(row=6, column=0, padx=15, pady=10)
        
        manage_plants_btn = ctk.CTkButton(button_frame, 
                                        text="🏡 管理植物", 
                                        command=self.manage_plants, 
                                        width=200, height=40)
        manage_plants_btn.grid(row=6, column=1, padx=15, pady=10)

        # 状态显示
        self.status_label = ctk.CTkLabel(main_frame, 
                                        text="系统就绪", 
                                        text_color="green")
        self.status_label.pack(pady=20)
        
        # 快速操作提示
        tips_frame = ctk.CTkFrame(main_frame)
        tips_frame.pack(pady=10)
        
        tips_label = ctk.CTkLabel(tips_frame, 
                                 text="💡 提示：首次使用请先运行数据库初始化脚本",
                                 font=ctk.CTkFont(size=12))
        tips_label.pack(pady=5)
        
        # 版权信息
        copyright_label = ctk.CTkLabel(main_frame, 
                                      text="© 2025 智能植物养护系统 - 开发版本 1.0", 
                                      font=ctk.CTkFont(size=10))
        copyright_label.pack(side="bottom", pady=10)
    
    def test_database(self):
        """测试数据库连接"""
        try:
            species = self.plant_species_model.get_all_species()
            plants = self.my_plants_model.get_all_plants()
            
            messagebox.showinfo("测试成功", 
                              f"✅ 数据库连接正常！\n"
                              f"📊 找到 {len(species)} 个植物品种\n"
                              f"🌿 找到 {len(plants)} 株我的植物")
            self.status_label.configure(text="数据库连接正常", text_color="green")
        except Exception as e:
            messagebox.showerror("测试失败", f"❌ 数据库连接失败：{str(e)}")
            self.status_label.configure(text="数据库连接失败", text_color="red")
    
    def view_species(self):
        """查看植物品种"""
        species = self.plant_species_model.get_all_species()
        if species:
            species_info = "🌿 植物品种库 🌿\n\n"
            for s in species:
                species_info += f"📗 {s['name']} ({s['scientific_name']})\n"
                species_info += f"   类型: {s['plant_type']} | 难度: {s['difficulty_level']}\n"
                species_info += f"   光照: {s['light_requirements']} | 浇水: 夏{s['watering_frequency_summer']}天/冬{s['watering_frequency_winter']}天\n"
                species_info += f"   描述: {s['description'][:50]}...\n\n"
            
            # 创建滚动文本框显示
            species_window = ctk.CTkToplevel(self.root)
            species_window.title("植物品种库")
            species_window.geometry("600x500")
            
            textbox = ctk.CTkTextbox(species_window, width=550, height=400)
            textbox.pack(padx=20, pady=20)
            textbox.insert("1.0", species_info)
            textbox.configure(state="disabled")  # 设置为只读
            
        else:
            messagebox.showinfo("植物品种", "暂无植物品种数据，请先添加基础数据")
    
    def add_species(self):
        """添加植物品种"""
        self.species_view.show_add_species_dialog()
    
    def add_plant(self):
        """添加我的植物"""
        self.plant_view.show_add_plant_dialog()
    
    def view_plants(self):
        """查看我的植物"""
        self.plant_view.show_plants_list()
    
    def view_database_data(self):
        """查看数据库数据"""
        self.data_viewer.show_data_viewer()
    
    def show_care_reminders(self):
        """显示养护提醒"""
        self.care_view.show_care_reminders()
    
    def show_care_history(self):
        """显示养护历史"""
        self.care_view.show_care_history()
    
    def show_growth_tracking(self):
        """显示生长追踪"""
        self.visualization_view.show_growth_tracking()
    
    def show_smart_reminders(self):
        """显示智能提醒"""
        self.report_view.show_smart_reminders()
    
    def show_reports(self):
        """显示报表中心"""
        self.report_view.show_report_dashboard()
    
    def check_auto_reminders(self):
        """启动时自动检查提醒"""
        try:
            # 这里可以添加自动检查逻辑
            pass
        except Exception as e:
            print(f"自动检查提醒错误: {e}")

    def show_care_center(self):
        """显示养护中心"""
        self.care_view.show_care_center()   

    def manage_species(self):
        """管理植物品种"""
        self.species_view.show_species_management()

    def manage_plants(self):
        """管理我的植物"""
        self.plant_view.show_plants_list()

def main():
    # 创建主窗口
    root = ctk.CTk()
    
    # 创建应用程序实例
    app = PlantCareApp(root)
    
    # 启动时自动检查提醒
    root.after(1000, app.check_auto_reminders)  # 1秒后执行
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main()