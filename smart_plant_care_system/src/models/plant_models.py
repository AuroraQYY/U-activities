# src/models/plant_models.py
from datetime import datetime, date
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from .database import DatabaseConnection

class PlantSpecies:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_all_species(self):
        """获取所有植物品种"""
        conn = self.db.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM plant_species ORDER BY name")
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"获取植物品种错误: {e}")
            return []
    
    def get_species_by_id(self, species_id):
        """根据ID获取植物品种"""
        conn = self.db.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM plant_species WHERE id = %s", (species_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            print(f"获取植物品种错误: {e}")
            return None
    
    def add_species(self, species_data):
        """添加植物品种"""
        conn = self.db.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO plant_species 
            (name, scientific_name, family, plant_type, difficulty_level, 
             light_requirements, optimal_temperature_min, optimal_temperature_max,
             ideal_humidity_min, ideal_humidity_max, watering_frequency_summer,
             watering_frequency_winter, fertilizing_frequency, repotting_frequency,
             description, care_tips, common_problems, toxicity, image_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                species_data['name'], species_data['scientific_name'],
                species_data['family'], species_data['plant_type'],
                species_data['difficulty_level'], species_data['light_requirements'],
                species_data['optimal_temperature_min'], species_data['optimal_temperature_max'],
                species_data['ideal_humidity_min'], species_data['ideal_humidity_max'],
                species_data['watering_frequency_summer'], species_data['watering_frequency_winter'],
                species_data['fertilizing_frequency'], species_data['repotting_frequency'],
                species_data['description'], species_data['care_tips'],
                species_data['common_problems'], species_data['toxicity'],
                species_data.get('image_path', '')
            ))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"添加植物品种错误: {e}")
            conn.rollback()
            return False


    def delete_species(self, species_id):
        """删除植物品种 - 修复版本"""
        conn = self.db.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            # 检查是否有植物使用这个品种
            cursor.execute("SELECT COUNT(*) as count FROM my_plants WHERE species_id = %s", (species_id,))
            result = cursor.fetchone()
            plant_count = result['count'] if result else 0
            
            if plant_count > 0:
                print(f"无法删除品种: 有 {plant_count} 个植物正在使用")
                return False
            
            # 删除植物品种
            cursor.execute("DELETE FROM plant_species WHERE id = %s", (species_id,))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"删除植物品种错误: {e}")
            conn.rollback()
            return False

    def update_species(self, species_id, updates):
        """更新植物品种信息"""
        conn = self.db.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
            values = list(updates.values())
            values.append(species_id)
            
            query = f"UPDATE plant_species SET {set_clause} WHERE id = %s"
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"更新植物品种错误: {e}")
            conn.rollback()
            return False

    # 在 MyPlants 类中确保有 delete_plant 方法（如果还没有的话）：
    def delete_plant(self, plant_id):
        """删除植物"""
        conn = self.db.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM my_plants WHERE id = %s", (plant_id,))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"删除植物错误: {e}")
            conn.rollback()
            return False


