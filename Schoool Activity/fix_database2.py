# fix_database.py
import os
from models import init_db

def main():
    print("开始修复数据库...")
    
    # 删除现有的数据库文件
    if os.path.exists('campus_events.db'):
        os.remove('campus_events.db')
        print("已删除旧数据库文件")
    
    # 重新初始化
    init_db()
    print("数据库修复完成！")

if __name__ == '__main__':
    main()