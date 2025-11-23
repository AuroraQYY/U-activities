# src/views/species_views.py
import customtkinter as ctk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.plant_models import PlantSpecies
from utils.window_utils import create_child_window
from models.plant_models import MyPlants
class SpeciesManagementView:
    def __init__(self, parent):
        self.parent = parent
        self.plant_species_model = PlantSpecies()
    
    def show_add_species_dialog(self):
        """显示添加植物品种对话框"""
        dialog = create_child_window(self.parent, "添加植物品种", "600x700")
        
        # 创建主滚动框架
        main_scroll = ctk.CTkScrollableFrame(dialog)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 标题
        ctk.CTkLabel(main_scroll, text="🌿 添加新植物品种", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)
        
        # === 基本信息 ===
        basic_frame = ctk.CTkFrame(main_scroll)
        basic_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(basic_frame, text="📋 基本信息", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        # 植物名称
        ctk.CTkLabel(basic_frame, text="植物名称 *").pack(anchor="w", pady=5)
        name_entry = ctk.CTkEntry(basic_frame, placeholder_text="例如：绿萝")
        name_entry.pack(fill="x", pady=5)
        
        # 学名和科属在一行
        name_row = ctk.CTkFrame(basic_frame, fg_color="transparent")
        name_row.pack(fill="x", pady=5)
        
        ctk.CTkLabel(name_row, text="学名").pack(side="left", anchor="w", padx=(0, 10))
        scientific_name_entry = ctk.CTkEntry(name_row, placeholder_text="例如：Epipremnum aureum")
        scientific_name_entry.pack(side="left", fill="x", expand=True, padx=(0, 20))
        
        ctk.CTkLabel(name_row, text="科属").pack(side="left", anchor="w", padx=(0, 10))
        family_entry = ctk.CTkEntry(name_row, placeholder_text="例如：天南星科")
        family_entry.pack(side="left", fill="x", expand=True)
        
        # 植物类型和难度在一行
        type_row = ctk.CTkFrame(basic_frame, fg_color="transparent")
        type_row.pack(fill="x", pady=5)
        
        ctk.CTkLabel(type_row, text="植物类型").pack(side="left", anchor="w", padx=(0, 10))
        plant_type_var = ctk.StringVar(value="观叶植物")
        plant_type_combo = ctk.CTkComboBox(type_row, 
                                        values=["观叶植物", "开花植物", "多肉植物", "果蔬", "草本植物", "乔木", "灌木"],
                                        variable=plant_type_var, width=150)
        plant_type_combo.pack(side="left", padx=(0, 20))
        
        ctk.CTkLabel(type_row, text="养护难度").pack(side="left", anchor="w", padx=(0, 10))
        difficulty_var = ctk.StringVar(value="中等")
        difficulty_combo = ctk.CTkComboBox(type_row, 
                                        values=["非常简单", "简单", "中等", "困难", "专家级"],
                                        variable=difficulty_var, width=150)
        difficulty_combo.pack(side="left")
        
        # === 养护要求 ===
        care_frame = ctk.CTkFrame(main_scroll)
        care_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(care_frame, text="💧 养护要求", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        # 光照和毒性在一行
        light_toxicity_row = ctk.CTkFrame(care_frame, fg_color="transparent")
        light_toxicity_row.pack(fill="x", pady=5)
        
        ctk.CTkLabel(light_toxicity_row, text="光照需求").pack(side="left", anchor="w", padx=(0, 10))
        light_var = ctk.StringVar(value="中光照")
        light_combo = ctk.CTkComboBox(light_toxicity_row, 
                                    values=["强光", "中光照", "弱光", "耐阴"],
                                    variable=light_var, width=120)
        light_combo.pack(side="left", padx=(0, 20))
        
        ctk.CTkLabel(light_toxicity_row, text="毒性").pack(side="left", anchor="w", padx=(0, 10))
        toxicity_var = ctk.StringVar(value="无毒")
        toxicity_combo = ctk.CTkComboBox(light_toxicity_row, 
                                    values=["无毒", "微毒", "有毒", "剧毒"],
                                    variable=toxicity_var, width=120)
        toxicity_combo.pack(side="left")
        
        # 浇水频率
        watering_frame = ctk.CTkFrame(care_frame, fg_color="transparent")
        watering_frame.pack(fill="x", pady=8)
        
        ctk.CTkLabel(watering_frame, text="浇水频率").pack(anchor="w", pady=5)
        
        watering_sub = ctk.CTkFrame(watering_frame, fg_color="transparent")
        watering_sub.pack(fill="x", pady=5)
        
        ctk.CTkLabel(watering_sub, text="夏季").pack(side="left", padx=5)
        summer_water_entry = ctk.CTkEntry(watering_sub, width=60, placeholder_text="7")
        summer_water_entry.pack(side="left", padx=5)
        summer_water_entry.insert(0, "7")
        ctk.CTkLabel(watering_sub, text="天/次").pack(side="left", padx=5)
        
        ctk.CTkLabel(watering_sub, text="冬季").pack(side="left", padx=(20,5))
        winter_water_entry = ctk.CTkEntry(watering_sub, width=60, placeholder_text="14")
        winter_water_entry.pack(side="left", padx=5)
        winter_water_entry.insert(0, "14")
        ctk.CTkLabel(watering_sub, text="天/次").pack(side="left", padx=5)
        
        # 施肥和换盆频率
        fert_repot_frame = ctk.CTkFrame(care_frame, fg_color="transparent")
        fert_repot_frame.pack(fill="x", pady=8)
        
        ctk.CTkLabel(fert_repot_frame, text="施肥频率").pack(side="left", anchor="w", padx=(0, 10))
        fertilizing_entry = ctk.CTkEntry(fert_repot_frame, width=80, placeholder_text="30")
        fertilizing_entry.pack(side="left", padx=(0, 20))
        fertilizing_entry.insert(0, "30")
        ctk.CTkLabel(fert_repot_frame, text="天/次").pack(side="left", padx=5)
        
        ctk.CTkLabel(fert_repot_frame, text="换盆频率").pack(side="left", anchor="w", padx=(20, 10))
        repotting_entry = ctk.CTkEntry(fert_repot_frame, width=80, placeholder_text="12")
        repotting_entry.pack(side="left", padx=(0, 5))
        repotting_entry.insert(0, "12")
        ctk.CTkLabel(fert_repot_frame, text="月/次").pack(side="left", padx=5)
        
        # 温度和湿度要求
        temp_humidity_frame = ctk.CTkFrame(care_frame, fg_color="transparent")
        temp_humidity_frame.pack(fill="x", pady=8)
        
        # 温度
        temp_frame = ctk.CTkFrame(temp_humidity_frame, fg_color="transparent")
        temp_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(temp_frame, text="适宜温度").pack(anchor="w")
        temp_sub = ctk.CTkFrame(temp_frame, fg_color="transparent")
        temp_sub.pack(fill="x", pady=5)
        
        temp_min_entry = ctk.CTkEntry(temp_sub, width=60, placeholder_text="15")
        temp_min_entry.pack(side="left", padx=2)
        temp_min_entry.insert(0, "15")
        ctk.CTkLabel(temp_sub, text="~").pack(side="left", padx=2)
        temp_max_entry = ctk.CTkEntry(temp_sub, width=60, placeholder_text="30")
        temp_max_entry.pack(side="left", padx=2)
        temp_max_entry.insert(0, "30")
        ctk.CTkLabel(temp_sub, text="℃").pack(side="left", padx=2)
        
        # 湿度
        humidity_frame = ctk.CTkFrame(temp_humidity_frame, fg_color="transparent")
        humidity_frame.pack(side="left", fill="x", expand=True, padx=(20,0))
        
        ctk.CTkLabel(humidity_frame, text="适宜湿度").pack(anchor="w")
        humidity_sub = ctk.CTkFrame(humidity_frame, fg_color="transparent")
        humidity_sub.pack(fill="x", pady=5)
        
        humidity_min_entry = ctk.CTkEntry(humidity_sub, width=60, placeholder_text="40")
        humidity_min_entry.pack(side="left", padx=2)
        humidity_min_entry.insert(0, "40")
        ctk.CTkLabel(humidity_sub, text="~").pack(side="left", padx=2)
        humidity_max_entry = ctk.CTkEntry(humidity_sub, width=60, placeholder_text="70")
        humidity_max_entry.pack(side="left", padx=2)
        humidity_max_entry.insert(0, "70")
        ctk.CTkLabel(humidity_sub, text="%").pack(side="left", padx=2)
        
        # === 描述信息 ===
        desc_frame = ctk.CTkFrame(main_scroll)
        desc_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(desc_frame, text="📝 描述信息", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        # 植物描述
        ctk.CTkLabel(desc_frame, text="植物描述").pack(anchor="w", pady=5)
        description_text = ctk.CTkTextbox(desc_frame, height=70)
        description_text.pack(fill="x", pady=5)
        description_text.insert("1.0", "请描述植物的外观特征、生长习性等...")
        
        # 养护技巧
        ctk.CTkLabel(desc_frame, text="养护技巧").pack(anchor="w", pady=(15,5))
        care_tips_text = ctk.CTkTextbox(desc_frame, height=60)
        care_tips_text.pack(fill="x", pady=5)
        care_tips_text.insert("1.0", "请提供具体的养护方法和技巧...")
        
        # 常见问题
        ctk.CTkLabel(desc_frame, text="常见问题").pack(anchor="w", pady=(15,5))
        common_problems_text = ctk.CTkTextbox(desc_frame, height=60)
        common_problems_text.pack(fill="x", pady=5)
        common_problems_text.insert("1.0", "请列出养护中可能遇到的常见问题及解决方法...")
        
        def save_species():
            """保存植物品种"""
            # 验证必填字段
            if not name_entry.get().strip():
                messagebox.showerror("错误", "请填写植物名称")
                return
            
            # 验证数字字段
            try:
                summer_water = int(summer_water_entry.get()) if summer_water_entry.get().strip() else 7
                winter_water = int(winter_water_entry.get()) if winter_water_entry.get().strip() else 14
                fertilizing = int(fertilizing_entry.get()) if fertilizing_entry.get().strip() else 30
                repotting = int(repotting_entry.get()) if repotting_entry.get().strip() else 12
                
                temp_min = int(temp_min_entry.get()) if temp_min_entry.get().strip() else None
                temp_max = int(temp_max_entry.get()) if temp_max_entry.get().strip() else None
                humidity_min = int(humidity_min_entry.get()) if humidity_min_entry.get().strip() else None
                humidity_max = int(humidity_max_entry.get()) if humidity_max_entry.get().strip() else None
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")
                return
            
            species_data = {
                'name': name_entry.get().strip(),
                'scientific_name': scientific_name_entry.get().strip(),
                'family': family_entry.get().strip(),
                'plant_type': plant_type_var.get(),
                'difficulty_level': difficulty_var.get(),
                'light_requirements': light_var.get(),
                'optimal_temperature_min': temp_min,
                'optimal_temperature_max': temp_max,
                'ideal_humidity_min': humidity_min,
                'ideal_humidity_max': humidity_max,
                'watering_frequency_summer': summer_water,
                'watering_frequency_winter': winter_water,
                'fertilizing_frequency': fertilizing,
                'repotting_frequency': repotting,
                'description': description_text.get("1.0", "end-1c").strip(),
                'care_tips': care_tips_text.get("1.0", "end-1c").strip(),
                'common_problems': common_problems_text.get("1.0", "end-1c").strip(),
                'toxicity': toxicity_var.get()
            }
            
            if self.plant_species_model.add_species(species_data):
                messagebox.showinfo("成功", "🌿 植物品种添加成功！")
                dialog.destroy()
            else:
                messagebox.showerror("错误", "添加植物品种失败，请重试")
        
        # === 按钮 ===
        button_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
        button_frame.pack(pady=20)
        
        save_btn = ctk.CTkButton(button_frame, text="💾 保存品种", 
                            command=save_species, 
                            width=120, height=35,
                            fg_color="#2E8B57", hover_color="#3CB371")
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(button_frame, text="❌ 取消", 
                                command=dialog.destroy, 
                                width=120, height=35,
                                fg_color="#DC143C", hover_color="#FF6B6B")
        cancel_btn.pack(side="left", padx=10)

        # 提示信息
        ctk.CTkLabel(main_scroll, text="💡 提示：带 * 的字段为必填项", 
                    text_color="#666666", font=ctk.CTkFont(size=12)).pack(pady=10)

    def show_species_management(self):
        """显示植物品种管理界面"""
        management_window = create_child_window(self.parent, "🌿 Plant Species Management", "1000x600")
        
        # Header
        header_frame = ctk.CTkFrame(management_window, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(header_frame, text="🌿 Plant Species Management", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        
        def refresh_list():
            """刷新品种列表"""
            for widget in main_scroll.winfo_children():
                widget.destroy()
            load_species_data()
        
        refresh_btn = ctk.CTkButton(header_frame, text="🔄 Refresh", 
                                command=refresh_list, width=80)
        refresh_btn.pack(side="right", padx=10)
        
        add_btn = ctk.CTkButton(header_frame, text="➕ Add Species", 
                            command=self.show_add_species_dialog, width=100)
        add_btn.pack(side="right", padx=10)
        
        # Main scroll frame
        main_scroll = ctk.CTkScrollableFrame(management_window)
        main_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        def load_species_data():
            """加载植物品种数据"""
            species_list = self.plant_species_model.get_all_species()
            
            if not species_list:
                ctk.CTkLabel(main_scroll, text="No plant species data available").pack(pady=50)
                return
            
            # Table header
            headers = ["ID", "Name", "Scientific Name", "Type", "Difficulty", "Light", "Actions"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(main_scroll, text=header, font=ctk.CTkFont(weight="bold")).grid(
                    row=0, column=i, padx=8, pady=8, sticky="w"
                )
            
            # Data rows
            for row, species in enumerate(species_list, 1):
                # ID
                ctk.CTkLabel(main_scroll, text=str(species['id'])).grid(
                    row=row, column=0, padx=8, pady=4, sticky="w"
                )
                # Name
                ctk.CTkLabel(main_scroll, text=species['name']).grid(
                    row=row, column=1, padx=8, pady=4, sticky="w"
                )
                # Scientific Name
                ctk.CTkLabel(main_scroll, text=species.get('scientific_name', '')).grid(
                    row=row, column=2, padx=8, pady=4, sticky="w"
                )
                # Type
                ctk.CTkLabel(main_scroll, text=species['plant_type']).grid(
                    row=row, column=3, padx=8, pady=4, sticky="w"
                )
                # Difficulty
                ctk.CTkLabel(main_scroll, text=species['difficulty_level']).grid(
                    row=row, column=4, padx=8, pady=4, sticky="w"
                )
                # Light
                ctk.CTkLabel(main_scroll, text=species['light_requirements']).grid(
                    row=row, column=5, padx=8, pady=4, sticky="w"
                )
                
                # Action buttons
                action_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
                action_frame.grid(row=row, column=6, padx=8, pady=4, sticky="w")
                
                def edit_species(species_id=species['id']):
                    """编辑植物品种"""
                    self.show_edit_species_dialog(species_id, refresh_list)
                
                def delete_species(species_id=species['id'], species_name=species['name']):
                    """删除植物品种"""
                    self._delete_species_confirmation(species_id, species_name, refresh_list)
                
                edit_btn = ctk.CTkButton(action_frame, text="Edit", 
                                    command=edit_species, width=50)
                edit_btn.pack(side="left", padx=2)
                
                delete_btn = ctk.CTkButton(action_frame, text="Delete", 
                                        command=delete_species, width=50,
                                        fg_color="#DC143C", hover_color="#FF6B6B")
                delete_btn.pack(side="left", padx=2)
        
        # Initial data load
        load_species_data()



# 在 SpeciesManagementView 类中，修复 show_edit_species_dialog 方法：

    def show_edit_species_dialog(self, species_id, refresh_callback=None):
        """显示编辑植物品种对话框 - 修复版本"""
        species = self.plant_species_model.get_species_by_id(species_id)
        if not species:
            messagebox.showerror("错误", "找不到该植物品种信息")
            return
        
        dialog = create_child_window(self.parent, f"编辑 {species['name']}", "600x700")
        
        # 创建主滚动框架
        main_scroll = ctk.CTkScrollableFrame(dialog)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(main_scroll, text=f"✏️ 编辑 {species['name']}", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)
        
        # === 基本信息 ===
        basic_frame = ctk.CTkFrame(main_scroll)
        basic_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(basic_frame, text="📋 基本信息", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        # 植物名称
        ctk.CTkLabel(basic_frame, text="植物名称 *").pack(anchor="w", pady=5)
        name_entry = ctk.CTkEntry(basic_frame, placeholder_text="例如：绿萝")
        name_entry.pack(fill="x", pady=5)
        name_entry.insert(0, species['name'])
        
        # 学名和科属在一行
        name_row = ctk.CTkFrame(basic_frame, fg_color="transparent")
        name_row.pack(fill="x", pady=5)
        
        ctk.CTkLabel(name_row, text="学名").pack(side="left", anchor="w", padx=(0, 10))
        scientific_name_entry = ctk.CTkEntry(name_row, placeholder_text="例如：Epipremnum aureum")
        scientific_name_entry.pack(side="left", fill="x", expand=True, padx=(0, 20))
        scientific_name_entry.insert(0, species.get('scientific_name', ''))
        
        ctk.CTkLabel(name_row, text="科属").pack(side="left", anchor="w", padx=(0, 10))
        family_entry = ctk.CTkEntry(name_row, placeholder_text="例如：天南星科")
        family_entry.pack(side="left", fill="x", expand=True)
        family_entry.insert(0, species.get('family', ''))
        
        # 植物类型和难度在一行
        type_row = ctk.CTkFrame(basic_frame, fg_color="transparent")
        type_row.pack(fill="x", pady=5)
        
        ctk.CTkLabel(type_row, text="植物类型").pack(side="left", anchor="w", padx=(0, 10))
        plant_type_var = ctk.StringVar(value=species['plant_type'])
        plant_type_combo = ctk.CTkComboBox(type_row, 
                                        values=["观叶植物", "开花植物", "多肉植物", "果蔬", "草本植物", "乔木", "灌木"],
                                        variable=plant_type_var, width=150)
        plant_type_combo.pack(side="left", padx=(0, 20))
        
        ctk.CTkLabel(type_row, text="养护难度").pack(side="left", anchor="w", padx=(0, 10))
        difficulty_var = ctk.StringVar(value=species['difficulty_level'])
        difficulty_combo = ctk.CTkComboBox(type_row, 
                                        values=["非常简单", "简单", "中等", "困难", "专家级"],
                                        variable=difficulty_var, width=150)
        difficulty_combo.pack(side="left")
        
        # === 养护要求 ===
        care_frame = ctk.CTkFrame(main_scroll)
        care_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(care_frame, text="💧 养护要求", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        # 光照和毒性在一行
        light_toxicity_row = ctk.CTkFrame(care_frame, fg_color="transparent")
        light_toxicity_row.pack(fill="x", pady=5)
        
        ctk.CTkLabel(light_toxicity_row, text="光照需求").pack(side="left", anchor="w", padx=(0, 10))
        light_var = ctk.StringVar(value=species['light_requirements'])
        light_combo = ctk.CTkComboBox(light_toxicity_row, 
                                    values=["强光", "中光照", "弱光", "耐阴"],
                                    variable=light_var, width=120)
        light_combo.pack(side="left", padx=(0, 20))
        
        ctk.CTkLabel(light_toxicity_row, text="毒性").pack(side="left", anchor="w", padx=(0, 10))
        toxicity_var = ctk.StringVar(value=species.get('toxicity', '无毒'))
        toxicity_combo = ctk.CTkComboBox(light_toxicity_row, 
                                    values=["无毒", "微毒", "有毒", "剧毒"],
                                    variable=toxicity_var, width=120)
        toxicity_combo.pack(side="left")
        
        # 浇水频率
        watering_frame = ctk.CTkFrame(care_frame, fg_color="transparent")
        watering_frame.pack(fill="x", pady=8)
        
        ctk.CTkLabel(watering_frame, text="浇水频率").pack(anchor="w", pady=5)
        
        watering_sub = ctk.CTkFrame(watering_frame, fg_color="transparent")
        watering_sub.pack(fill="x", pady=5)
        
        ctk.CTkLabel(watering_sub, text="夏季").pack(side="left", padx=5)
        summer_water_entry = ctk.CTkEntry(watering_sub, width=60)
        summer_water_entry.pack(side="left", padx=5)
        summer_water_entry.insert(0, str(species.get('watering_frequency_summer', 7)))
        ctk.CTkLabel(watering_sub, text="天/次").pack(side="left", padx=5)
        
        ctk.CTkLabel(watering_sub, text="冬季").pack(side="left", padx=(20,5))
        winter_water_entry = ctk.CTkEntry(watering_sub, width=60)
        winter_water_entry.pack(side="left", padx=5)
        winter_water_entry.insert(0, str(species.get('watering_frequency_winter', 14)))
        ctk.CTkLabel(watering_sub, text="天/次").pack(side="left", padx=5)
        
        # 施肥和换盆频率
        fert_repot_frame = ctk.CTkFrame(care_frame, fg_color="transparent")
        fert_repot_frame.pack(fill="x", pady=8)
        
        ctk.CTkLabel(fert_repot_frame, text="施肥频率").pack(side="left", anchor="w", padx=(0, 10))
        fertilizing_entry = ctk.CTkEntry(fert_repot_frame, width=80)
        fertilizing_entry.pack(side="left", padx=(0, 20))
        fertilizing_entry.insert(0, str(species.get('fertilizing_frequency', 30)))
        ctk.CTkLabel(fert_repot_frame, text="天/次").pack(side="left", padx=5)
        
        ctk.CTkLabel(fert_repot_frame, text="换盆频率").pack(side="left", anchor="w", padx=(20, 10))
        repotting_entry = ctk.CTkEntry(fert_repot_frame, width=80)
        repotting_entry.pack(side="left", padx=(0, 5))
        repotting_entry.insert(0, str(species.get('repotting_frequency', 12)))
        ctk.CTkLabel(fert_repot_frame, text="月/次").pack(side="left", padx=5)
        
        # 温度和湿度要求
        temp_humidity_frame = ctk.CTkFrame(care_frame, fg_color="transparent")
        temp_humidity_frame.pack(fill="x", pady=8)
        
        # 温度
        temp_frame = ctk.CTkFrame(temp_humidity_frame, fg_color="transparent")
        temp_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(temp_frame, text="适宜温度").pack(anchor="w")
        temp_sub = ctk.CTkFrame(temp_frame, fg_color="transparent")
        temp_sub.pack(fill="x", pady=5)
        
        temp_min_entry = ctk.CTkEntry(temp_sub, width=60)
        temp_min_entry.pack(side="left", padx=2)
        temp_min_entry.insert(0, str(species.get('optimal_temperature_min', 15)))
        ctk.CTkLabel(temp_sub, text="~").pack(side="left", padx=2)
        temp_max_entry = ctk.CTkEntry(temp_sub, width=60)
        temp_max_entry.pack(side="left", padx=2)
        temp_max_entry.insert(0, str(species.get('optimal_temperature_max', 30)))
        ctk.CTkLabel(temp_sub, text="℃").pack(side="left", padx=2)
        
        # 湿度
        humidity_frame = ctk.CTkFrame(temp_humidity_frame, fg_color="transparent")
        humidity_frame.pack(side="left", fill="x", expand=True, padx=(20,0))
        
        ctk.CTkLabel(humidity_frame, text="适宜湿度").pack(anchor="w")
        humidity_sub = ctk.CTkFrame(humidity_frame, fg_color="transparent")
        humidity_sub.pack(fill="x", pady=5)
        
        humidity_min_entry = ctk.CTkEntry(humidity_sub, width=60)
        humidity_min_entry.pack(side="left", padx=2)
        humidity_min_entry.insert(0, str(species.get('ideal_humidity_min', 40)))
        ctk.CTkLabel(humidity_sub, text="~").pack(side="left", padx=2)
        humidity_max_entry = ctk.CTkEntry(humidity_sub, width=60)
        humidity_max_entry.pack(side="left", padx=2)
        humidity_max_entry.insert(0, str(species.get('ideal_humidity_max', 70)))
        ctk.CTkLabel(humidity_sub, text="%").pack(side="left", padx=2)
        
        # === 描述信息 ===
        desc_frame = ctk.CTkFrame(main_scroll)
        desc_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(desc_frame, text="📝 描述信息", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        # 植物描述
        ctk.CTkLabel(desc_frame, text="植物描述").pack(anchor="w", pady=5)
        description_text = ctk.CTkTextbox(desc_frame, height=70)
        description_text.pack(fill="x", pady=5)
        description_text.insert("1.0", species.get('description', ''))
        
        # 养护技巧
        ctk.CTkLabel(desc_frame, text="养护技巧").pack(anchor="w", pady=(15,5))
        care_tips_text = ctk.CTkTextbox(desc_frame, height=60)
        care_tips_text.pack(fill="x", pady=5)
        care_tips_text.insert("1.0", species.get('care_tips', ''))
        
        # 常见问题
        ctk.CTkLabel(desc_frame, text="常见问题").pack(anchor="w", pady=(15,5))
        common_problems_text = ctk.CTkTextbox(desc_frame, height=60)
        common_problems_text.pack(fill="x", pady=5)
        common_problems_text.insert("1.0", species.get('common_problems', ''))
        
        def save_changes():
            """保存修改"""
            # 验证必填字段
            if not name_entry.get().strip():
                messagebox.showerror("错误", "请填写植物名称")
                return
            
            # 验证数字字段
            try:
                summer_water = int(summer_water_entry.get()) if summer_water_entry.get().strip() else 7
                winter_water = int(winter_water_entry.get()) if winter_water_entry.get().strip() else 14
                fertilizing = int(fertilizing_entry.get()) if fertilizing_entry.get().strip() else 30
                repotting = int(repotting_entry.get()) if repotting_entry.get().strip() else 12
                
                temp_min = int(temp_min_entry.get()) if temp_min_entry.get().strip() else None
                temp_max = int(temp_max_entry.get()) if temp_max_entry.get().strip() else None
                humidity_min = int(humidity_min_entry.get()) if humidity_min_entry.get().strip() else None
                humidity_max = int(humidity_max_entry.get()) if humidity_max_entry.get().strip() else None
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")
                return
            
            updates = {
                'name': name_entry.get().strip(),
                'scientific_name': scientific_name_entry.get().strip(),
                'family': family_entry.get().strip(),
                'plant_type': plant_type_var.get(),
                'difficulty_level': difficulty_var.get(),
                'light_requirements': light_var.get(),
                'optimal_temperature_min': temp_min,
                'optimal_temperature_max': temp_max,
                'ideal_humidity_min': humidity_min,
                'ideal_humidity_max': humidity_max,
                'watering_frequency_summer': summer_water,
                'watering_frequency_winter': winter_water,
                'fertilizing_frequency': fertilizing,
                'repotting_frequency': repotting,
                'description': description_text.get("1.0", "end-1c").strip(),
                'care_tips': care_tips_text.get("1.0", "end-1c").strip(),
                'common_problems': common_problems_text.get("1.0", "end-1c").strip(),
                'toxicity': toxicity_var.get()
            }
            
            if self.plant_species_model.update_species(species_id, updates):
                messagebox.showinfo("成功", "植物品种信息更新成功！")
                dialog.destroy()
                if refresh_callback:
                    refresh_callback()  # 刷新列表
            else:
                messagebox.showerror("错误", "更新失败，请重试")
        
        # 按钮框架
        button_frame = ctk.CTkFrame(main_scroll)
        button_frame.pack(pady=20)
        
        save_btn = ctk.CTkButton(button_frame, text="💾 保存", 
                            command=save_changes, width=120)
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(button_frame, text="❌ 取消", 
                            command=dialog.destroy, width=120)
        cancel_btn.pack(side="left", padx=10)



    def _delete_species_confirmation(self, species_id, species_name, refresh_callback):
        """删除植物品种确认对话框 - 修复版本"""
        # 先检查是否有植物使用这个品种
        plants_using_species = self._check_plants_using_species(species_id)
        
        if plants_using_species:
            plant_names = ", ".join([p['nickname'] for p in plants_using_species[:3]])  # 显示前3个
            if len(plants_using_species) > 3:
                plant_names += f" 等{len(plants_using_species)}个植物"
            
            messagebox.showerror(
                "无法删除", 
                f"无法删除品种 '{species_name}'，因为以下植物正在使用：\n{plant_names}\n\n请先删除或修改这些植物后再删除品种。"
            )
            return
        
        # 确认删除
        result = messagebox.askyesno(
            "确认删除",
            f"确定要删除品种 '{species_name}' 吗？\n\n此操作不可撤销！"
        )
        
        if result:
            if self.plant_species_model.delete_species(species_id):
                messagebox.showinfo("成功", f"品种 '{species_name}' 删除成功！")
                if refresh_callback:
                    refresh_callback()
            else:
                messagebox.showerror("错误", f"删除品种 '{species_name}' 失败")

    def _check_plants_using_species(self, species_id):
        """检查是否有植物使用这个品种"""
        try:
            my_plants_model = MyPlants()
            all_plants = my_plants_model.get_all_plants()
            plants_using = [plant for plant in all_plants if plant['species_id'] == species_id]
            return plants_using
        except Exception as e:
            print(f"检查品种使用情况错误: {e}")
            return []


# 如果直接运行此文件进行测试
if __name__ == "__main__":
    root = ctk.CTk()
    app = SpeciesManagementView(root)
    app.show_add_species_dialog()
    root.mainloop()