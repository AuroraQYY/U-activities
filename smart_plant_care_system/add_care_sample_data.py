import mysql.connector
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(__file__))

try:
    from config import Config
except ImportError:
    class ManualConfig:
        MYSQL_HOST = 'localhost'
        MYSQL_USER = 'root'
        MYSQL_PASSWORD = '123456'
        MYSQL_DB = 'plant_care_system'
        MYSQL_PORT = 3306
    Config = ManualConfig()

def add_sample_care_data():
    """添加示例养护数据"""
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor(dictionary=True)
        
        print("💧 开始添加示例养护数据...")
        
        # 获取植物ID
        cursor.execute("SELECT id FROM my_plants WHERE nickname = '小绿'")
        plant = cursor.fetchone()
        
        if not plant:
            print("❌ 找不到示例植物，请先运行 add_sample_data.py")
            return False
        
        plant_id = plant['id']
        
        # 添加一些养护记录
        care_logs = [
            {
                'plant_id': plant_id,
                'care_type': '浇水',
                'care_date': datetime.now() - timedelta(days=2),
                'details': '常规浇水',
                'amount_used': '300ml',
                'observed_effect': '无变化',
                'notes': '土壤湿度正常',
                'next_due_date': datetime.now() + timedelta(days=5)  # 过期任务
            },
            {
                'plant_id': plant_id,
                'care_type': '施肥',
                'care_date': datetime.now() - timedelta(days=10),
                'details': '液体肥料',
                'amount_used': '10ml',
                'observed_effect': '轻微改善',
                'notes': '新叶生长良好',
                'next_due_date': datetime.now() - timedelta(days=3)  # 已过期任务
            },
            {
                'plant_id': plant_id,
                'care_type': '清洁叶片',
                'care_date': datetime.now() - timedelta(days=1),
                'details': '擦拭叶片',
                'amount_used': '',
                'observed_effect': '明显改善',
                'notes': '叶片更加光亮',
                'next_due_date': datetime.now() + timedelta(days=6)
            }
        ]
        
        for log in care_logs:
            cursor.execute("""
            INSERT INTO care_logs 
            (plant_id, care_type, care_date, details, amount_used, 
             observed_effect, notes, next_due_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                log['plant_id'], log['care_type'], log['care_date'],
                log['details'], log['amount_used'], log['observed_effect'],
                log['notes'], log['next_due_date']
            ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ 示例养护数据添加成功！")
        return True
        
    except Exception as e:
        print(f"❌ 添加养护数据错误: {e}")
        return False

if __name__ == "__main__":
    add_sample_care_data()