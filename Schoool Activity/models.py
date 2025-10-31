import sqlite3
from datetime import datetime, timedelta
import random
import os

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect('campus_events.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row  # 使返回的行像字典一样工作
    return conn

def close_db_connection(conn):
    """关闭数据库连接"""
    if conn:
        conn.close()

def init_db():
    """初始化数据库，创建所有表并插入示例数据"""
    conn = sqlite3.connect('campus_events.db', check_same_thread=False)
    cursor = conn.cursor()
    
    print("开始创建数据库表...")
    
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL, -- 'student' or 'club'
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ 用户表创建完成")
    
    # 创建活动分类表（必须先于活动表创建）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            color TEXT DEFAULT '#007bff',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ 活动分类表创建完成")
    
    # 创建活动表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            date_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            location TEXT NOT NULL,
            max_participants INTEGER NOT NULL,
            club_id INTEGER NOT NULL,
            status TEXT DEFAULT 'upcoming',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (club_id) REFERENCES users (id)
        )
    ''')
    print("✓ 活动表创建完成")
    
    # 创建活动-分类关联表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event_category_relations (
            event_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            PRIMARY KEY (event_id, category_id),
            FOREIGN KEY (event_id) REFERENCES events (id),
            FOREIGN KEY (category_id) REFERENCES event_categories (id)
        )
    ''')
    print("✓ 活动-分类关联表创建完成")
    
    # 创建报名表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES users (id),
            FOREIGN KEY (event_id) REFERENCES events (id),
            UNIQUE(student_id, event_id)
        )
    ''')
    print("✓ 报名表创建完成")
    
    # 创建评价表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            content_score INTEGER NOT NULL CHECK (content_score >= 1 AND content_score <= 5),
            organization_score INTEGER NOT NULL CHECK (organization_score >= 1 AND organization_score <= 5),
            comment TEXT,
            reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES users (id),
            FOREIGN KEY (event_id) REFERENCES events (id),
            UNIQUE(student_id, event_id)
        )
    ''')
    print("✓ 评价表创建完成")
    
    # 创建收藏表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES users (id),
            FOREIGN KEY (event_id) REFERENCES events (id),
            UNIQUE(student_id, event_id)
        )
    ''')
    print("✓ 收藏表创建完成")
    
    # 插入初始分类数据
    insert_initial_categories(cursor)
    
    # 插入初始用户和示例数据
    insert_initial_data(cursor)
    
    conn.commit()
    conn.close()
    print("🎉 数据库初始化完成！")

def insert_initial_categories(cursor):
    """插入初始分类数据"""
    print("开始插入初始分类...")
    
    categories = [
        ('技术竞赛', '编程、算法、创新技术相关的竞赛活动', '#dc3545'),
        ('艺术创作', '绘画、摄影、设计等艺术类活动', '#6f42c1'),
        ('体育运动', '篮球、足球、羽毛球等体育比赛和活动', '#20c997'),
        ('学术讲座', '专业知识、学术研究相关的讲座', '#fd7e14'),
        ('文艺表演', '音乐、舞蹈、戏剧等表演活动', '#e83e8c'),
        ('社会实践', '志愿服务、社会调查等实践活动', '#28a745'),
        ('技能培训', '工作坊、培训课程等技能提升活动', '#17a2b8'),
        ('娱乐休闲', '游戏、观影、聚会等休闲活动', '#ffc107')
    ]
    
    for category in categories:
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO event_categories (name, description, color) VALUES (?, ?, ?)",
                category
            )
        except Exception as e:
            print(f"插入分类失败 {category[0]}: {e}")
    
    print("✓ 初始分类插入完成")

def insert_initial_data(cursor):
    """插入初始示例数据"""
    print("开始插入初始数据...")
    
    # 插入社团用户
    clubs = [
        ('tech_club', 'password123', 'club', 'tech@campus.edu'),
        ('art_club', 'password123', 'club', 'art@campus.edu'),
        ('sports_club', 'password123', 'club', 'sports@campus.edu'),
        ('music_club', 'password123', 'club', 'music@campus.edu'),
        ('dance_club', 'password123', 'club', 'dance@campus.edu')
    ]
    
    for club in clubs:
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO users (username, password, role, email) VALUES (?, ?, ?, ?)",
                club
            )
        except Exception as e:
            print(f"插入社团用户失败 {club[0]}: {e}")
    
    # 插入学生用户
    students = [
        ('student1', 'password123', 'student', 'student1@campus.edu'),
        ('student2', 'password123', 'student', 'student2@campus.edu'),
        ('student3', 'password123', 'student', 'student3@campus.edu'),
        ('student4', 'password123', 'student', 'student4@campus.edu'),
        ('student5', 'password123', 'student', 'student5@campus.edu'),
        ('student6', 'password123', 'student', 'student6@campus.edu')
    ]
    
    for student in students:
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO users (username, password, role, email) VALUES (?, ?, ?, ?)",
                student
            )
        except Exception as e:
            print(f"插入学生用户失败 {student[0]}: {e}")
    
    print("✓ 用户数据插入完成")
    
    # 插入示例活动
    insert_sample_events(cursor)
    
    # 添加报名记录和评价
    insert_sample_registrations_and_reviews(cursor)
    
    print("✓ 示例数据插入完成")

def insert_sample_events(cursor):
    """插入示例活动数据"""
    print("开始插入示例活动...")
    
    # 获取社团ID
    cursor.execute("SELECT id FROM users WHERE username='tech_club'")
    tech_club_result = cursor.fetchone()
    tech_club_id = tech_club_result[0] if tech_club_result else 1
    
    cursor.execute("SELECT id FROM users WHERE username='art_club'")
    art_club_result = cursor.fetchone()
    art_club_id = art_club_result[0] if art_club_result else 2
    
    cursor.execute("SELECT id FROM users WHERE username='sports_club'")
    sports_club_result = cursor.fetchone()
    sports_club_id = sports_club_result[0] if sports_club_result else 3
    
    cursor.execute("SELECT id FROM users WHERE username='music_club'")
    music_club_result = cursor.fetchone()
    music_club_id = music_club_result[0] if music_club_result else 4
    
    cursor.execute("SELECT id FROM users WHERE username='dance_club'")
    dance_club_result = cursor.fetchone()
    dance_club_id = dance_club_result[0] if dance_club_result else 5
    
    # 获取分类ID
    cursor.execute("SELECT id FROM event_categories WHERE name='技术竞赛'")
    tech_category_result = cursor.fetchone()
    tech_category_id = tech_category_result[0] if tech_category_result else 1
    
    cursor.execute("SELECT id FROM event_categories WHERE name='艺术创作'")
    art_category_result = cursor.fetchone()
    art_category_id = art_category_result[0] if art_category_result else 2
    
    cursor.execute("SELECT id FROM event_categories WHERE name='体育运动'")
    sports_category_result = cursor.fetchone()
    sports_category_id = sports_category_result[0] if sports_category_result else 3
    
    cursor.execute("SELECT id FROM event_categories WHERE name='学术讲座'")
    lecture_category_result = cursor.fetchone()
    lecture_category_id = lecture_category_result[0] if lecture_category_result else 4
    
    cursor.execute("SELECT id FROM event_categories WHERE name='文艺表演'")
    performance_category_result = cursor.fetchone()
    performance_category_id = performance_category_result[0] if performance_category_result else 5
    
    # 示例活动数据 - 使用未来时间
    now = datetime.now()
    sample_events = [
        # 技术类活动
        ('校园编程竞赛', '年度编程大赛，挑战你的算法和编程能力！', 
         (now + timedelta(days=5)).strftime('%Y-%m-%d 14:00:00'),
         (now + timedelta(days=5)).strftime('%Y-%m-%d 17:00:00'),
         '计算机学院101', 50, tech_club_id),
        
        ('AI技术前沿讲座', '人工智能最新技术分享与实战演示', 
         (now + timedelta(days=7)).strftime('%Y-%m-%d 16:00:00'),
         (now + timedelta(days=7)).strftime('%Y-%m-%d 18:00:00'),
         '学术报告厅', 100, tech_club_id),
        
        ('Web开发工作坊', '从零开始学习现代Web开发技术', 
         (now + timedelta(days=10)).strftime('%Y-%m-%d 10:00:00'),
         (now + timedelta(days=10)).strftime('%Y-%m-%d 12:00:00'),
         '信息楼301', 30, tech_club_id),
        
        # 艺术类活动
        ('校园艺术展', '学生艺术作品展览与交流', 
         (now + timedelta(days=3)).strftime('%Y-%m-%d 09:00:00'),
         (now + timedelta(days=3)).strftime('%Y-%m-%d 17:00:00'),
         '艺术馆大厅', 200, art_club_id),
        
        ('摄影技巧培训', '专业摄影师指导手机摄影技巧', 
         (now + timedelta(days=6)).strftime('%Y-%m-%d 14:00:00'),
         (now + timedelta(days=6)).strftime('%Y-%m-%d 16:00:00'),
         '艺术楼205', 25, art_club_id),
        
        # 体育类活动
        ('校园篮球联赛', '学院间篮球友谊比赛', 
         (now + timedelta(days=4)).strftime('%Y-%m-%d 15:00:00'),
         (now + timedelta(days=4)).strftime('%Y-%m-%d 17:00:00'),
         '体育馆主馆', 40, sports_club_id),
        
        ('羽毛球训练营', '羽毛球基础技巧训练', 
         (now + timedelta(days=8)).strftime('%Y-%m-%d 19:00:00'),
         (now + timedelta(days=8)).strftime('%Y-%m-%d 21:00:00'),
         '羽毛球馆', 20, sports_club_id),
        
        # 文艺表演
        ('校园音乐会', '学生乐队音乐表演晚会', 
         (now + timedelta(days=2)).strftime('%Y-%m-%d 19:00:00'),
         (now + timedelta(days=2)).strftime('%Y-%m-%d 21:00:00'),
         '学生活动中心', 150, music_club_id),
        
        ('舞蹈表演晚会', '现代舞与民族舞精彩表演', 
         (now + timedelta(days=9)).strftime('%Y-%m-%d 18:30:00'),
         (now + timedelta(days=9)).strftime('%Y-%m-%d 20:30:00'),
         '大礼堂', 300, dance_club_id)
    ]
    
    # 插入活动
    event_ids = []
    for event in sample_events:
        try:
            cursor.execute('''
                INSERT INTO events (title, description, date_time, end_time, location, max_participants, club_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', event)
            event_ids.append(cursor.lastrowid)
        except Exception as e:
            print(f"插入活动失败 {event[0]}: {e}")
    
    # 关联活动与分类
    event_categories = [
        (event_ids[0], tech_category_id),  # 编程竞赛 - 技术竞赛
        (event_ids[1], tech_category_id),  # AI讲座 - 技术竞赛
        (event_ids[1], lecture_category_id),  # AI讲座 - 学术讲座
        (event_ids[2], tech_category_id),  # Web开发 - 技术竞赛
        (event_ids[3], art_category_id),   # 艺术展 - 艺术创作
        (event_ids[4], art_category_id),   # 摄影培训 - 艺术创作
        (event_ids[5], sports_category_id), # 篮球赛 - 体育运动
        (event_ids[6], sports_category_id), # 羽毛球 - 体育运动
        (event_ids[7], performance_category_id), # 音乐会 - 文艺表演
        (event_ids[8], performance_category_id)  # 舞蹈晚会 - 文艺表演
    ]
    
    for event_category in event_categories:
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO event_category_relations (event_id, category_id) VALUES (?, ?)",
                event_category
            )
        except Exception as e:
            print(f"关联活动分类失败: {e}")
    
    print("✓ 示例活动插入完成")

