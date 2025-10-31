import sqlite3
import os
from datetime import datetime, timedelta

def fix_database():
    """修复数据库结构"""
    db_path = 'campus_events.db'
    
    print("开始修复数据库结构...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. 检查 events 表结构
        print("检查 events 表结构...")
        cursor.execute("PRAGMA table_info(events)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"当前列: {columns}")
        
        # 2. 添加缺失的列
        if 'end_time' not in columns:
            print("添加 end_time 列...")
            cursor.execute('ALTER TABLE events ADD COLUMN end_time TEXT')
            # 为现有活动设置合理的结束时间（开始时间+2小时）
            cursor.execute("SELECT id, date_time FROM events WHERE end_time IS NULL")
            events = cursor.fetchall()
            for event_id, date_time in events:
                try:
                    # 尝试解析时间并计算结束时间
                    if 'T' in date_time:
                        # 新格式: 2024-01-15T14:00
                        start_dt = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
                    else:
                        # 旧格式: 2024-01-15 14:00:00
                        start_dt = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                    
                    end_dt = start_dt + timedelta(hours=2)
                    end_time = end_dt.strftime('%Y-%m-%d %H:%M:%S')
                    
                    cursor.execute(
                        "UPDATE events SET end_time = ? WHERE id = ?",
                        (end_time, event_id)
                    )
                    print(f"为活动 {event_id} 设置结束时间: {end_time}")
                except Exception as e:
                    print(f"设置活动 {event_id} 结束时间失败: {e}")
                    # 设置默认结束时间
                    cursor.execute(
                        "UPDATE events SET end_time = ? WHERE id = ?",
                        (date_time, event_id)
                    )
        
        if 'status' not in columns:
            print("添加 status 列...")
            cursor.execute('ALTER TABLE events ADD COLUMN status TEXT DEFAULT "upcoming"')
            # 为现有活动设置状态
            cursor.execute('UPDATE events SET status = "upcoming" WHERE status IS NULL')
            print("为所有现有活动设置状态为 'upcoming'")
        
        # 3. 提交更改
        conn.commit()
        print("✅ 数据库修复完成！")
        
        # 4. 显示修复后的表结构
        cursor.execute("PRAGMA table_info(events)")
        fixed_columns = [column[1] for column in cursor.fetchall()]
        print(f"修复后的列: {fixed_columns}")
        
        # 5. 显示活动数据示例
        cursor.execute("SELECT id, title, date_time, end_time, status FROM events LIMIT 3")
        sample_events = cursor.fetchall()
        print("\n示例活动数据:")
        for event in sample_events:
            print(f"  ID: {event[0]}, 标题: {event[1]}, 开始: {event[2]}, 结束: {event[3]}, 状态: {event[4]}")
            
    except Exception as e:
        print(f"❌ 修复数据库失败: {e}")
        conn.rollback()
    finally:
        conn.close()

def check_database_health():
    """检查数据库健康状态"""
    db_path = 'campus_events.db'
    
    if not os.path.exists(db_path):
        print("❌ 数据库文件不存在")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 检查所有必要的表
        required_tables = ['users', 'events', 'registrations', 'reviews']
        existing_tables = []
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        existing_tables = [table[0] for table in tables]
        
        print("现有表:", existing_tables)
        
        missing_tables = [table for table in required_tables if table not in existing_tables]
        if missing_tables:
            print(f"❌ 缺失的表: {missing_tables}")
            return False
        
        print("✅ 所有必要表都存在")
        return True
        
    except Exception as e:
        print(f"❌ 检查数据库健康状态失败: {e}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    print("=" * 50)
    print("校园活动系统数据库修复工具")
    print("=" * 50)
    
    # 检查数据库健康状态
    if not check_database_health():
        print("\n数据库不完整，建议重新初始化...")
        choice = input("是否重新初始化数据库？(y/n): ")
        if choice.lower() == 'y':
            from models import init_db
            init_db()
            print("✅ 数据库重新初始化完成！")
        else:
            print("请手动处理数据库问题")
    else:
        # 修复数据库结构
        fix_database()
    
    print("\n修复完成！现在可以重新启动 app.py")