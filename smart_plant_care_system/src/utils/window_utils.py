# src/utils/window_utils.py
import customtkinter as ctk

def create_child_window(parent, title, geometry):
    """
    创建子窗口并确保显示在最前面
    """
    window = ctk.CTkToplevel(parent)
    window.title(title)
    window.geometry(geometry)
    
    # 设置窗口关系
    window.transient(parent)  # 设置为父窗口的transient窗口
    window.grab_set()         # 模态对话框，阻止父窗口操作
    window.focus_set()        # 获得焦点
    
    # 确保窗口显示在最前面
    window.lift()
    window.attributes('-topmost', True)
    window.after(100, lambda: window.attributes('-topmost', False))
    
    # 设置关闭窗口时的行为
    def on_closing():
        window.grab_release()
        window.destroy()
    
    window.protocol("WM_DELETE_WINDOW", on_closing)
    
    return window