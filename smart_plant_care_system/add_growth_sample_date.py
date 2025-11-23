import mysql.connector
from datetime import datetime, timedelta
import random
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

def add_sample_growth_data():
    """添加示例生长数据"""
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor(dictionary=True)
        
        print("🌱 开始添加示例生长数据...")
        
        # 获取植物ID
        cursor.execute("SELECT id, nickname FROM my_plants WHERE nickname = '小绿'")
        plant = cursor.fetchone()
        
        if not plant:
            print("❌ 找不到示例植物，请先运行 add_sample_data.py")
            return False
        
        plant_id = plant['id']
        plant_nickname = plant['nickname']
        
        # 生成模拟生长数据（过去30天的数据）
        base_height = 15.0  # 初始高度
        base_leaves = 8     # 初始叶片数
        
        growth_records = []
        for i in range(30):
            record_date = datetime.now() - timedelta(days=29-i)  # 从30天前开始
            
            # 模拟生长：每天有70%概率生长
            if random.random() < 0.7:
                height_growth = random.uniform(0.1, 0.3)  # 每天生长0.1-0.3cm
                leaf_growth = random.randint(0, 1)        # 可能长新叶
            else:
                height_growth = 0
                leaf_growth = 0
            
            base_height += height_growth
            base_leaves += leaf_growth
            
            # 健康评分：基于生长情况和随机波动
            health_score = max(1, min(10, 7 + random.uniform(-1, 2)))
            
            growth_records.append({
                'plant_id': plant_id,
                'record_date': record_date,
                'height_cm': round(base_height, 1),
                'leaf_count': base_leaves,
                'new_leaf_count': leaf_growth,
                'health_score': round(health_score),
                'observations': '自动生成的示例数据'
            })
        
        # 插入生长记录
        for record in growth_records:
            cursor.execute("""
            INSERT IGNORE INTO growth_records 
            (plant_id, record_date, height_cm, leaf_count, new_leaf_count, health_score, observations)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                record['plant_id'], record['record_date'], record['height_cm'],
                record['leaf_count'], record['new_leaf_count'], record['health_score'],
                record['observations']
            ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ 为 {plant_nickname} 添加了 {len(growth_records)} 条生长记录！")
        print("📈 现在可以查看生长图表和统计数据了")
        return True
        
    except Exception as e:
        print(f"❌ 添加生长数据错误: {e}")
        return False

if __name__ == "__main__":
    add_sample_growth_data()