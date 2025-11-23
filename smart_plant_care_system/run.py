import sys
import os

# 添加项目根目录和src目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')

if project_root not in sys.path:
    sys.path.insert(0, project_root)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

print(f"项目根目录: {project_root}")
print(f"Python路径: {sys.path}")

try:
    from src.main import main
    print("✅ 导入成功！")
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("尝试直接运行main.py...")
    
    # 尝试直接运行main.py
    main_py_path = os.path.join(src_path, 'main.py')
    if os.path.exists(main_py_path):
        exec(open(main_py_path).read())
    else:
        print(f"❌ 找不到main.py: {main_py_path}")