class MyPlants:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_all_plants(self):
        """获取所有我的植物"""
        conn = self.db.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT mp.*, ps.name as species_name, ps.scientific_name
            FROM my_plants mp
            JOIN plant_species ps ON mp.species_id = ps.id
            ORDER BY mp.nickname
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"获取我的植物错误: {e}")
            return []
    
    def get_plant_by_id(self, plant_id):
        """根据ID获取植物详情"""
        conn = self.db.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT mp.*, ps.name as species_name, ps.scientific_name,
                   ps.light_requirements, ps.watering_frequency_summer,
                   ps.watering_frequency_winter, ps.fertilizing_frequency
            FROM my_plants mp
            JOIN plant_species ps ON mp.species_id = ps.id
            WHERE mp.id = %s
            """
            cursor.execute(query, (plant_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            print(f"获取植物详情错误: {e}")
            return None
    
    def add_plant(self, plant_data):
        """添加我的植物"""
        conn = self.db.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO my_plants 
            (species_id, nickname, purchase_date, purchase_source, purchase_price,
             location, specific_spot, health_status, growth_stage, notes, profile_image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                plant_data['species_id'], plant_data['nickname'],
                plant_data.get('purchase_date'), plant_data.get('purchase_source'),
                plant_data.get('purchase_price'), plant_data['location'],
                plant_data.get('specific_spot', ''), plant_data['health_status'],
                plant_data['growth_stage'], plant_data.get('notes', ''),
                plant_data.get('profile_image', '')
            ))
            conn.commit()
            plant_id = cursor.lastrowid
            cursor.close()
            return plant_id
        except Exception as e:
            print(f"添加植物错误: {e}")
            conn.rollback()
            return False
    
    def update_plant(self, plant_id, updates):
        """更新植物信息"""
        conn = self.db.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
            values = list(updates.values())
            values.append(plant_id)
            
            query = f"UPDATE my_plants SET {set_clause} WHERE id = %s"
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"更新植物错误: {e}")
            conn.rollback()
            return False
    
    def delete_plant(self, plant_id):
        """删除植物"""
        conn = self.db.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM my_plants WHERE id = %s", (plant_id,))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"删除植物错误: {e}")
            conn.rollback()
            return False

class CareLogs:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def add_care_log(self, log_data):
        """添加养护记录"""
        conn = self.db.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO care_logs 
            (plant_id, care_type, care_date, details, amount_used, product_used, 
             observed_effect, notes, next_due_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                log_data['plant_id'], log_data['care_type'],
                log_data.get('care_date', datetime.now()),
                log_data.get('details', ''), log_data.get('amount_used', ''),
                log_data.get('product_used', ''), log_data.get('observed_effect', '无变化'),
                log_data.get('notes', ''), log_data.get('next_due_date')
            ))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"添加养护记录错误: {e}")
            conn.rollback()
            return False
    
    def get_plant_care_logs(self, plant_id):
        """获取植物的养护记录"""
        conn = self.db.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT cl.*, mp.nickname as plant_nickname
            FROM care_logs cl
            JOIN my_plants mp ON cl.plant_id = mp.id
            WHERE cl.plant_id = %s
            ORDER BY cl.care_date DESC
            """
            cursor.execute(query, (plant_id,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"获取养护记录错误: {e}")
            return []
    
    def get_due_care_tasks(self):
        """获取到期的养护任务"""
        conn = self.db.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT 
                mp.id as plant_id,
                mp.nickname,
                ps.name as species_name,
                cl.care_type,
                cl.next_due_date,
                DATEDIFF(CURDATE(), cl.next_due_date) as days_overdue
            FROM care_logs cl
            JOIN my_plants mp ON cl.plant_id = mp.id
            JOIN plant_species ps ON mp.species_id = ps.id
            WHERE cl.next_due_date <= CURDATE()
            ORDER BY cl.next_due_date ASC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"获取到期任务错误: {e}")
            return []

class GrowthRecords:
    def __init__(self):
        self.db = DatabaseConnection()
    
    

    def add_growth_record(self, record_data):
        """添加生长记录 - 修复版本"""
        conn = self.db.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            query = """
            INSERT INTO growth_records 
            (plant_id, record_date, height_cm, width_cm, stem_diameter_mm, leaf_count, 
            new_leaf_count, flower_count, fruit_count, health_score, pest_problems, 
            disease_problems, observations, image_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                record_data['plant_id'],
                record_data.get('record_date', date.today()),
                record_data.get('height_cm'),
                record_data.get('width_cm'),
                record_data.get('stem_diameter_mm'),
                record_data.get('leaf_count'),
                record_data.get('new_leaf_count'),
                record_data.get('flower_count'),
                record_data.get('fruit_count'),
                record_data.get('health_score'),
                record_data.get('pest_problems', False),
                record_data.get('disease_problems', False),
                record_data.get('observations', ''),
                record_data.get('image_path', '')
            ))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"添加生长记录错误: {e}")
            conn.rollback()
            return False

    def get_plant_growth_records(self, plant_id):
        """获取植物的生长记录 - 修复版本"""
        conn = self.db.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT gr.*, mp.nickname as plant_nickname
            FROM growth_records gr
            JOIN my_plants mp ON gr.plant_id = mp.id
            WHERE gr.plant_id = %s
            ORDER BY gr.record_date ASC
            """
            cursor.execute(query, (plant_id,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"获取生长记录错误: {e}")
            return []

    def get_growth_statistics(self, plant_id):
        """获取植物的生长统计数据"""
        conn = self.db.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            # 获取基础统计
            query = """
            SELECT 
                COUNT(*) as total_records,
                MIN(record_date) as first_record,
                MAX(record_date) as last_record,
                AVG(height_cm) as avg_height,
                AVG(leaf_count) as avg_leaves,
                AVG(health_score) as avg_health
            FROM growth_records 
            WHERE plant_id = %s
            """
            cursor.execute(query, (plant_id,))
            stats = cursor.fetchone()
            
            # 获取生长趋势数据
            trend_query = """
            SELECT 
                record_date,
                height_cm,
                leaf_count,
                health_score
            FROM growth_records 
            WHERE plant_id = %s 
            ORDER BY record_date
            """
            cursor.execute(trend_query, (plant_id,))
            trend_data = cursor.fetchall()
            
            cursor.close()
            
            return {
                'statistics': stats,
                'trend_data': trend_data
            }
            
        except Exception as e:
            print(f"获取生长统计错误: {e}")
            return None