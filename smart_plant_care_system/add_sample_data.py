import mysql.connector
import sys
import os
sys.path.append(os.path.dirname(__file__))

try:
    from config import Config
except ImportError:
    print("❌ 无法导入config，使用手动配置...")
    class ManualConfig:
        MYSQL_HOST = 'localhost'
        MYSQL_USER = 'root'
        MYSQL_PASSWORD = '123456'
        MYSQL_DB = 'plant_care_system'
        MYSQL_PORT = 3306
    Config = ManualConfig()

def seed_plant_species():
    """添加示例植物品种数据"""
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor()
        
        print("🌱 开始添加示例植物数据...")
        
        plant_species = [
            {
                'name': '绿萝', 'scientific_name': 'Epipremnum aureum', 'family': '天南星科',
                'plant_type': '观叶植物', 'difficulty_level': '非常简单', 'light_requirements': '耐阴',
                'optimal_temperature_min': 15, 'optimal_temperature_max': 30, 'ideal_humidity_min': 40,
                'ideal_humidity_max': 70, 'watering_frequency_summer': 7, 'watering_frequency_winter': 14,
                'fertilizing_frequency': 30, 'repotting_frequency': 12, 'toxicity': '微毒',
                'description': '非常适合室内养护的观叶植物，净化空气能力强，生长快速，易于繁殖。',
                'care_tips': '避免阳光直射，保持土壤微湿，定期擦拭叶片。',
                'common_problems': '过度浇水会导致根部腐烂，光照不足会使叶片变小。'
            },
            {
                'name': '多肉植物', 'scientific_name': 'Succulent plants', 'family': '多种科属',
                'plant_type': '多肉植物', 'difficulty_level': '简单', 'light_requirements': '强光',
                'optimal_temperature_min': 10, 'optimal_temperature_max': 35, 'ideal_humidity_min': 30,
                'ideal_humidity_max': 50, 'watering_frequency_summer': 10, 'watering_frequency_winter': 30,
                'fertilizing_frequency': 60, 'repotting_frequency': 24, 'toxicity': '无毒',
                'description': '叶片肥厚多汁，耐旱性强，形态各异，适合盆栽观赏。',
                'care_tips': '少浇水，多晒太阳，保证良好排水，使用透气性好的土壤。',
                'common_problems': '过度浇水易腐烂，光照不足会徒长。'
            },
            {
                'name': '龟背竹', 'scientific_name': 'Monstera deliciosa', 'family': '天南星科',
                'plant_type': '观叶植物', 'difficulty_level': '中等', 'light_requirements': '中光照',
                'optimal_temperature_min': 18, 'optimal_temperature_max': 28, 'ideal_humidity_min': 50,
                'ideal_humidity_max': 80, 'watering_frequency_summer': 5, 'watering_frequency_winter': 10,
                'fertilizing_frequency': 15, 'repotting_frequency': 12, 'toxicity': '微毒',
                'description': '叶片有独特的孔洞，观赏价值高，是流行的室内观叶植物。',
                'care_tips': '喜欢温暖湿润环境，需要适当光照，定期喷雾增加湿度。',
                'common_problems': '空气干燥时叶缘会枯黄，光照过强会灼伤叶片。'
            },
            {
                'name': '仙人掌', 'scientific_name': 'Cactaceae', 'family': '仙人掌科',
                'plant_type': '多肉植物', 'difficulty_level': '非常简单', 'light_requirements': '强光',
                'optimal_temperature_min': 5, 'optimal_temperature_max': 40, 'ideal_humidity_min': 20,
                'ideal_humidity_max': 40, 'watering_frequency_summer': 15, 'watering_frequency_winter': 45,
                'fertilizing_frequency': 90, 'repotting_frequency': 36, 'toxicity': '无毒',
                'description': '极其耐旱的沙漠植物，形态独特，养护简单。',
                'care_tips': '极少浇水，需要充足阳光，冬季保持干燥。',
                'common_problems': '过度浇水是主要死因，光照不足会变形。'
            },
            {
                'name': '吊兰', 'scientific_name': 'Chlorophytum comosum', 'family': '天门冬科',
                'plant_type': '观叶植物', 'difficulty_level': '非常简单', 'light_requirements': '耐阴',
                'optimal_temperature_min': 10, 'optimal_temperature_max': 28, 'ideal_humidity_min': 40,
                'ideal_humidity_max': 70, 'watering_frequency_summer': 5, 'watering_frequency_winter': 10,
                'fertilizing_frequency': 30, 'repotting_frequency': 12, 'toxicity': '无毒',
                'description': '生长快速，易于养护，能有效净化室内空气。',
                'care_tips': '保持土壤湿润但不积水，适当光照叶片会更鲜艳。',
                'common_problems': '叶尖枯黄通常是因为水质或空气干燥。'
            }
        ]
        
        added_count = 0
        for plant in plant_species:
            # 检查是否已存在
            cursor.execute("SELECT id FROM plant_species WHERE name = %s", (plant['name'],))
            if not cursor.fetchone():
                query = """
                INSERT INTO plant_species 
                (name, scientific_name, family, plant_type, difficulty_level, 
                 light_requirements, optimal_temperature_min, optimal_temperature_max,
                 ideal_humidity_min, ideal_humidity_max, watering_frequency_summer,
                 watering_frequency_winter, fertilizing_frequency, repotting_frequency,
                 description, care_tips, common_problems, toxicity)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    plant['name'], plant['scientific_name'], plant['family'],
                    plant['plant_type'], plant['difficulty_level'], plant['light_requirements'],
                    plant['optimal_temperature_min'], plant['optimal_temperature_max'],
                    plant['ideal_humidity_min'], plant['ideal_humidity_max'],
                    plant['watering_frequency_summer'], plant['watering_frequency_winter'],
                    plant['fertilizing_frequency'], plant['repotting_frequency'],
                    plant['description'], plant['care_tips'], plant['common_problems'],
                    plant['toxicity']
                ))
                added_count += 1
                print(f"✅ 添加: {plant['name']}")
            else:
                print(f"⏩ 已存在: {plant['name']}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"🎉 示例植物数据添加完成！共添加 {added_count} 个新品种")
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ 数据库错误: {err}")
        return False
    except Exception as e:
        print(f"❌ 添加示例数据错误: {e}")
        return False

def add_sample_plants():
    """添加示例我的植物数据"""
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor(dictionary=True)
        
        print("\n🏡 开始添加示例我的植物...")
        
        # 获取植物品种ID
        cursor.execute("SELECT id, name FROM plant_species")
        species = cursor.fetchall()
        species_dict = {name: id for id, name in species}
        
        # 示例我的植物数据
        my_plants = [
            {
                'species_id': species_dict['绿萝'],
                'nickname': '小绿',
                'location': '客厅',
                'specific_spot': '电视柜旁边',
                'health_status': '健康',
                'growth_stage': '生长期',
                'notes': '2023年购买的，生长很好'
            },
            {
                'species_id': species_dict['多肉植物'],
                'nickname': '肉肉',
                'location': '阳台',
                'specific_spot': '东面窗台',
                'health_status': '非常健康',
                'growth_stage': '成熟期',
                'notes': '喜欢晒太阳，颜色很漂亮'
            },
            {
                'species_id': species_dict['龟背竹'],
                'nickname': '大叶',
                'location': '书房',
                'specific_spot': '书桌旁',
                'health_status': '一般',
                'growth_stage': '生长期',
                'notes': '新买的，还在适应环境'
            }
        ]
        
        added_count = 0
        for plant in my_plants:
            # 检查是否已存在
            cursor.execute("SELECT id FROM my_plants WHERE nickname = %s", (plant['nickname'],))
            if not cursor.fetchone():
                query = """
                INSERT INTO my_plants 
                (species_id, nickname, location, specific_spot, health_status, growth_stage, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    plant['species_id'], plant['nickname'], plant['location'],
                    plant['specific_spot'], plant['health_status'], plant['growth_stage'],
                    plant['notes']
                ))
                added_count += 1
                print(f"✅ 添加我的植物: {plant['nickname']}")
            else:
                print(f"⏩ 已存在: {plant['nickname']}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"🎉 示例我的植物添加完成！共添加 {added_count} 株植物")
        return True
        
    except Exception as e:
        print(f"❌ 添加我的植物错误: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🌿 智能植物养护系统 - 示例数据初始化")
    print("=" * 50)
    
    # 添加植物品种
    if seed_plant_species():
        # 添加我的植物
        add_sample_plants()
    
    print("\n🎊 所有示例数据添加完成！")
    print("现在可以运行 'python run.py' 启动应用程序了")