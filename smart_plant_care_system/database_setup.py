import mysql.connector
from config import Config

def create_database():
    """创建数据库"""
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ 数据库 {Config.MYSQL_DB} 创建成功")
        
        cursor.close()
        conn.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ 数据库创建错误: {err}")
        return False

def create_tables():
    """创建所有数据表"""
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT
        )
        cursor = conn.cursor()
        
        with open('schema.sql', 'r', encoding='utf-8') as file:
            sql_commands = file.read().split(';')
            
            for command in sql_commands:
                if command.strip():
                    try:
                        cursor.execute(command)
                    except mysql.connector.Error as err:
                        print(f"⚠️ SQL执行警告: {err}")
        
        conn.commit()
        
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✅ 数据库表创建完成，共有 {len(tables)} 张表")
        
        cursor.close()
        conn.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ 表创建错误: {err}")
        return False

def initialize_database():
    """完整的数据库初始化"""
    print("🚀 开始初始化数据库...")
    Config.create_directories()
    
    if create_database() and create_tables():
        print("🎉 数据库初始化完成！")
        return True
    
    print("❌ 数据库初始化失败！")
    return False

if __name__ == "__main__":
    initialize_database()