def insert_sample_registrations_and_reviews(cursor):
    """插入示例报名记录和评价数据"""
    print("开始插入示例报名和评价数据...")
    
    # 获取所有学生ID
    cursor.execute("SELECT id FROM users WHERE role='student'")
    student_ids = [row[0] for row in cursor.fetchall()]
    
    # 获取所有活动ID
    cursor.execute("SELECT id, date_time FROM events")
    events = cursor.fetchall()
    
    # 为每个活动随机添加报名记录
    for event_id, event_time in events:
        # 随机选择一些学生报名（1-4人）
        num_participants = random.randint(1, min(4, len(student_ids)))
        participants = random.sample(student_ids, num_participants)
        
        for student_id in participants:
            try:
                cursor.execute(
                    'INSERT OR IGNORE INTO registrations (student_id, event_id) VALUES (?, ?)',
                    (student_id, event_id)
                )
                
                # 随机添加一些收藏
                if random.random() > 0.7:  # 30%的概率收藏
                    try:
                        cursor.execute(
                            'INSERT OR IGNORE INTO favorites (student_id, event_id) VALUES (?, ?)',
                            (student_id, event_id)
                        )
                    except:
                        pass
                
            except Exception as e:
                print(f"插入报名记录失败: {e}")
    
    print("✓ 示例报名数据插入完成")

