import mysql.connector
from config import Config
import sys
import os

def db_viewer():
    """简单的数据库查看工具"""
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor(dictionary=True)
        
        while True:
            print("\n" + "="*50)
            print("🌿 植物养护系统 - 数据库查看工具")
            print("="*50)
            print("1. 查看植物品种")
            print("2. 查看我的植物") 
            print("3. 查看养护记录")
            print("4. 查看生长记录")
            print("5. 查看所有表统计")
            print("6. 执行自定义SQL")
            print("0. 退出")
            print("-"*50)
            
            choice = input("请选择操作 (0-6): ").strip()
            
            if choice == '1':
                print("\n📗 植物品种数据:")
                cursor.execute("SELECT * FROM plant_species ORDER BY name")
                species = cursor.fetchall()
                for s in species:
                    print(f"ID: {s['id']}, 名称: {s['name']}, 学名: {s['scientific_name']}")
                    print(f"   类型: {s['plant_type']}, 难度: {s['difficulty_level']}")
                    print(f"   光照: {s['light_requirements']}, 浇水: 夏{s['watering_frequency_summer']}天/冬{s['watering_frequency_winter']}天")
                    print()
            
            elif choice == '2':
                print("\n🌿 我的植物数据:")
                cursor.execute("""
                    SELECT mp.*, ps.name as species_name 
                    FROM my_plants mp 
                    JOIN plant_species ps ON mp.species_id = ps.id 
                    ORDER BY mp.nickname
                """)
                plants = cursor.fetchall()
                for p in plants:
                    print(f"ID: {p['id']}, 昵称: {p['nickname']}, 品种: {p['species_name']}")
                    print(f"   位置: {p['location']}, 健康: {p['health_status']}, 阶段: {p['growth_stage']}")
                    print(f"   最后浇水: {p['last_watered']}, 创建时间: {p['created_at']}")
                    print()
            
            elif choice == '3':
                print("\n💧 养护记录:")
                cursor.execute("""
                    SELECT cl.*, mp.nickname as plant_nickname, ps.name as species_name
                    FROM care_logs cl
                    JOIN my_plants mp ON cl.plant_id = mp.id
                    JOIN plant_species ps ON mp.species_id = ps.id
                    ORDER BY cl.care_date DESC
                    LIMIT 20
                """)
                care_logs = cursor.fetchall()
                for log in care_logs:
                    print(f"ID: {log['id']}, 植物: {log['plant_nickname']} ({log['species_name']})")
                    print(f"   类型: {log['care_type']}, 时间: {log['care_date']}")
                    print(f"   详情: {log.get('details', '无')}, 效果: {log.get('observed_effect', '无变化')}")
                    print()
            
            elif choice == '4':
                print("\n📈 生长记录:")
                cursor.execute("""
                    SELECT gr.*, mp.nickname as plant_nickname
                    FROM growth_records gr
                    JOIN my_plants mp ON gr.plant_id = mp.id
                    ORDER BY gr.record_date DESC
                    LIMIT 15
                """)
                growth_records = cursor.fetchall()
                for record in growth_records:
                    print(f"ID: {record['id']}, 植物: {record['plant_nickname']}")
                    print(f"   日期: {record['record_date']}, 高度: {record.get('height_cm', '无')}cm")
                    print(f"   叶片: {record.get('leaf_count', '无')}, 健康评分: {record.get('health_score', '无')}/10")
                    print()
            
            elif choice == '5':
                print("\n📊 数据库统计:")
                tables = ['plant_species', 'my_plants', 'care_logs', 'growth_records']
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                    count = cursor.fetchone()['count']
                    print(f"{table}: {count} 条记录")
            
            elif choice == '6':
                sql = input("请输入SQL查询语句: ").strip()
                if sql.lower().startswith('select'):
                    try:
                        cursor.execute(sql)
                        results = cursor.fetchall()
                        if results:
                            for row in results:
                                print(row)
                        else:
                            print("查询结果为空")
                    except Exception as e:
                        print(f"SQL执行错误: {e}")
                else:
                    print("只支持SELECT查询")
            
            elif choice == '0':
                print("再见！")
                break
            
            else:
                print("无效选择，请重新输入")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"数据库连接错误: {err}")

if __name__ == "__main__":
    db_viewer()