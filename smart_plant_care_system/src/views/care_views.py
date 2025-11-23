# src/views/care_views.py
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.plant_models import MyPlants, CareLogs
from utils.window_utils import create_child_window

class CareManagementView:
    def __init__(self, parent):
        self.parent = parent
        self.my_plants_model = MyPlants()
        self.care_logs_model = CareLogs()
       
    def show_care_reminders(self):
        """显示养护提醒"""
        due_tasks = self.care_logs_model.get_due_care_tasks()
        
        if not due_tasks:
            messagebox.showinfo("养护提醒", "🎉 没有到期的养护任务！")
            return
        
        reminder_window = create_child_window(self.parent, "📅 养护提醒", "600x400")
        
        ctk.CTkLabel(reminder_window, 
                    text="⏰ 到期的养护任务",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        scroll_frame = ctk.CTkScrollableFrame(reminder_window)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        for task in due_tasks:
            task_frame = ctk.CTkFrame(scroll_frame)
            task_frame.pack(fill="x", padx=5, pady=5)
            
            # 任务信息
            info_text = f"🌿 {task['nickname']} ({task['species_name']})\n"
            info_text += f"📋 {task['care_type']} - 逾期 {task['days_overdue']} 天\n"
            info_text += f"📅 应于 {task['next_due_date']} 完成"
            
            ctk.CTkLabel(task_frame, text=info_text, justify="left").pack(anchor="w", padx=10, pady=5)
            
            # 完成按钮 - 修复窗口管理
            def complete_task(plant_id=task['plant_id'], care_type=task['care_type'], window=reminder_window):
                window.destroy()  # 先关闭提醒窗口
                self.record_care_completion(plant_id, care_type)
                # 不再自动重新打开提醒窗口
            
            complete_btn = ctk.CTkButton(task_frame, text="标记完成", 
                                    command=complete_task, width=80)
            complete_btn.pack(side="right", padx=10, pady=5)
   


    def record_care_completion(self, plant_id, care_type, refresh_callback=None, parent_window=None):
        """记录养护完成 - 支持回调刷新"""
        if parent_window is None:
            parent_window = self.parent
            
        dialog = create_child_window(parent_window, f"记录{care_type}", "450x500")
        
        # 设置窗口标题和焦点
        dialog.title(f"记录{care_type}完成")
        dialog.focus_set()
        
        ctk.CTkLabel(dialog, text=f"记录 {care_type} 完成", 
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        # 表单框架
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        row = 0
        
        # 详细信息
        ctk.CTkLabel(form_frame, text="详细信息*:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        details_entry = ctk.CTkEntry(form_frame, width=250, placeholder_text="例如：浇水量、肥料类型等")
        details_entry.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        row += 1
        
        # 用量
        ctk.CTkLabel(form_frame, text="用量:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        amount_entry = ctk.CTkEntry(form_frame, width=250, placeholder_text="例如：500ml, 10g")
        amount_entry.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        row += 1
        
        # 使用的产品
        ctk.CTkLabel(form_frame, text="使用的产品:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        product_entry = ctk.CTkEntry(form_frame, width=250, placeholder_text="例如：液体肥料、杀虫剂等")
        product_entry.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        row += 1
        
        # 观察效果
        ctk.CTkLabel(form_frame, text="观察效果:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        effect_var = ctk.StringVar(value="无变化")
        effect_combo = ctk.CTkComboBox(form_frame, 
                                    values=["明显改善", "轻微改善", "无变化", "有不良反应"],
                                    variable=effect_var, width=250)
        effect_combo.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        row += 1
        
        # 备注
        ctk.CTkLabel(form_frame, text="备注:").grid(row=row, column=0, padx=10, pady=10, sticky="nw")
        notes_text = ctk.CTkTextbox(form_frame, width=250, height=80)
        notes_text.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        row += 1
        
        # 下次养护提醒（可选）
        ctk.CTkLabel(form_frame, text="下次提醒:").grid(row=row, column=0, padx=10, pady=10, sticky="w")
        reminder_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        reminder_frame.grid(row=row, column=1, padx=10, pady=10, sticky="w")
        
        reminder_var = ctk.StringVar(value="7")
        reminder_combo = ctk.CTkComboBox(reminder_frame, 
                                    values=["3", "5", "7", "10", "14", "30"],
                                    variable=reminder_var, width=80)
        reminder_combo.pack(side="left")
        ctk.CTkLabel(reminder_frame, text="天后").pack(side="left", padx=5)
        row += 1
        
        # 配置网格权重
        form_frame.columnconfigure(1, weight=1)
        
        def save_care_log():
            """保存养护记录"""
            # 验证必填字段
            if not details_entry.get().strip():
                messagebox.showerror("错误", "请填写详细信息")
                return
            
            # 计算下次提醒日期
            from datetime import datetime, timedelta
            try:
                reminder_days = int(reminder_var.get())
                next_due_date = datetime.now() + timedelta(days=reminder_days)
            except ValueError:
                next_due_date = datetime.now() + timedelta(days=7)
            
            care_data = {
                'plant_id': plant_id,
                'care_type': care_type,
                'care_date': datetime.now(),
                'details': details_entry.get().strip(),
                'amount_used': amount_entry.get().strip(),
                'product_used': product_entry.get().strip(),
                'observed_effect': effect_var.get(),
                'notes': notes_text.get("1.0", "end-1c").strip(),
                'next_due_date': next_due_date
            }
            
            if self.care_logs_model.add_care_log(care_data):
                # 更新植物的最后养护时间
                update_data = {}
                if care_type == '浇水':
                    update_data['last_watered'] = datetime.now().date()
                elif care_type == '施肥':
                    update_data['last_fertilized'] = datetime.now().date()
                elif care_type == '换盆':
                    update_data['last_repotted'] = datetime.now().date()
                elif care_type == '修剪':
                    update_data['last_pruned'] = datetime.now().date()
                
                if update_data:
                    self.my_plants_model.update_plant(plant_id, update_data)
                
                messagebox.showinfo("成功", f"{care_type}记录已保存！\n下次提醒: {next_due_date.strftime('%Y-%m-%d')}")
                dialog.destroy()
                
                # 回调刷新
                if refresh_callback:
                    refresh_callback()
            else:
                messagebox.showerror("错误", "保存记录失败，请重试")
        
        # 按钮框架
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=20)
        
        save_btn = ctk.CTkButton(button_frame, text="💾 保存记录", command=save_care_log, width=120)
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(button_frame, text="❌ 取消", command=dialog.destroy, width=120)
        cancel_btn.pack(side="left", padx=10)

        # 自动填充一些默认值
        if care_type == '浇水':
            details_entry.insert(0, "常规浇水")
            amount_entry.insert(0, "适量")
        elif care_type == '施肥':
            details_entry.insert(0, "液体肥料")
            amount_entry.insert(0, "按说明稀释")
        elif care_type == '修剪':
            details_entry.insert(0, "修剪枯叶和过密枝条")
        elif care_type == '清洁叶片':
            details_entry.insert(0, "擦拭叶片灰尘")

    def show_care_history(self, plant_id=None):
        """显示养护历史"""
        if plant_id is None:
            plants = self.my_plants_model.get_all_plants()
            if not plants:
                messagebox.showinfo("提示", "请先添加植物")
                return
            
            # 让用户选择植物
            plant_selection = create_child_window(self.parent, "选择植物", "300x400")
            
            ctk.CTkLabel(plant_selection, text="选择要查看的植物:", font=ctk.CTkFont(weight="bold")).pack(pady=10)
            
            for plant in plants:
                def show_history(p_id=plant['id']):
                    plant_selection.destroy()
                    self._show_plant_care_history(p_id)
                
                plant_frame = ctk.CTkFrame(plant_selection)
                plant_frame.pack(fill="x", padx=20, pady=5)
                
                plant_text = f"🌿 {plant['nickname']}\n"
                plant_text += f"  品种: {plant['species_name']}\n"
                plant_text += f"  位置: {plant['location']}"
                
                ctk.CTkLabel(plant_frame, text=plant_text, justify="left").pack(anchor="w", padx=10, pady=8)
                
                history_btn = ctk.CTkButton(plant_frame, text="查看历史", command=show_history, width=80)
                history_btn.pack(side="right", padx=10, pady=5)
        else:
            self._show_plant_care_history(plant_id)
    
    def _show_plant_care_history(self, plant_id):
        """显示具体植物的养护历史"""
        plant = self.my_plants_model.get_plant_by_id(plant_id)
        care_logs = self.care_logs_model.get_plant_care_logs(plant_id)
        
        history_window = create_child_window(self.parent, f"{plant['nickname']}的养护历史", "900x500")
        
        title_text = f"🌿 {plant['nickname']} ({plant['species_name']}) - 养护历史"
        ctk.CTkLabel(history_window, text=title_text, 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        if not care_logs:
            ctk.CTkLabel(history_window, text="暂无养护记录").pack(pady=50)
            return
        
        scroll_frame = ctk.CTkScrollableFrame(history_window)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 表头
        headers = ["日期", "养护类型", "详细信息", "用量", "效果", "备注"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(scroll_frame, text=header, 
                        font=ctk.CTkFont(weight="bold")).grid(
                row=0, column=i, padx=10, pady=5, sticky="w"
            )
        
        # 养护记录
        for row, log in enumerate(care_logs, 1):
            # 日期
            ctk.CTkLabel(scroll_frame, text=str(log['care_date'])[:16]).grid(
                row=row, column=0, padx=10, pady=2, sticky="w"
            )
            # 养护类型
            ctk.CTkLabel(scroll_frame, text=log['care_type']).grid(
                row=row, column=1, padx=10, pady=2, sticky="w"
            )
            # 详细信息
            details = log.get('details', '')
            ctk.CTkLabel(scroll_frame, text=details[:20] + "..." if len(details) > 20 else details).grid(
                row=row, column=2, padx=10, pady=2, sticky="w"
            )
            # 用量
            amount = log.get('amount_used', '')
            ctk.CTkLabel(scroll_frame, text=amount).grid(
                row=row, column=3, padx=10, pady=2, sticky="w"
            )
            # 效果
            effect = log.get('observed_effect', '无变化')
            ctk.CTkLabel(scroll_frame, text=effect).grid(
                row=row, column=4, padx=10, pady=2, sticky="w"
            )
            # 备注
            notes = log.get('notes', '')
            ctk.CTkLabel(scroll_frame, text=notes[:30] + "..." if len(notes) > 30 else notes).grid(
                row=row, column=5, padx=10, pady=2, sticky="w"
            )

    def show_care_center(self):
        """显示养护中心 - 统一管理所有植物的养护"""
        center_window = create_child_window(self.parent, "🏥 植物养护中心", "900x700")
        
        # 标题和统计
        header_frame = ctk.CTkFrame(center_window, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(header_frame, text="🏥 植物养护中心", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        
        # 刷新按钮
        def refresh_center():
            """刷新养护中心"""
            for widget in main_scroll.winfo_children():
                widget.destroy()
            load_plants_data()
        
        refresh_btn = ctk.CTkButton(header_frame, text="🔄 刷新", 
                                command=refresh_center, width=80)
        refresh_btn.pack(side="right", padx=10)
        
        # 主滚动框架
        main_scroll = ctk.CTkScrollableFrame(center_window)
        main_scroll.pack(fill="both", expand=True, padx=20, pady=10)
        
        def _needs_watering(plant):
            """判断植物是否需要浇水"""
            if not plant['last_watered']:
                return True
            
            from datetime import datetime
            last_watered = plant['last_watered']
            if isinstance(last_watered, str):
                try:
                    last_watered = datetime.strptime(last_watered, '%Y-%m-%d').date()
                except:
                    return True
            
            # 简单逻辑：超过5天需要浇水
            days_since_water = (datetime.now().date() - last_watered).days
            return days_since_water >= 5
        
        def _get_care_status(plant):
            """获取植物养护状态"""
            needs_water = _needs_watering(plant)
            needs_care = plant['health_status'] in ['需关注', '生病', '濒危']
            
            return {
                'needs_water': needs_water,
                'needs_care': needs_water or needs_care,
                'health_status': plant['health_status']
            }
        
        def _quick_care_action(plant_id, care_type, refresh_callback=None):
            """快速养护操作"""
            plant = self.my_plants_model.get_plant_by_id(plant_id)
            if not plant:
                messagebox.showerror("错误", "找不到植物信息")
                return
            
            from datetime import datetime, timedelta
            
            # 快速记录养护
            care_data = {
                'plant_id': plant_id,
                'care_type': care_type,
                'care_date': datetime.now(),
                'details': f"快速{care_type}",
                'amount_used': "适量",
                'observed_effect': '无变化',
                'notes': f"通过养护中心快速{care_type}",
                'next_due_date': datetime.now() + timedelta(days=7)
            }
            
            if self.care_logs_model.add_care_log(care_data):
                # 更新植物的最后养护时间
                update_data = {}
                if care_type == '浇水':
                    update_data['last_watered'] = datetime.now().date()
                elif care_type == '施肥':
                    update_data['last_fertilized'] = datetime.now().date()
                
                if update_data:
                    self.my_plants_model.update_plant(plant_id, update_data)
                
                messagebox.showinfo("成功", f"✅ 已为 {plant['nickname']} 完成{care_type}")
                if refresh_callback:
                    refresh_callback()
            else:
                messagebox.showerror("错误", f"{care_type}记录失败")
        
        def _show_plant_care_dialog(plant_id, refresh_callback=None):
            """显示植物详细养护对话框"""
            plant = self.my_plants_model.get_plant_by_id(plant_id)
            if not plant:
                messagebox.showerror("错误", "找不到植物信息")
                return
            
            dialog = create_child_window(center_window, f"养护 {plant['nickname']}", "500x600")
            
            main_scroll = ctk.CTkScrollableFrame(dialog)
            main_scroll.pack(fill="both", expand=True, padx=10, pady=10)
            
            ctk.CTkLabel(main_scroll, text=f"🏥 养护 {plant['nickname']}", 
                        font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)
            
            # 植物信息
            info_frame = ctk.CTkFrame(main_scroll)
            info_frame.pack(fill="x", pady=10, padx=5)
            
            info_text = f"品种: {plant['species_name']}\n"
            info_text += f"位置: {plant['location']}\n"
            info_text += f"健康状态: {plant['health_status']}\n"
            info_text += f"最后浇水: {plant['last_watered'] or '从未浇水'}\n"
            info_text += f"最后施肥: {plant['last_fertilized'] or '从未施肥'}"
            
            ctk.CTkLabel(info_frame, text=info_text, justify="left").pack(anchor="w", padx=15, pady=10)
            
            # 养护类型选择
            care_frame = ctk.CTkFrame(main_scroll)
            care_frame.pack(fill="x", pady=10, padx=5)
            
            ctk.CTkLabel(care_frame, text="🔧 选择养护类型", 
                        font=ctk.CTkFont(weight="bold")).pack(pady=10)
            
            # 创建两行按钮布局
            care_types_row1 = ["浇水", "施肥", "换盆", "修剪"]
            care_types_row2 = ["除虫", "清洁叶片", "移动位置", "其他护理"]
            
            row1_frame = ctk.CTkFrame(care_frame, fg_color="transparent")
            row1_frame.pack(fill="x", pady=5)
            
            for care_type in care_types_row1:
                care_btn = ctk.CTkButton(row1_frame, text=care_type,
                                    command=lambda ct=care_type: self.record_care_completion(
                                        plant_id, ct, refresh_callback, dialog),
                                    width=80, height=35)
                care_btn.pack(side="left", padx=5, pady=5)
            
            row2_frame = ctk.CTkFrame(care_frame, fg_color="transparent")
            row2_frame.pack(fill="x", pady=5)
            
            for care_type in care_types_row2:
                care_btn = ctk.CTkButton(row2_frame, text=care_type,
                                    command=lambda ct=care_type: self.record_care_completion(
                                        plant_id, ct, refresh_callback, dialog),
                                    width=80, height=35)
                care_btn.pack(side="left", padx=5, pady=5)
            
            # 养护历史
            history_frame = ctk.CTkFrame(main_scroll)
            history_frame.pack(fill="x", pady=10, padx=5)
            
            ctk.CTkLabel(history_frame, text="📜 最近养护记录", 
                        font=ctk.CTkFont(weight="bold")).pack(pady=10)
            
            # 获取最近养护记录
            care_logs = self.care_logs_model.get_plant_care_logs(plant_id)[:5]  # 最近5条
            
            if care_logs:
                for log in care_logs:
                    log_text = f"{log['care_date'].strftime('%m-%d %H:%M')} {log['care_type']}: {log.get('details', '')}"
                    ctk.CTkLabel(history_frame, text=log_text, justify="left").pack(anchor="w", padx=15, pady=2)
            else:
                ctk.CTkLabel(history_frame, text="暂无养护记录").pack(pady=10)
        
        def load_plants_data():
            """加载所有植物数据"""
            plants = self.my_plants_model.get_all_plants()
            
            if not plants:
                ctk.CTkLabel(main_scroll, text="暂无植物数据，请先添加植物").pack(pady=50)
                return
            
            # 统计信息
            stats_frame = ctk.CTkFrame(main_scroll)
            stats_frame.pack(fill="x", pady=10, padx=5)
            
            total_plants = len(plants)
            need_water = len([p for p in plants if _needs_watering(p)])
            need_care = len([p for p in plants if p['health_status'] in ['需关注', '生病', '濒危']])
            
            stats_text = f"📊 统计: 共有 {total_plants} 株植物 | 💧 {need_water} 株需要浇水 | ⚠️ {need_care} 株需要关注"
            ctk.CTkLabel(stats_frame, text=stats_text, 
                        font=ctk.CTkFont(weight="bold")).pack(pady=10)
            
            # 每个植物的养护卡片
            for plant in plants:
                plant_card = ctk.CTkFrame(main_scroll)
                plant_card.pack(fill="x", pady=8, padx=5)
                
                # 植物基本信息
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
                
                # 养护状态
                care_status = _get_care_status(plant)
                status_color = "#FF6B6B" if care_status['needs_care'] else "#2E8B57"
                status_text = "⚠️ 需要养护" if care_status['needs_care'] else "✅ 状态良好"
                ctk.CTkLabel(left_info, text=status_text, text_color=status_color).pack(anchor="w", pady=(5,0))
                
                # 右侧操作按钮
                button_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
                button_frame.pack(side="right")
                
                # 快速养护按钮
                quick_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
                quick_frame.pack(pady=5)
                
                water_btn = ctk.CTkButton(quick_frame, text="💧 浇水", 
                                        command=lambda p=plant['id']: _quick_care_action(p, "浇水", refresh_center),
                                        width=70, height=30)
                water_btn.pack(side="left", padx=2)
                
                fertilize_btn = ctk.CTkButton(quick_frame, text="🌱 施肥", 
                                            command=lambda p=plant['id']: _quick_care_action(p, "施肥", refresh_center),
                                            width=70, height=30)
                fertilize_btn.pack(side="left", padx=2)
                
                # 详细养护按钮
                detail_btn = ctk.CTkButton(button_frame, text="📝 详细养护", 
                                        command=lambda p=plant['id']: _show_plant_care_dialog(p, refresh_center),
                                        width=100, height=30)
                detail_btn.pack(pady=5)
        
        # 初始加载数据
        load_plants_data()

