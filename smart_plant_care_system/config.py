import os

class Config:
    # 数据库配置 - 修改为你的实际密码
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '123456'  # ← 重要：修改为你的MySQL密码！
    MYSQL_DB = 'plant_care_system'
    MYSQL_PORT = 3306
    
    # 应用配置
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    IMAGE_DIR = os.path.join(DATA_DIR, 'images')
    
    # 创建必要的目录
    @staticmethod
    def create_directories():
        os.makedirs(Config.IMAGE_DIR, exist_ok=True)
        os.makedirs(os.path.join(Config.DATA_DIR, 'exports'), exist_ok=True)

if __name__ == "__main__":
    print("🔧 配置信息:")
    print(f"数据库: {Config.MYSQL_DB}")
    print(f"主机: {Config.MYSQL_HOST}")
    print(f"用户: {Config.MYSQL_USER}")
    print("✅ 配置加载成功")