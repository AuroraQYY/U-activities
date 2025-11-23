# src/utils/report_exporter.py
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import Config
from models.plant_models import MyPlants, CareLogs, GrowthRecords

class ReportExporter:
    def __init__(self):
        self.my_plants_model = MyPlants()
        self.care_logs_model = CareLogs()
        self.growth_records_model = GrowthRecords()
        self.export_dir = os.path.join(Config.DATA_DIR, 'exports')
        os.makedirs(self.export_dir, exist_ok=True)
    
    def export_care_statistics(self, format_type='excel'):
        """导出养护统计报表"""
        try:
            # 获取统计数据
            plants = self.my_plants_model.get_all_plants()
            care_stats = self._get_care_statistics_data()
            
            if format_type == 'excel':
                return self._export_care_to_excel(care_stats, plants)
            elif format_type == 'csv':
                return self._export_care_to_csv(care_stats, plants)
            else:
                return None
                
        except Exception as e:
            print(f"导出养护统计错误: {e}")
            return None
    
    def export_growth_report(self, plant_id=None, format_type='excel'):
        """导出生长报告"""
        try:
            if plant_id:
                # 单个植物生长报告
                plant = self.my_plants_model.get_plant_by_id(plant_id)
                growth_data = self.growth_records_model.get_growth_statistics(plant_id)
                return self._export_single_growth_report(plant, growth_data, format_type)
            else:
                # 所有植物生长报告
                plants = self.my_plants_model.get_all_plants()
                return self._export_all_growth_report(plants, format_type)
                
        except Exception as e:
            print(f"导出生长报告错误: {e}")
            return None
    
    def export_health_report(self, format_type='excel'):
        """导出健康状态报告"""
        try:
            plants = self.my_plants_model.get_all_plants()
            health_data = self._get_health_report_data(plants)
            
            if format_type == 'excel':
                return self._export_health_to_excel(health_data, plants)
            elif format_type == 'csv':
                return self._export_health_to_csv(health_data, plants)
                
        except Exception as e:
            print(f"导出健康报告错误: {e}")
            return None
    
    def export_monthly_report(self, month=None, format_type='excel'):
        """导出月度报告"""
        try:
            if month is None:
                month = datetime.now().strftime('%Y-%m')
            
            monthly_data = self._get_monthly_report_data(month)
            
            if format_type == 'excel':
                return self._export_monthly_to_excel(monthly_data, month)
            elif format_type == 'csv':
                return self._export_monthly_to_csv(monthly_data, month)
                
        except Exception as e:
            print(f"导出月度报告错误: {e}")
            return None
    
    def _get_care_statistics_data(self):
        """获取养护统计数据"""
        # 这里实现具体的数据获取逻辑
        plants = self.my_plants_model.get_all_plants()
        care_data = []
        
        for plant in plants:
            care_logs = self.care_logs_model.get_plant_care_logs(plant['id'])

            last_care_dates = [log['care_date'] for log in care_logs if log['care_date']]
            last_care = max(last_care_dates) if last_care_dates else '无记录'

            care_data.append({
                'plant_id': plant['id'],
                'nickname': plant['nickname'],
                'species': plant['species_name'],
                'total_care': len(care_logs),
                'watering_count': len([log for log in care_logs if log['care_type'] == '浇水']),
                'fertilizing_count': len([log for log in care_logs if log['care_type'] == '施肥']),
                'last_care': last_care
            })
        
        return care_data
    
    def _export_care_to_excel(self, care_data, plants):
        """导出养护统计到Excel"""
        filename = f"养护统计报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(self.export_dir, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # 总体统计表
            summary_data = {
                '统计项目': ['总植物数量', '总养护记录', '平均每株养护次数', '需要关注的植物'],
                '数值': [
                    len(plants),
                    sum(item['total_care'] for item in care_data),
                    round(sum(item['total_care'] for item in care_data) / len(plants), 1),
                    len([p for p in plants if p['health_status'] in ['需关注', '生病', '濒危']])
                ]
            }
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='总体统计', index=False)
            
            # 详细养护记录表
            df_care = pd.DataFrame(care_data)
            df_care.to_excel(writer, sheet_name='养护详情', index=False)
            
            # 植物健康状态表
            health_data = []
            for plant in plants:
                health_data.append({
                    '植物昵称': plant['nickname'],
                    '品种': plant['species_name'],
                    '健康状态': plant['health_status'],
                    '生长阶段': plant['growth_stage'],
                    '最后浇水': plant['last_watered'],
                    '位置': plant['location']
                })
            df_health = pd.DataFrame(health_data)
            df_health.to_excel(writer, sheet_name='健康状态', index=False)
        
        return filepath
    
    def _export_care_to_csv(self, care_data, plants):
        """导出养护统计到CSV"""
        try:
            filename = f"养护统计报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join(self.export_dir, filename)
            
            # 创建主要数据表
            if care_data:
                df_care = pd.DataFrame(care_data)
                df_care.to_csv(filepath, index=False, encoding='utf-8-sig')
                return filepath
            else:
                return None
        except Exception as e:
            print(f"导出CSV错误: {e}")
            return None
    
    def _export_single_growth_report(self, plant, growth_data, format_type):
        """导出单个植物生长报告"""
        if format_type == 'excel':
            filename = f"{plant['nickname']}_生长报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = os.path.join(self.export_dir, filename)
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # 植物基本信息
                plant_info = {
                    '项目': ['昵称', '品种', '健康状态', '生长阶段', '位置', '最后浇水'],
                    '信息': [
                        plant['nickname'],
                        plant['species_name'],
                        plant['health_status'],
                        plant['growth_stage'],
                        plant['location'],
                        plant['last_watered'] or '无记录'
                    ]
                }
                df_info = pd.DataFrame(plant_info)
                df_info.to_excel(writer, sheet_name='植物信息', index=False)
                
                # 生长记录数据
                if growth_data and growth_data['trend_data']:
                    growth_records = growth_data['trend_data']
                    growth_list = []
                    for record in growth_records:
                        growth_list.append({
                            '记录日期': record['record_date'],
                            '高度(cm)': record.get('height_cm', ''),
                            '叶片数量': record.get('leaf_count', ''),
                            '健康评分': record.get('health_score', '')
                        })
                    df_growth = pd.DataFrame(growth_list)
                    df_growth.to_excel(writer, sheet_name='生长记录', index=False)
            
            return filepath
        
        return None
    
    def _get_health_report_data(self, plants):
        """获取健康报告数据"""
        health_distribution = {}
        plants_need_care = []
        
        for plant in plants:
            status = plant['health_status']
            health_distribution[status] = health_distribution.get(status, 0) + 1
            
            if status in ['需关注', '生病', '濒危']:
                plants_need_care.append(plant)
        
        return {
            'health_distribution': health_distribution,
            'plants_need_care': plants_need_care,
            'total_plants': len(plants),
            'healthy_count': len([p for p in plants if p['health_status'] in ['非常健康', '健康']])
        }
    
    def _export_health_to_excel(self, health_data, plants):
        """导出健康报告到Excel"""
        filename = f"植物健康报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(self.export_dir, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # 健康状态分布
            health_dist = []
            for status, count in health_data['health_distribution'].items():
                health_dist.append({
                    '健康状态': status,
                    '植物数量': count,
                    '占比': f"{(count/health_data['total_plants'])*100:.1f}%"
                })
            df_health_dist = pd.DataFrame(health_dist)
            df_health_dist.to_excel(writer, sheet_name='健康分布', index=False)
            
            # 需要关注的植物
            if health_data['plants_need_care']:
                need_care_data = []
                for plant in health_data['plants_need_care']:
                    need_care_data.append({
                        '植物昵称': plant['nickname'],
                        '品种': plant['species_name'],
                        '健康状态': plant['health_status'],
                        '位置': plant['location'],
                        '最后浇水': plant['last_watered'] or '无记录'
                    })
                df_need_care = pd.DataFrame(need_care_data)
                df_need_care.to_excel(writer, sheet_name='需关注植物', index=False)
        
        return filepath
    def _export_health_to_csv(self, health_data, plants):
        """导出健康报告到CSV"""
        try:
            filename = f"植物健康报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join(self.export_dir, filename)
            
            # 导出健康分布数据
            health_dist = []
            for status, count in health_data['health_distribution'].items():
                percentage = (count/health_data['total_plants'])*100 if health_data['total_plants'] > 0 else 0
                health_dist.append({
                    '健康状态': status,
                    '植物数量': count,
                    '占比': f"{percentage:.1f}%"
                })
            
            if health_dist:
                df_health = pd.DataFrame(health_dist)
                df_health.to_csv(filepath, index=False, encoding='utf-8-sig')
                return filepath
            else:
                return None
        except Exception as e:
            print(f"导出健康报告CSV错误: {e}")
            return None


    def _get_monthly_report_data(self, month):
        """获取月度报告数据 - 修复版本"""
        try:
            plants = self.my_plants_model.get_all_plants()
            
            # 修复：正确处理日期比较
            new_plants_count = 0
            for plant in plants:
                created_at = plant.get('created_at')
                if created_at:
                    # 如果是字符串，转换为日期
                    if isinstance(created_at, str):
                        try:
                            created_date = datetime.strptime(created_at.split()[0], '%Y-%m-%d')
                            if created_date.strftime('%Y-%m') == month:
                                new_plants_count += 1
                        except:
                            continue
                    # 如果是datetime对象
                    elif hasattr(created_at, 'strftime'):
                        if created_at.strftime('%Y-%m') == month:
                            new_plants_count += 1
            
            return {
                'report_month': month,
                'plant_count': len(plants),
                'new_plants': new_plants_count,
                'healthy_plants': len([p for p in plants if p['health_status'] in ['非常健康', '健康']]),
                'plants_need_care': len([p for p in plants if p['health_status'] in ['需关注', '生病', '濒危']]),
                'total_care_actions': 0,  # 简化实现
                'watering_count': 0,
                'fertilizing_count': 0,
                'other_care_count': 0,
                'growth_records': 0,
                'avg_health_score': 8.0
            }
        except Exception as e:
            print(f"获取月度数据错误: {e}")
            return {
                'report_month': month,
                'plant_count': 0,
                'new_plants': 0,
                'healthy_plants': 0,
                'plants_need_care': 0,
                'total_care_actions': 0,
                'watering_count': 0,
                'fertilizing_count': 0,
                'other_care_count': 0,
                'growth_records': 0,
                'avg_health_score': 0
            }

    
    def _export_monthly_to_excel(self, monthly_data, month):
        """导出月度报告到Excel"""
        filename = f"月度报告_{month}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(self.export_dir, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # 月度摘要
            summary_data = {
                '报告月份': [month],
                '植物总数': [monthly_data['plant_count']],
                '新增植物': [monthly_data['new_plants']],
                '健康植物': [monthly_data['healthy_plants']],
                '需关注植物': [monthly_data['plants_need_care']]
            }
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='月度摘要', index=False)
        
        return filepath

    def _export_monthly_to_csv(self, monthly_data, month):
        """导出月度报告到CSV"""
        try:
            filename = f"月度报告_{month}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join(self.export_dir, filename)
            
            summary_data = {
                '报告月份': [month],
                '植物总数': [monthly_data['plant_count']],
                '新增植物': [monthly_data['new_plants']],
                '健康植物': [monthly_data['healthy_plants']],
                '需关注植物': [monthly_data['plants_need_care']],
                '养护总次数': [monthly_data['total_care_actions']],
                '浇水次数': [monthly_data['watering_count']],
                '施肥次数': [monthly_data['fertilizing_count']],
                '平均健康评分': [monthly_data['avg_health_score']]
            }
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            return filepath
        except Exception as e:
            print(f"导出月度报告CSV错误: {e}")
            return None

    def get_export_formats(self):
        """获取支持的导出格式"""
        return ['excel', 'csv']

    def _export_all_growth_report(self, plants, format_type):
        """导出所有植物生长报告 - 简化实现"""
        # 这里可以实现所有植物的生长报告导出
        return None