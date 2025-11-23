# src/models/database.py
import mysql.connector
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config import Config

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
        return cls._instance
    
    def get_connection(self):
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host=Config.MYSQL_HOST,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    database=Config.MYSQL_DB,
                    port=Config.MYSQL_PORT
                )
                print("✅ 数据库连接成功")
            except mysql.connector.Error as err:
                print(f"❌ 数据库连接错误: {err}")
                return None
        return self.connection
    
    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None
            print("✅ 数据库连接已关闭")