def update_event_statuses():
    """自动更新活动状态"""
    conn = get_db_connection()
    
    # 获取当前时间
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # 更新已开始但未标记为进行中的活动
        conn.execute('''
            UPDATE events 
            SET status = 'ongoing' 
            WHERE datetime(date_time) <= datetime(?) 
            AND datetime(end_time) > datetime(?)
            AND status = 'upcoming'
        ''', (now, now))
        
        # 更新已结束的活动
        conn.execute('''
            UPDATE events 
            SET status = 'completed' 
            WHERE datetime(end_time) <= datetime(?)
            AND status IN ('upcoming', 'ongoing')
        ''', (now,))
        
        conn.commit()
        print("✓ 活动状态更新完成")
    except Exception as e:
        print(f"更新活动状态失败: {e}")
    finally:
        conn.close()

# 数据库操作函数
def execute_query(query, params=()):
    """执行查询并返回结果"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

def execute_update(query, params=()):
    """执行更新操作并提交"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def get_user_by_username(username):
    """根据用户名获取用户信息"""
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    """根据用户ID获取用户信息"""
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    conn.close()
    return user

def get_event_by_id(event_id):
    """根据活动ID获取活动信息"""
    conn = get_db_connection()
    event = conn.execute(
        'SELECT * FROM events WHERE id = ?', (event_id,)
    ).fetchone()
    conn.close()
    return event

