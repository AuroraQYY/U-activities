# src/views/plant_views.py
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.plant_models import PlantSpecies, MyPlants
from utils.window_utils import create_child_window

class PlantManagementView:
    def __init__(self, parent):
        self.parent = parent
        self.plant_species_model = PlantSpecies()
        self.my_plants_model = MyPlants()
    

    def show_add_plant_dialog(self):
        """显示添加植物对话框"""
        dialog = create_child_window(self.parent, "添加新植物", "500x700")
        
        # 创建主滚动框架
        main_scroll = ctk.CTkScrollableFrame(dialog)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 标题
        ctk.CTkLabel(main_scroll, text="🌱 添加我的植物", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)
        
        # 植物品种选择
        ctk.CTkLabel(main_scroll, text="植物品种 *", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=5)
        species_list = self.plant_species_model.get_all_species()
        
        if not species_list:
            ctk.CTkLabel(main_scroll, text="❌ 请先添加植物品种", 
                        text_color="red").pack(pady=10)
            # 禁用保存按钮
            save_btn = ctk.CTkButton(main_scroll, text="无法添加", state="disabled")
            save_btn.pack(pady=20)
            return
        
        species_names = [f"{s['name']} ({s['scientific_name']})" for s in species_list]
        species_dict = {name: s['id'] for name, s in zip(species_names, species_list)}
        
        species_var = ctk.StringVar()
        species_combo = ctk.CTkComboBox(main_scroll, values=species_names, variable=species_var)
        species_combo.pack(fill="x", pady=5)
        species_combo.set(species_names[0])  # 设置默认选择
        
        # 植物昵称
        ctk.CTkLabel(main_scroll, text="植物昵称 *", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(20,5))
        nickname_entry = ctk.CTkEntry(main_scroll, placeholder_text="给你的植物起个可爱的名字")
        nickname_entry.pack(fill="x", pady=5)
        
        # === 购买信息 ===
        purchase_frame = ctk.CTkFrame(main_scroll)
        purchase_frame.pack(fill="x", pady=15, padx=5)
        
        ctk.CTkLabel(purchase_frame, text="🛒 购买信息", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        # 购买日期
        ctk.CTkLabel(purchase_frame, text="购买日期").pack(anchor="w", pady=5)
        purchase_date_entry = ctk.CTkEntry(purchase_frame, placeholder_text="YYYY-MM-DD")
        purchase_date_entry.pack(fill="x", pady=5)
        
        # 购买来源
        ctk.CTkLabel(purchase_frame, text="购买来源").pack(anchor="w", pady=(15,5))
        purchase_source_entry = ctk.CTkEntry(purchase_frame, placeholder_text="例如：花市、网店等")
        purchase_source_entry.pack(fill="x", pady=5)
        
        # 购买价格
        ctk.CTkLabel(purchase_frame, text="购买价格").pack(anchor="w", pady=(15,5))
        purchase_price_entry = ctk.CTkEntry(purchase_frame, placeholder_text="元")
        purchase_price_entry.pack(fill="x", pady=5)
        
        # === 位置信息 ===
        location_frame = ctk.CTkFrame(main_scroll)
        location_frame.pack(fill="x", pady=15, padx=5)
        
        ctk.CTkLabel(location_frame, text="📍 位置信息", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        # 位置选择
        ctk.CTkLabel(location_frame, text="摆放位置").pack(anchor="w", pady=5)
        location_var = ctk.StringVar(value="客厅")
        location_combo = ctk.CTkComboBox(location_frame, 
                                    values=["客厅", "卧室", "阳台", "书房", "厨房", "卫生间", "办公室", "庭院"],
                                    variable=location_var)
        location_combo.pack(fill="x", pady=5)
        
        # 具体位置
        ctk.CTkLabel(location_frame, text="具体位置描述").pack(anchor="w", pady=(15,5))
        specific_spot_entry = ctk.CTkEntry(location_frame, placeholder_text="例如：电视柜左边、窗台等")
        specific_spot_entry.pack(fill="x", pady=5)
        
        # === 状态信息 ===
        status_frame = ctk.CTkFrame(main_scroll)
        status_frame.pack(fill="x", pady=15, padx=5)
        
        ctk.CTkLabel(status_frame, text="📊 状态信息", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        # 健康状态和生长阶段在一行
        status_row = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_row.pack(fill="x", pady=10)
        
        # 健康状态
        health_frame = ctk.CTkFrame(status_row, fg_color="transparent")
        health_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(health_frame, text="健康状态").pack(anchor="w")
        health_var = ctk.StringVar(value="健康")
        health_combo = ctk.CTkComboBox(health_frame, 
                                    values=["非常健康", "健康", "一般", "需关注", "生病", "濒危"],
                                    variable=health_var)
        health_combo.pack(fill="x", pady=5)
        
        # 生长阶段
        growth_frame = ctk.CTkFrame(status_row, fg_color="transparent")
        growth_frame.pack(side="left", fill="x", expand=True, padx=(20,0))
        
        ctk.CTkLabel(growth_frame, text="生长阶段").pack(anchor="w")
        growth_var = ctk.StringVar(value="生长期")
        growth_combo = ctk.CTkComboBox(growth_frame, 
                                    values=["幼苗", "生长期", "成熟期", "开花期", "结果期", "休眠期"],
                                    variable=growth_var)
        growth_combo.pack(fill="x", pady=5)
        
        # === 备注信息 ===
        notes_frame = ctk.CTkFrame(main_scroll)
        notes_frame.pack(fill="x", pady=15, padx=5)
        
        ctk.CTkLabel(notes_frame, text="📝 备注信息", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        ctk.CTkLabel(notes_frame, text="个性化备注").pack(anchor="w", pady=5)
        notes_text = ctk.CTkTextbox(notes_frame, height=80)
        notes_text.pack(fill="x", pady=5)
        notes_text.insert("1.0", "可以记录植物的特殊习性、养护心得等...")
        
        def save_plant():
            """保存植物信息"""
            # 验证必填字段
            if not species_var.get() or not nickname_entry.get().strip():
                messagebox.showerror("错误", "请填写植物品种和昵称")
                return
            
            if species_var.get() not in species_dict:
                messagebox.showerror("错误", "请选择有效的植物品种")
                return
            
            # 验证购买日期格式
            purchase_date = None
            if purchase_date_entry.get().strip():
                try:
                    from datetime import datetime
                    purchase_date = datetime.strptime(purchase_date_entry.get().strip(), "%Y-%m-%d").date()
                except ValueError:
                    messagebox.showerror("错误", "购买日期格式不正确，请使用 YYYY-MM-DD 格式")
                    return
            
            # 验证价格格式
            purchase_price = None
            if purchase_price_entry.get().strip():
                try:
                    purchase_price = float(purchase_price_entry.get().strip())
                except ValueError:
                    messagebox.showerror("错误", "购买价格必须是数字")
                    return
            
            species_id = species_dict[species_var.get()]
            plant_data = {
                'species_id': species_id,
                'nickname': nickname_entry.get().strip(),
                'purchase_date': purchase_date,
                'purchase_source': purchase_source_entry.get().strip(),
                'purchase_price': purchase_price,
                'location': location_var.get(),
                'specific_spot': specific_spot_entry.get().strip(),
                'health_status': health_var.get(),
                'growth_stage': growth_var.get(),
                'notes': notes_text.get("1.0", "end-1c").strip()
            }
            
            result = self.my_plants_model.add_plant(plant_data)
            if result:
                messagebox.showinfo("成功", f"🌿 植物 '{nickname_entry.get().strip()}' 添加成功！")
                dialog.destroy()
            else:
                messagebox.showerror("错误", "添加植物失败，请重试")
        
        # === 按钮 ===
        button_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
        button_frame.pack(pady=20)
        
        save_btn = ctk.CTkButton(button_frame, text="💾 保存植物", 
                            command=save_plant, 
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




    def show_plants_list(self):
        """显示植物列表 - 增强版本"""
        list_window = create_child_window(self.parent, "My Plants List", "1000x600")
        
        # 标题和刷新按钮
        header_frame = ctk.CTkFrame(list_window, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(header_frame, text="🌿 My Plants List", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        
        def refresh_list():
            """刷新植物列表"""
            for widget in table_frame.winfo_children():
                widget.destroy()
            load_plants_data()
        
        refresh_btn = ctk.CTkButton(header_frame, text="🔄 Refresh", 
                                command=refresh_list, width=80)
        refresh_btn.pack(side="right", padx=10)
        
        add_btn = ctk.CTkButton(header_frame, text="➕ Add Plant", 
                            command=self.show_add_plant_dialog, width=100)
        add_btn.pack(side="right", padx=10)
        
        # 创建表格框架
        table_frame = ctk.CTkScrollableFrame(list_window)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        def load_plants_data():
            """加载植物数据到表格"""
            plants = self.my_plants_model.get_all_plants()
            
            if not plants:
                ctk.CTkLabel(table_frame, text="No plant data available, please add plants first").pack(pady=50)
                return
            
            # 表头
            headers = ["Nickname", "Species", "Location", "Health", "Growth Stage", "Last Watered", "Actions"]
            for i, header in enumerate(headers):
                ctk.CTkLabel(table_frame, text=header, font=ctk.CTkFont(weight="bold")).grid(
                    row=0, column=i, padx=8, pady=8, sticky="w"
                )
            
            # 数据行
            for row, plant in enumerate(plants, 1):
                # 昵称
                ctk.CTkLabel(table_frame, text=plant['nickname']).grid(
                    row=row, column=0, padx=8, pady=4, sticky="w"
                )
                # 品种
                ctk.CTkLabel(table_frame, text=plant['species_name']).grid(
                    row=row, column=1, padx=8, pady=4, sticky="w"
                )
                # 位置
                ctk.CTkLabel(table_frame, text=plant['location']).grid(
                    row=row, column=2, padx=8, pady=4, sticky="w"
                )
                # 健康状态（带颜色）
                health_color = {
                    '非常健康': '#2E8B57',
                    '健康': '#32CD32', 
                    '一般': '#FFA500',
                    '需关注': '#FF6B6B',
                    '生病': '#DC143C',
                    '濒危': '#8B0000'
                }.get(plant['health_status'], '#000000')
                
                health_label = ctk.CTkLabel(table_frame, text=plant['health_status'], text_color=health_color)
                health_label.grid(row=row, column=3, padx=8, pady=4, sticky="w")
                
                # 生长阶段
                ctk.CTkLabel(table_frame, text=plant['growth_stage']).grid(
                    row=row, column=4, padx=8, pady=4, sticky="w"
                )
                # 最后浇水
                last_watered = plant['last_watered'] if plant['last_watered'] else "Never"
                ctk.CTkLabel(table_frame, text=str(last_watered)).grid(
                    row=row, column=5, padx=8, pady=4, sticky="w"
                )
                
                # 操作按钮
                action_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
                action_frame.grid(row=row, column=6, padx=8, pady=4, sticky="w")
                
                def edit_plant(plant_id=plant['id']):
                    """编辑植物信息"""
                    self.show_edit_plant_dialog(plant_id, refresh_list)
                
                def delete_plant(plant_id=plant['id'], plant_name=plant['nickname']):
                    """删除植物"""
                    self._delete_plant_confirmation(plant_id, plant_name, refresh_list)
                
                def view_details(plant_id=plant['id']):
                    """查看植物详情"""
                    self.show_plant_details(plant_id)
                
                edit_btn = ctk.CTkButton(action_frame, text="Edit", 
                                    command=edit_plant, width=50)
                edit_btn.pack(side="left", padx=2)
                
                delete_btn = ctk.CTkButton(action_frame, text="Delete", 
                                        command=delete_plant, width=50,
                                        fg_color="#DC143C", hover_color="#FF6B6B")
                delete_btn.pack(side="left", padx=2)
                
                details_btn = ctk.CTkButton(action_frame, text="Details", 
                                        command=view_details, width=50)
                details_btn.pack(side="left", padx=2)
        
        # 初始加载数据
        load_plants_data()

    def _delete_plant_confirmation(self, plant_id, plant_name, refresh_callback):
        """删除植物确认对话框"""
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete '{plant_name}'?\n\n"
            "Note: This will also delete all care logs and growth records for this plant."
        )
        
        if result:
            if self.my_plants_model.delete_plant(plant_id):
                messagebox.showinfo("Success", f"Plant '{plant_name}' deleted successfully!")
                if refresh_callback:
                    refresh_callback()
            else:
                messagebox.showerror("Error", f"Failed to delete plant '{plant_name}'")

    def show_edit_plant_dialog(self, plant_id, refresh_callback=None):
        """显示编辑植物对话框"""
        plant = self.my_plants_model.get_plant_by_id(plant_id)
        if not plant:
            messagebox.showerror("错误", "找不到该植物信息")
            return
        
        dialog = create_child_window(self.parent, f"编辑 {plant['nickname']}", "500x600")
        
        # 添加主滚动框架
        main_scroll = ctk.CTkScrollableFrame(dialog)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(main_scroll, text=f"✏️ 编辑 {plant['nickname']}", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)
        
        # 植物昵称
        ctk.CTkLabel(main_scroll, text="植物昵称 *").pack(anchor="w", pady=5)
        nickname_entry = ctk.CTkEntry(main_scroll)
        nickname_entry.pack(fill="x", pady=5)
        nickname_entry.insert(0, plant['nickname'])
        
        # 位置信息
        location_frame = ctk.CTkFrame(main_scroll)
        location_frame.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(location_frame, text="📍 位置信息", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        ctk.CTkLabel(location_frame, text="摆放位置").pack(anchor="w", pady=5)
        location_var = ctk.StringVar(value=plant['location'])
        location_combo = ctk.CTkComboBox(location_frame, 
                                    values=["客厅", "卧室", "阳台", "书房", "厨房", "卫生间", "办公室", "庭院"],
                                    variable=location_var)
        location_combo.pack(fill="x", pady=5)
        
        ctk.CTkLabel(location_frame, text="具体位置").pack(anchor="w", pady=(15,5))
        specific_spot_entry = ctk.CTkEntry(location_frame, placeholder_text="例如：电视柜左边、窗台等")
        specific_spot_entry.pack(fill="x", pady=5)
        specific_spot_entry.insert(0, plant.get('specific_spot', ''))
        
        # 状态信息
        status_frame = ctk.CTkFrame(main_scroll)
        status_frame.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(status_frame, text="📊 状态信息", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        status_row = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_row.pack(fill="x", pady=10)
        
        # 健康状态
        health_frame = ctk.CTkFrame(status_row, fg_color="transparent")
        health_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(health_frame, text="健康状态").pack(anchor="w")
        health_var = ctk.StringVar(value=plant['health_status'])
        health_combo = ctk.CTkComboBox(health_frame, 
                                    values=["非常健康", "健康", "一般", "需关注", "生病", "濒危"],
                                    variable=health_var)
        health_combo.pack(fill="x", pady=5)
        
        # 生长阶段
        growth_frame = ctk.CTkFrame(status_row, fg_color="transparent")
        growth_frame.pack(side="left", fill="x", expand=True, padx=(20,0))
        
        ctk.CTkLabel(growth_frame, text="生长阶段").pack(anchor="w")
        growth_var = ctk.StringVar(value=plant['growth_stage'])
        growth_combo = ctk.CTkComboBox(growth_frame, 
                                    values=["幼苗", "生长期", "成熟期", "开花期", "结果期", "休眠期"],
                                    variable=growth_var)
        growth_combo.pack(fill="x", pady=5)
        
        # 购买信息（如果存在）
        if plant.get('purchase_date') or plant.get('purchase_source') or plant.get('purchase_price'):
            purchase_frame = ctk.CTkFrame(main_scroll)
            purchase_frame.pack(fill="x", pady=10, padx=5)
            
            ctk.CTkLabel(purchase_frame, text="🛒 购买信息", 
                        font=ctk.CTkFont(weight="bold")).pack(pady=10)
            
            # 购买日期
            if plant.get('purchase_date'):
                ctk.CTkLabel(purchase_frame, text=f"购买日期: {plant['purchase_date']}").pack(anchor="w", pady=2)
            
            # 购买来源
            if plant.get('purchase_source'):
                ctk.CTkLabel(purchase_frame, text=f"购买来源: {plant['purchase_source']}").pack(anchor="w", pady=2)
            
            # 购买价格
            if plant.get('purchase_price'):
                ctk.CTkLabel(purchase_frame, text=f"购买价格: {plant['purchase_price']}元").pack(anchor="w", pady=2)
        
        # 备注
        notes_frame = ctk.CTkFrame(main_scroll)
        notes_frame.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(notes_frame, text="📝 备注").pack(anchor="w", pady=5)
        notes_text = ctk.CTkTextbox(notes_frame, height=100)
        notes_text.pack(fill="x", pady=5)
        notes_text.insert("1.0", plant.get('notes', ''))
        
        def save_changes():
            """保存修改"""
            if not nickname_entry.get().strip():
                messagebox.showerror("错误", "请填写植物昵称")
                return
            
            updates = {
                'nickname': nickname_entry.get().strip(),
                'location': location_var.get(),
                'specific_spot': specific_spot_entry.get().strip(),
                'health_status': health_var.get(),
                'growth_stage': growth_var.get(),
                'notes': notes_text.get("1.0", "end-1c").strip()
            }
            
            if self.my_plants_model.update_plant(plant_id, updates):
                messagebox.showinfo("成功", "植物信息更新成功！")
                dialog.destroy()
                if refresh_callback:
                    refresh_callback()  # 刷新列表
            else:
                messagebox.showerror("错误", "更新失败，请重试")
        
        # 按钮
        button_frame = ctk.CTkFrame(main_scroll, fg_color="transparent")
        button_frame.pack(pady=20)
        
        save_btn = ctk.CTkButton(button_frame, text="💾 保存", 
                            command=save_changes, width=100)
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(button_frame, text="❌ 取消", 
                                command=dialog.destroy, width=100)
        cancel_btn.pack(side="left", padx=10)


    def show_plant_details(self, plant_id):
        """显示植物详情"""
        plant = self.my_plants_model.get_plant_by_id(plant_id)
        if not plant:
            messagebox.showerror("错误", "找不到该植物信息")
            return
        
        details_window = create_child_window(self.parent, f"{plant['nickname']} 详情", "500x500")
        
        # 添加主滚动框架
        main_scroll = ctk.CTkScrollableFrame(details_window)
        main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(main_scroll, text=f"🌿 {plant['nickname']} 详细信息", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)
        
        # 基本信息卡片
        basic_frame = ctk.CTkFrame(main_scroll)
        basic_frame.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(basic_frame, text="📋 基本信息", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        info_text = f"品种: {plant['species_name']}\n"
        info_text += f"学名: {plant.get('scientific_name', '未知')}\n"
        info_text += f"位置: {plant['location']}\n"
        info_text += f"具体位置: {plant.get('specific_spot', '未设置')}\n"
        info_text += f"健康状态: {plant['health_status']}\n"
        info_text += f"生长阶段: {plant['growth_stage']}"
        
        ctk.CTkLabel(basic_frame, text=info_text, justify="left").pack(anchor="w", padx=15, pady=10)
        
        # 养护信息卡片
        care_frame = ctk.CTkFrame(main_scroll)
        care_frame.pack(fill="x", pady=10, padx=5)
        
        ctk.CTkLabel(care_frame, text="💧 养护记录", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        care_text = f"最后浇水: {plant['last_watered'] or '从未浇水'}\n"
        care_text += f"最后施肥: {plant['last_fertilized'] or '从未施肥'}\n"
        care_text += f"最后换盆: {plant['last_repotted'] or '从未换盆'}\n"
        care_text += f"最后修剪: {plant['last_pruned'] or '从未修剪'}"
        
        ctk.CTkLabel(care_frame, text=care_text, justify="left").pack(anchor="w", padx=15, pady=10)
        
        # 购买信息卡片（如果有）
        if plant.get('purchase_date') or plant.get('purchase_source') or plant.get('purchase_price'):
            purchase_frame = ctk.CTkFrame(main_scroll)
            purchase_frame.pack(fill="x", pady=10, padx=5)
            
            ctk.CTkLabel(purchase_frame, text="🛒 购买信息", 
                        font=ctk.CTkFont(weight="bold")).pack(pady=10)
            
            purchase_text = ""
            if plant.get('purchase_date'):
                purchase_text += f"购买日期: {plant['purchase_date']}\n"
            if plant.get('purchase_source'):
                purchase_text += f"购买来源: {plant['purchase_source']}\n"
            if plant.get('purchase_price'):
                purchase_text += f"购买价格: {plant['purchase_price']}元"
            
            ctk.CTkLabel(purchase_frame, text=purchase_text, justify="left").pack(anchor="w", padx=15, pady=10)
        
        # 备注信息卡片
        if plant.get('notes'):
            notes_frame = ctk.CTkFrame(main_scroll)
            notes_frame.pack(fill="x", pady=10, padx=5)
            
            ctk.CTkLabel(notes_frame, text="📝 备注", 
                        font=ctk.CTkFont(weight="bold")).pack(pady=10)
            
            notes_label = ctk.CTkLabel(notes_frame, text=plant['notes'], justify="left", wraplength=400)
            notes_label.pack(anchor="w", padx=15, pady=10)
        
        # 关闭按钮
        close_btn = ctk.CTkButton(main_scroll, text="关闭", 
                                command=details_window.destroy, width=100)
        close_btn.pack(pady=20)



