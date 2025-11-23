# src/utils/reminder_engine.py
from datetime import datetime, date, timedelta
import mysql.connector
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import Config

class SmartReminderEngine:
    def __init__(self):
        self.db_config = {
            'host': Config.MYSQL_HOST,
            'user': Config.MYSQL_USER,
            'password': Config.MYSQL_PASSWORD,
            'database': Config.MYSQL_DB,
            'port': Config.MYSQL_PORT
        }
    
    def get_connection(self):
        """获取数据库连接"""
        try:
            conn = mysql.connector.connect(**self.db_config)
            return conn
        except mysql.connector.Error as err:
            print(f"数据库连接错误: {err}")
            return None
    
    def get_smart_reminders(self):
        """获取智能提醒列表"""
        reminders = []
        
        # 1. 浇水提醒
        watering_reminders = self._get_watering_reminders()
        reminders.extend(watering_reminders)
        
        # 2. 施肥提醒
        fertilizing_reminders = self._get_fertilizing_reminders()
        reminders.extend(fertilizing_reminders)
        
        # 3. 换盆提醒
        repotting_reminders = self._get_repotting_reminders()
        reminders.extend(repotting_reminders)
        
        # 4. 健康状态提醒
        health_reminders = self._get_health_reminders()
        reminders.extend(health_reminders)
        
        # 5. 季节性提醒
        seasonal_reminders = self._get_seasonal_reminders()
        reminders.extend(seasonal_reminders)
        
        # 按优先级排序
        reminders.sort(key=lambda x: x['priority'], reverse=True)
        
        return reminders
    
    def _get_watering_reminders(self):
        """获取浇水提醒"""
        reminders = []
        conn = self.get_connection()
        if not conn:
            return reminders
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            query = """
            SELECT 
                mp.id as plant_id,
                mp.nickname,
                ps.name as species_name,
                mp.last_watered,
                ps.watering_frequency_summer as frequency,
                mp.location,
                DATEDIFF(CURDATE(), mp.last_watered) as days_since_watered
            FROM my_plants mp
            JOIN plant_species ps ON mp.species_id = ps.id
            WHERE mp.last_watered IS NOT NULL
            """
            
            cursor.execute(query)
            plants = cursor.fetchall()
            
            for plant in plants:
                days_since_watered = plant['days_since_watered'] or 0
                frequency = plant['frequency'] or 7
                
                # 根据季节调整浇水频率（简化逻辑）
                current_month = datetime.now().month
                if current_month in [6, 7, 8]:  # 夏季
                    frequency = max(5, frequency - 2)
                elif current_month in [12, 1, 2]:  # 冬季
                    frequency = min(14, frequency + 3)
                
                if days_since_watered >= frequency:
                    urgency = "高" if days_since_watered >= frequency + 3 else "中"
                    priority = 3 if urgency == "高" else 2
                    
                    reminders.append({
                        'type': '💧 浇水提醒',
                        'plant_id': plant['plant_id'],
                        'plant_name': f"{plant['nickname']} ({plant['species_name']})",
                        'message': f"已经 {days_since_watered} 天没有浇水，建议 {frequency} 天浇水一次",
                        'urgency': urgency,
                        'priority': priority,
                        'suggested_action': '立即浇水',
                        'last_action': plant['last_watered']
                    })
            
            cursor.close()
            
        except Exception as e:
            print(f"获取浇水提醒错误: {e}")
        finally:
            conn.close()
        
        return reminders
    
    def _get_fertilizing_reminders(self):
        """获取施肥提醒"""
        reminders = []
        conn = self.get_connection()
        if not conn:
            return reminders
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            query = """
            SELECT 
                mp.id as plant_id,
                mp.nickname,
                ps.name as species_name,
                mp.last_fertilized,
                ps.fertilizing_frequency as frequency,
                DATEDIFF(CURDATE(), mp.last_fertilized) as days_since_fertilized
            FROM my_plants mp
            JOIN plant_species ps ON mp.species_id = ps.id
            WHERE mp.last_fertilized IS NOT NULL
            """
            
            cursor.execute(query)
            plants = cursor.fetchall()
            
            for plant in plants:
                days_since_fertilized = plant['days_since_fertilized'] or 0
                frequency = plant['frequency'] or 30
                
                if days_since_fertilized >= frequency:
                    urgency = "中"
                    priority = 2
                    
                    reminders.append({
                        'type': '🌱 施肥提醒',
                        'plant_id': plant['plant_id'],
                        'plant_name': f"{plant['nickname']} ({plant['species_name']})",
                        'message': f"已经 {days_since_fertilized} 天没有施肥，建议 {frequency} 天施肥一次",
                        'urgency': urgency,
                        'priority': priority,
                        'suggested_action': '施适量液体肥料',
                        'last_action': plant['last_fertilized']
                    })
            
            cursor.close()
            
        except Exception as e:
            print(f"获取施肥提醒错误: {e}")
        finally:
            conn.close()
        
        return reminders
    
    def _get_repotting_reminders(self):
        """获取换盆提醒"""
        reminders = []
        conn = self.get_connection()
        if not conn:
            return reminders
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            query = """
            SELECT 
                mp.id as plant_id,
                mp.nickname,
                ps.name as species_name,
                mp.last_repotted,
                ps.repotting_frequency as frequency_months,
                TIMESTAMPDIFF(MONTH, mp.last_repotted, CURDATE()) as months_since_repotted
            FROM my_plants mp
            JOIN plant_species ps ON mp.species_id = ps.id
            WHERE mp.last_repotted IS NOT NULL
            """
            
            cursor.execute(query)
            plants = cursor.fetchall()
            
            for plant in plants:
                months_since_repotted = plant['months_since_repotted'] or 0
                frequency_months = plant['frequency_months'] or 12
                
                if months_since_repotted >= frequency_months:
                    urgency = "低"
                    priority = 1
                    
                    reminders.append({
                        'type': '🪴 换盆提醒',
                        'plant_id': plant['plant_id'],
                        'plant_name': f"{plant['nickname']} ({plant['species_name']})",
                        'message': f"已经 {months_since_repotted} 个月没有换盆，建议 {frequency_months} 个月换盆一次",
                        'urgency': urgency,
                        'priority': priority,
                        'suggested_action': '检查根系情况，考虑换大一号花盆',
                        'last_action': plant['last_repotted']
                    })
            
            cursor.close()
            
        except Exception as e:
            print(f"获取换盆提醒错误: {e}")
        finally:
            conn.close()
        
        return reminders
    
    def _get_health_reminders(self):
        """获取健康状态提醒"""
        reminders = []
        conn = self.get_connection()
        if not conn:
            return reminders
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            query = """
            SELECT 
                mp.id as plant_id,
                mp.nickname,
                ps.name as species_name,
                mp.health_status,
                mp.growth_stage,
                mp.last_watered,
                gr.health_score,
                gr.record_date
            FROM my_plants mp
            JOIN plant_species ps ON mp.species_id = ps.id
            LEFT JOIN growth_records gr ON mp.id = gr.plant_id 
                AND gr.record_date = (SELECT MAX(record_date) FROM growth_records WHERE plant_id = mp.id)
            WHERE mp.health_status IN ('需关注', '生病', '濒危')
            """
            
            cursor.execute(query)
            plants = cursor.fetchall()
            
            for plant in plants:
                health_status = plant['health_status']
                
                if health_status == '濒危':
                    urgency = "紧急"
                    priority = 4
                    action = "立即检查并采取救治措施"
                elif health_status == '生病':
                    urgency = "高"
                    priority = 3
                    action = "检查病虫害，调整养护方式"
                else:  # 需关注
                    urgency = "中"
                    priority = 2
                    action = "加强观察，适当调整养护"
                
                reminders.append({
                    'type': '🏥 健康提醒',
                    'plant_id': plant['plant_id'],
                    'plant_name': f"{plant['nickname']} ({plant['species_name']})",
                    'message': f"健康状态: {health_status}，需要特别关注",
                    'urgency': urgency,
                    'priority': priority,
                    'suggested_action': action,
                    'last_action': plant['last_watered']
                })
            
            cursor.close()
            
        except Exception as e:
            print(f"获取健康提醒错误: {e}")
        finally:
            conn.close()
        
        return reminders
    
    def _get_seasonal_reminders(self):
        """获取季节性提醒"""
        reminders = []
        current_month = datetime.now().month
        season = self._get_current_season(current_month)
        
        seasonal_tips = {
            'spring': {
                'message': '🌸 春季是植物生长旺季，可以增加浇水和施肥频率',
                'actions': ['增加浇水频率', '开始施肥', '检查病虫害', '考虑换盆']
            },
            'summer': {
                'message': '☀️ 夏季高温，注意防晒和保持适当湿度',
                'actions': ['避免正午暴晒', '增加喷雾保湿', '注意通风']
            },
            'autumn': {
                'message': '🍂 秋季逐渐减少水肥，为越冬做准备',
                'actions': ['减少浇水', '停止施肥', '清理枯叶']
            },
            'winter': {
                'message': '⛄️ 冬季注意防寒，减少浇水',
                'actions': ['减少浇水', '保持温暖', '避免冷风直吹']
            }
        }
        
        if season in seasonal_tips:
            reminders.append({
                'type': '📅 季节性提醒',
                'plant_id': None,
                'plant_name': '所有植物',
                'message': seasonal_tips[season]['message'],
                'urgency': '低',
                'priority': 1,
                'suggested_action': ' | '.join(seasonal_tips[season]['actions']),
                'last_action': None
            })
        
        return reminders
    
    def _get_current_season(self, month):
        """获取当前季节"""
        if month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'autumn'
        else:
            return 'winter'
    
    def get_reminder_statistics(self):
        """获取提醒统计信息"""
        reminders = self.get_smart_reminders()
        
        stats = {
            'total': len(reminders),
            'urgent': len([r for r in reminders if r['urgency'] in ['紧急', '高']]),
            'medium': len([r for r in reminders if r['urgency'] == '中']),
            'low': len([r for r in reminders if r['urgency'] == '低']),
            'by_type': {}
        }
        
        # 按类型统计
        for reminder in reminders:
            reminder_type = reminder['type']
            if reminder_type not in stats['by_type']:
                stats['by_type'][reminder_type] = 0
            stats['by_type'][reminder_type] += 1
        
        return stats