def get_events_by_club(club_id):
    """获取社团发布的所有活动"""
    conn = get_db_connection()
    events = conn.execute(
        'SELECT * FROM events WHERE club_id = ? ORDER BY date_time', (club_id,)
    ).fetchall()
    conn.close()
    return events

def get_categories():
    """获取所有分类"""
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM event_categories ORDER BY name').fetchall()
    conn.close()
    return categories

def get_categories_with_event_count():
    """获取所有分类及其活动数量"""
    conn = get_db_connection()
    categories = conn.execute('''
        SELECT ec.*, COUNT(ecr.event_id) as event_count
        FROM event_categories ec
        LEFT JOIN event_category_relations ecr ON ec.id = ecr.category_id
        LEFT JOIN events e ON ecr.event_id = e.id AND (e.status = 'upcoming' OR e.status = 'ongoing')
        GROUP BY ec.id
        ORDER BY ec.name
    ''').fetchall()
    conn.close()
    return categories

def get_events_by_category(category_id, student_id=None):
    """根据分类获取活动"""
    conn = get_db_connection()
    
    if student_id:
        events = conn.execute('''
            SELECT e.*, u.username as club_name, 
                   (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id) as registered_count,
                   (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id AND r.student_id = ?) as is_registered,
                   (SELECT COUNT(*) FROM favorites f WHERE f.event_id = e.id AND f.student_id = ?) as is_favorited
            FROM events e
            JOIN users u ON e.club_id = u.id
            JOIN event_category_relations ecr ON e.id = ecr.event_id
            WHERE ecr.category_id = ? AND (e.status = 'upcoming' OR e.status = 'ongoing')
            ORDER BY e.date_time
        ''', (student_id, student_id, category_id)).fetchall()
    else:
        events = conn.execute('''
            SELECT e.*, u.username as club_name,
                   (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id) as registered_count
            FROM events e
            JOIN users u ON e.club_id = u.id
            JOIN event_category_relations ecr ON e.id = ecr.event_id
            WHERE ecr.category_id = ? AND (e.status = 'upcoming' OR e.status = 'ongoing')
            ORDER BY e.date_time
        ''', (category_id,)).fetchall()
    
    conn.close()
    return events

def is_event_favorited(student_id, event_id):
    """检查活动是否被收藏"""
    conn = get_db_connection()
    favorite = conn.execute(
        'SELECT * FROM favorites WHERE student_id = ? AND event_id = ?',
        (student_id, event_id)
    ).fetchone()
    conn.close()
    return favorite is not None

def add_favorite(student_id, event_id):
    """添加收藏"""
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO favorites (student_id, event_id) VALUES (?, ?)',
            (student_id, event_id)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def remove_favorite(student_id, event_id):
    """移除收藏"""
    conn = get_db_connection()
    conn.execute(
        'DELETE FROM favorites WHERE student_id = ? AND event_id = ?',
        (student_id, event_id)
    )
    conn.commit()
    conn.close()

# 如果直接运行此文件，则初始化数据库
if __name__ == '__main__':
    print("开始初始化数据库...")
    init_db()
    
    # 测试查询
    print("\n测试查询：")
    users = execute_query("SELECT COUNT(*) as count FROM users")
    print(f"用户数量: {users[0][0]}")
    
    events = execute_query("SELECT COUNT(*) as count FROM events")
    print(f"活动数量: {events[0][0]}")
    
    categories = execute_query("SELECT COUNT(*) as count FROM event_categories")
    print(f"分类数量: {categories[0][0]}")
    
    print("🎉 数据库模型测试完成！")