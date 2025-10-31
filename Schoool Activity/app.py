from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import sqlite3
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'campus_event_system_secret_key_2024'
app.config['DATABASE'] = 'campus_events.db'

# 导入数据库模型
try:
    from models import init_db, get_db_connection, close_db_connection
except ImportError:
    # 如果models.py不存在，创建一个简单的版本
    def init_db():
        pass
    def get_db_connection():
        return None
    def close_db_connection(conn):
        pass

# app.py - 修复数据库初始化部分
def initialize_database():
    """初始化数据库"""
    print("检查数据库初始化...")
    if not os.path.exists(app.config['DATABASE']):
        print("数据库文件不存在，开始初始化...")
        init_db()
    else:
        print("数据库文件已存在，跳过初始化")
        
    # 无论如何都检查表结构
    try:
        conn = get_db_connection()
        if conn:
            # 检查用户表是否存在
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if not cursor.fetchone():
                print("用户表不存在，重新初始化数据库...")
                conn.close()
                # 删除旧数据库文件重新创建
                if os.path.exists(app.config['DATABASE']):
                    os.remove(app.config['DATABASE'])
                init_db()
            else:
                print("✓ 数据库表结构正常")
                conn.close()
    except Exception as e:
        print(f"数据库检查失败: {e}")
        # 重新初始化
        if os.path.exists(app.config['DATABASE']):
            os.remove(app.config['DATABASE'])
        init_db()
# 活动状态管理函数
def safe_update_event_statuses():
    """安全地更新活动状态，处理可能的数据库结构问题"""
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        # 检查必要的列是否存在
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(events)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'end_time' not in columns or 'status' not in columns:
            print("数据库结构不完整，跳过状态更新")
            return
        
        # 获取当前时间
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 更新已开始但未标记为进行中的活动
        cursor.execute('''
            UPDATE events 
            SET status = 'ongoing' 
            WHERE datetime(date_time) <= datetime(?) 
            AND datetime(end_time) > datetime(?)
            AND status = 'upcoming'
        ''', (now, now))
        
        # 更新已结束的活动
        cursor.execute('''
            UPDATE events 
            SET status = 'completed' 
            WHERE datetime(end_time) <= datetime(?)
            AND status IN ('upcoming', 'ongoing')
        ''', (now,))
        
        conn.commit()
        print("活动状态更新成功")
        
    except Exception as e:
        print(f"更新活动状态时出现错误: {e}")
    finally:
        conn.close()

def update_all_event_statuses():
    """更新所有活动状态"""
    try:
        safe_update_event_statuses()
        print("活动状态更新完成")
    except Exception as e:
        print(f"活动状态更新失败: {e}")

# 在应用启动时初始化数据库和更新状态
with app.app_context():
    initialize_database()
    update_all_event_statuses()

# 首页
@app.route('/')
def index():
    """系统首页"""
    return render_template('index.html')

# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录处理"""
    # 如果已登录，重定向到仪表盘
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        if conn:
            user = conn.execute(
                'SELECT * FROM users WHERE username = ? AND password = ?', 
                (username, password)
            ).fetchone()
            conn.close()
            
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                session['email'] = user['email'] if 'email' in user.keys() else ''
                flash(f'欢迎回来，{user["username"]}！', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('用户名或密码错误，请重试。', 'error')
        else:
            flash('数据库连接失败，请检查系统配置。', 'error')
    
    return render_template('login.html')

# 用户注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册处理"""
    # 如果已登录，重定向到仪表盘
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    # 社团许可证密钥
    CLUB_LICENSE_KEY = "ZHIMA"
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']
        email = request.form.get('email', '')
        license_key = request.form.get('license_key', '')
        
        # 验证密码确认
        if password != confirm_password:
            flash('密码与确认密码不匹配，请重试。', 'error')
            return render_template('register.html')
        
        # 验证用户名长度
        if len(username) < 3:
            flash('用户名至少需要3个字符。', 'error')
            return render_template('register.html')
        
        # 验证密码长度
        if len(password) < 6:
            flash('密码至少需要6个字符。', 'error')
            return render_template('register.html')
        
        # 社团注册验证许可证
        if role == 'club':
            if not license_key:
                flash('社团注册需要提供许可证。', 'error')
                return render_template('register.html')
            
            if license_key != CLUB_LICENSE_KEY:
                flash('社团许可证错误，注册失败。请确认许可证是否正确或联系学校管理部门。', 'error')
                return render_template('register.html')
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)',
                    (username, password, role, email)
                )
                conn.commit()
                user_id = cursor.lastrowid
                conn.close()
                
                if role == 'club':
                    flash('社团注册成功！请登录您的账户。', 'success')
                else:
                    flash('注册成功！请登录您的账户。', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                conn.close()
                flash('用户名已存在，请选择其他用户名。', 'error')
            except Exception as e:
                conn.close()
                flash(f'注册失败：{str(e)}', 'error')
        else:
            flash('数据库连接失败，请检查系统配置。', 'error')
    
    return render_template('register.html')

# 用户仪表盘
@app.route('/dashboard')
def dashboard():
    """用户仪表盘"""
    if 'user_id' not in session:
        flash('请先登录以访问仪表盘。', 'warning')
        return redirect(url_for('login'))
    
    # 更新活动状态
    safe_update_event_statuses()
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return render_template('error.html', message='数据库连接失败')
    
    # 获取当前时间
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if session['role'] == 'student':
        # 学生仪表盘
        try:
            events = conn.execute('''
                SELECT e.*, u.username as club_name, 
                       (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id) as registered_count,
                       (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id AND r.student_id = ?) as is_registered
                FROM events e
                JOIN users u ON e.club_id = u.id
                WHERE (e.status = 'upcoming' OR e.status = 'ongoing')
                ORDER BY e.date_time
            ''', (session['user_id'],)).fetchall()
            
            # 获取已报名的活动
            registered_events = conn.execute('''
                SELECT e.*, u.username as club_name
                FROM events e
                JOIN registrations r ON e.id = r.event_id
                JOIN users u ON e.club_id = u.id
                WHERE r.student_id = ?
                ORDER BY 
                    CASE 
                        WHEN e.status = 'ongoing' THEN 1
                        WHEN e.status = 'upcoming' THEN 2
                        WHEN e.status = 'completed' THEN 3
                        ELSE 4
                    END,
                    e.date_time
            ''', (session['user_id'],)).fetchall()
            
            # 获取可评价的活动（已结束且已报名但未评价）
            reviewable_events = conn.execute('''
                SELECT e.*, u.username as club_name
                FROM events e
                JOIN registrations r ON e.id = r.event_id
                JOIN users u ON e.club_id = u.id
                WHERE r.student_id = ? 
                AND e.status = 'completed'
                AND NOT EXISTS (
                    SELECT 1 FROM reviews rev 
                    WHERE rev.event_id = e.id AND rev.student_id = ?
                )
            ''', (session['user_id'], session['user_id'])).fetchall()
            
            # 修复：正确计算已完成评价的数量
            reviewed_events_count = conn.execute('''
                SELECT COUNT(DISTINCT r.event_id) 
                FROM reviews r 
                JOIN events e ON r.event_id = e.id 
                WHERE r.student_id = ? AND e.status = 'completed'
            ''', (session['user_id'],)).fetchone()[0]
            
            conn.close()
            
            return render_template('student_dashboard.html', 
                                  events=events, 
                                  registered_events=registered_events,
                                  reviewable_events=reviewable_events,
                                  reviewed_events_count=reviewed_events_count,
                                  now=now)
        except Exception as e:
            conn.close()
            flash(f'加载数据失败：{str(e)}', 'error')
            return render_template('student_dashboard.html', events=[], registered_events=[], reviewable_events=[], reviewed_events_count=0, now=now)
    
    else:  # 社团用户
        try:
            # 获取该社团发布的活动
            events = conn.execute('''
                SELECT e.*, 
                       (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id) as registered_count
                FROM events e
                WHERE e.club_id = ?
                ORDER BY 
                    CASE 
                        WHEN e.status = 'ongoing' THEN 1
                        WHEN e.status = 'upcoming' THEN 2
                        WHEN e.status = 'completed' THEN 3
                        ELSE 4
                    END,
                    e.date_time DESC
            ''', (session['user_id'],)).fetchall()
            
            # 计算统计数据
            total_participants = sum([event['registered_count'] for event in events]) if events else 0
            
            upcoming_events = len([event for event in events if event['status'] == 'upcoming']) if events else 0
            ongoing_events = len([event for event in events if event['status'] == 'ongoing']) if events else 0
            completed_events = len([event for event in events if event['status'] == 'completed']) if events else 0
            
            # 获取最近评价
            recent_reviews = conn.execute('''
                SELECT r.*, e.title as event_title, u.username as student_name
                FROM reviews r
                JOIN events e ON r.event_id = e.id
                JOIN users u ON r.student_id = u.id
                WHERE e.club_id = ?
                ORDER BY r.reviewed_at DESC
                LIMIT 5
            ''', (session['user_id'],)).fetchall()
            
            conn.close()
            
            return render_template('club_dashboard.html', 
                                 events=events, 
                                 total_participants=total_participants,
                                 upcoming_events=upcoming_events,
                                 ongoing_events=ongoing_events,
                                 completed_events=completed_events,
                                 recent_reviews=recent_reviews,
                                 now=now)
        except Exception as e:
            conn.close()
            flash(f'加载数据失败：{str(e)}', 'error')
            return render_template('club_dashboard.html', events=[], total_participants=0, upcoming_events=0, ongoing_events=0, completed_events=0, recent_reviews=[], now=now)

# 发布活动 - 更新版本支持分类
@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    """发布新活动 - 支持分类选择"""
    if 'user_id' not in session or session['role'] != 'club':
        flash('只有社团用户可以发布活动。', 'error')
        return redirect(url_for('login'))
    
    # 获取所有分类
    conn = get_db_connection()
    categories = []
    try:
        categories = conn.execute('SELECT * FROM event_categories ORDER BY name').fetchall()
    except Exception as e:
        print(f"获取分类失败: {e}")
        # 如果分类表不存在，继续执行但不显示分类
    finally:
        conn.close()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date_time = request.form['date_time']
        end_time = request.form['end_time']
        location = request.form['location']
        max_participants = int(request.form['max_participants'])
        selected_categories = request.form.getlist('categories')
        
        # 验证时间
        try:
            start_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
            end_time_dt = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
            
            if start_time <= datetime.now():
                flash('活动开始时间必须晚于当前时间。', 'error')
                return render_template('create_event.html', categories=categories)
            
            if end_time_dt <= start_time:
                flash('活动结束时间必须晚于开始时间。', 'error')
                return render_template('create_event.html', categories=categories)
                
        except ValueError:
            flash('时间格式不正确。', 'error')
            return render_template('create_event.html', categories=categories)
        
        # 验证参与人数
        if max_participants <= 0:
            flash('参与人数必须大于0。', 'error')
            return render_template('create_event.html', categories=categories)
        
        conn = get_db_connection()
        if conn:
            try:
                # 插入活动
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO events (title, description, date_time, end_time, location, max_participants, club_id, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'upcoming')
                ''', (title, description, date_time, end_time, location, max_participants, session['user_id']))
                
                event_id = cursor.lastrowid
                
                # 添加分类关联（如果分类表存在）
                if selected_categories:
                    for category_id in selected_categories:
                        try:
                            cursor.execute(
                                'INSERT INTO event_category_relations (event_id, category_id) VALUES (?, ?)',
                                (event_id, category_id)
                            )
                        except Exception as e:
                            print(f"添加分类关联失败: {e}")
                            # 如果分类关联表不存在，忽略错误继续执行
                
                conn.commit()
                conn.close()
                
                flash('活动发布成功！', 'success')
                return redirect(url_for('dashboard'))
            except Exception as e:
                conn.close()
                flash(f'发布活动失败：{str(e)}', 'error')
        else:
            flash('数据库连接失败，请检查系统配置。', 'error')
    
    return render_template('create_event.html', categories=categories)

# # 编辑活动
# @app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
# def edit_event(event_id):
#     """编辑活动信息"""
#     if 'user_id' not in session or session['role'] != 'club':
#         flash('只有社团用户可以编辑活动。', 'error')
#         return redirect(url_for('login'))
    
#     conn = get_db_connection()
#     if not conn:
#         flash('数据库连接失败，请检查系统配置。', 'error')
#         return redirect(url_for('dashboard'))
    
#     # 验证活动属于当前社团
#     event = conn.execute(
#         'SELECT * FROM events WHERE id = ? AND club_id = ?',
#         (event_id, session['user_id'])
#     ).fetchone()
    
#     if not event:
#         flash('无权编辑此活动或活动不存在。', 'error')
#         conn.close()
#         return redirect(url_for('dashboard'))
    
#     if request.method == 'POST':
#         title = request.form['title']
#         description = request.form['description']
#         date_time = request.form['date_time']
#         location = request.form['location']
#         max_participants = int(request.form['max_participants'])
        
#         # 检查新的人数限制是否小于当前报名人数
#         registered_count = conn.execute(
#             'SELECT COUNT(*) FROM registrations WHERE event_id = ?', (event_id,)
#         ).fetchone()[0]
        
#         if max_participants < registered_count:
#             flash(f'报名人数已超过新设置的限制。当前有{registered_count}人报名，请设置更大的限制。', 'error')
#             conn.close()
#             return redirect(url_for('edit_event', event_id=event_id))
        
#         try:
#             conn.execute('''
#                 UPDATE events 
#                 SET title = ?, description = ?, date_time = ?, location = ?, max_participants = ?
#                 WHERE id = ?
#             ''', (title, description, date_time, location, max_participants, event_id))
#             conn.commit()
#             conn.close()
            
#             flash('活动更新成功！', 'success')
#             return redirect(url_for('dashboard'))
#         except Exception as e:
#             conn.close()
#             flash(f'更新活动失败：{str(e)}', 'error')
    
#     conn.close()
#     return render_template('edit_event.html', event=event)

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    """编辑活动信息"""
    if 'user_id' not in session or session['role'] != 'club':
        flash('只有社团用户可以编辑活动。', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return redirect(url_for('dashboard'))
    
    # 验证活动属于当前社团
    event = conn.execute(
        'SELECT * FROM events WHERE id = ? AND club_id = ?',
        (event_id, session['user_id'])
    ).fetchone()
    
    if not event:
        flash('无权编辑此活动或活动不存在。', 'error')
        conn.close()
        return redirect(url_for('dashboard'))
    
    # 获取当前报名人数
    registered_count = conn.execute(
        'SELECT COUNT(*) FROM registrations WHERE event_id = ?', (event_id,)
    ).fetchone()[0]
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date_time = request.form['date_time']
        location = request.form['location']
        max_participants = int(request.form['max_participants'])
        
        # 验证时间格式
        try:
            event_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
            if event_time <= datetime.now():
                flash('活动开始时间必须晚于当前时间。', 'error')
                conn.close()
                return render_template('edit_event.html', event=event, registered_count=registered_count)
        except ValueError:
            flash('时间格式不正确。', 'error')
            conn.close()
            return render_template('edit_event.html', event=event, registered_count=registered_count)
        
        # 检查新的人数限制是否小于当前报名人数
        if max_participants < registered_count:
            flash(f'报名人数已超过新设置的限制。当前有{registered_count}人报名，请设置更大的限制。', 'error')
            conn.close()
            return render_template('edit_event.html', event=event, registered_count=registered_count)
        
        try:
            # 更新活动信息
            conn.execute('''
                UPDATE events 
                SET title = ?, description = ?, date_time = ?, location = ?, max_participants = ?
                WHERE id = ?
            ''', (title, description, date_time, location, max_participants, event_id))
            conn.commit()
            
            flash('活动更新成功！', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            conn.rollback()
            flash(f'更新活动失败：{str(e)}', 'error')
    
    conn.close()
    return render_template('edit_event.html', event=event, registered_count=registered_count)






# 删除活动
@app.route('/delete_event/<int:event_id>')
def delete_event(event_id):
    """删除活动"""
    if 'user_id' not in session or session['role'] != 'club':
        flash('只有社团用户可以删除活动。', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return redirect(url_for('dashboard'))
    
    # 验证活动属于当前社团
    event = conn.execute(
        'SELECT * FROM events WHERE id = ? AND club_id = ?',
        (event_id, session['user_id'])
    ).fetchone()
    
    if not event:
        flash('无权删除此活动或活动不存在。', 'error')
        conn.close()
        return redirect(url_for('dashboard'))
    
    try:
        # 删除相关评价
        conn.execute('DELETE FROM reviews WHERE event_id = ?', (event_id,))
        # 删除相关报名
        conn.execute('DELETE FROM registrations WHERE event_id = ?', (event_id,))
        # 删除活动
        conn.execute('DELETE FROM events WHERE id = ?', (event_id,))
        
        conn.commit()
        conn.close()
        
        flash('活动删除成功！', 'success')
    except Exception as e:
        conn.close()
        flash(f'删除活动失败：{str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

# 报名活动
@app.route('/register_event/<int:event_id>')
def register_event(event_id):
    """学生报名活动"""
    if 'user_id' not in session or session['role'] != 'student':
        flash('只有学生可以报名活动。', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return redirect(url_for('dashboard'))
    
    # 检查是否已报名
    existing = conn.execute(
        'SELECT * FROM registrations WHERE student_id = ? AND event_id = ?',
        (session['user_id'], event_id)
    ).fetchone()
    
    if existing:
        flash('您已报名此活动。', 'info')
        conn.close()
        return redirect(url_for('dashboard'))
    
    # 检查活动是否存在
    event = conn.execute(
        'SELECT * FROM events WHERE id = ?', (event_id,)
    ).fetchone()
    
    if not event:
        flash('活动不存在。', 'error')
        conn.close()
        return redirect(url_for('dashboard'))
    
    # 检查活动状态
    if event['status'] != 'upcoming' and event['status'] != 'ongoing':
        flash('该活动已结束或取消，无法报名。', 'error')
        conn.close()
        return redirect(url_for('dashboard'))
    
    # 检查活动是否已开始
    try:
        event_time = datetime.strptime(event['date_time'], '%Y-%m-%d %H:%M:%S')
        if datetime.now() > event_time:
            flash('活动已开始，无法报名。', 'error')
            conn.close()
            return redirect(url_for('dashboard'))
    except:
        # 如果时间格式不匹配，尝试其他格式
        try:
            event_time = datetime.strptime(event['date_time'], '%Y-%m-%d %H:%M')
            if datetime.now() > event_time:
                flash('活动已开始，无法报名。', 'error')
                conn.close()
                return redirect(url_for('dashboard'))
        except:
            pass
    
    # 检查活动人数是否已满
    registered_count = conn.execute(
        'SELECT COUNT(*) FROM registrations WHERE event_id = ?', (event_id,)
    ).fetchone()[0]
    
    if registered_count >= event['max_participants']:
        flash('活动人数已满，无法报名。', 'error')
        conn.close()
        return redirect(url_for('dashboard'))
    
    try:
        conn.execute(
            'INSERT INTO registrations (student_id, event_id) VALUES (?, ?)',
            (session['user_id'], event_id)
        )
        conn.commit()
        conn.close()
        
        flash('报名成功！', 'success')
    except Exception as e:
        conn.close()
        flash(f'报名失败：{str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

# 取消报名
@app.route('/cancel_registration/<int:event_id>')
def cancel_registration(event_id):
    """学生取消活动报名"""
    if 'user_id' not in session or session['role'] != 'student':
        flash('只有学生可以取消报名。', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return redirect(url_for('dashboard'))
    
    # 检查是否已报名
    existing = conn.execute(
        'SELECT * FROM registrations WHERE student_id = ? AND event_id = ?',
        (session['user_id'], event_id)
    ).fetchone()
    
    if not existing:
        flash('您未报名此活动。', 'error')
        conn.close()
        return redirect(url_for('dashboard'))
    
    # 检查活动是否已开始
    event = conn.execute(
        'SELECT date_time FROM events WHERE id = ?', (event_id,)
    ).fetchone()
    
    try:
        event_time = datetime.strptime(event['date_time'], '%Y-%m-%d %H:%M:%S')
        if datetime.now() > event_time:
            flash('活动已开始，无法取消报名。', 'error')
            conn.close()
            return redirect(url_for('dashboard'))
    except:
        try:
            event_time = datetime.strptime(event['date_time'], '%Y-%m-%d %H:%M')
            if datetime.now() > event_time:
                flash('活动已开始，无法取消报名。', 'error')
                conn.close()
                return redirect(url_for('dashboard'))
        except:
            pass
    
    try:
        conn.execute(
            'DELETE FROM registrations WHERE student_id = ? AND event_id = ?',
            (session['user_id'], event_id)
        )
        conn.commit()
        conn.close()
        
        flash('取消报名成功！', 'success')
    except Exception as e:
        conn.close()
        flash(f'取消报名失败：{str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

# 手动结束活动
@app.route('/end_event/<int:event_id>')
def end_event(event_id):
    """社团手动结束活动"""
    if 'user_id' not in session or session['role'] != 'club':
        flash('只有社团用户可以结束活动。', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return redirect(url_for('dashboard'))
    
    # 验证活动属于当前社团
    event = conn.execute(
        'SELECT * FROM events WHERE id = ? AND club_id = ?',
        (event_id, session['user_id'])
    ).fetchone()
    
    if not event:
        flash('无权操作此活动或活动不存在。', 'error')
        conn.close()
        return redirect(url_for('dashboard'))
    
    # 检查活动是否已经结束
    if event['status'] == 'completed':
        flash('活动已经结束。', 'info')
        conn.close()
        return redirect(url_for('dashboard'))
    
    try:
        conn.execute(
            'UPDATE events SET status = "completed", end_time = ? WHERE id = ?',
            (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), event_id)
        )
        conn.commit()
        conn.close()
        
        flash('活动已手动结束！', 'success')
    except Exception as e:
        conn.close()
        flash(f'结束活动失败：{str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

# # 取消活动
# @app.route('/cancel_event/<int:event_id>')
# def cancel_event(event_id):
#     """社团取消活动"""
#     if 'user_id' not in session or session['role'] != 'club':
#         flash('只有社团用户可以取消活动。', 'error')
#         return redirect(url_for('login'))
    
#     conn = get_db_connection()
#     if not conn:
#         flash('数据库连接失败，请检查系统配置。', 'error')
#         return redirect(url_for('dashboard'))
    
#     # 验证活动属于当前社团
#     event = conn.execute(
#         'SELECT * FROM events WHERE id = ? AND club_id = ?',
#         (event_id, session['user_id'])
#     ).fetchone()
    
#     if not event:
#         flash('无权操作此活动或活动不存在。', 'error')
#         conn.close()
#         return redirect(url_for('dashboard'))
    
#     try:
#         conn.execute(
#             'UPDATE events SET status = "cancelled" WHERE id = ?',
#             (event_id,)
#         )
#         conn.commit()
#         conn.close()
        
#         flash('活动已取消！', 'success')
#     except Exception as e:
#         conn.close()
#         flash(f'取消活动失败：{str(e)}', 'error')
    
#     return redirect(url_for('dashboard'))


# 取消活动
@app.route('/cancel_event/<int:event_id>')
def cancel_event(event_id):
    """社团取消活动"""
    if 'user_id' not in session or session['role'] != 'club':
        flash('只有社团用户可以取消活动。', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return redirect(url_for('dashboard'))
    
    # 验证活动属于当前社团
    event = conn.execute(
        'SELECT * FROM events WHERE id = ? AND club_id = ?',
        (event_id, session['user_id'])
    ).fetchone()
    
    if not event:
        flash('无权操作此活动或活动不存在。', 'error')
        conn.close()
        return redirect(url_for('dashboard'))
    
    try:
        conn.execute(
            'UPDATE events SET status = "cancelled" WHERE id = ?',
            (event_id,)
        )
        conn.commit()
        flash('活动已取消！', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'取消活动失败：{str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('dashboard'))


# 评价活动
@app.route('/review_event/<int:event_id>', methods=['GET', 'POST'])
def review_event(event_id):
    """学生评价活动"""
    if 'user_id' not in session or session['role'] != 'student':
        flash('只有学生可以评价活动。', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return redirect(url_for('dashboard'))
    
    # 检查是否有资格评价（已报名且活动已结束且未评价过）
    event = conn.execute('''
        SELECT e.*, u.username as club_name
        FROM events e
        JOIN users u ON e.club_id = u.id
        WHERE e.id = ? AND e.status = 'completed'
        AND EXISTS (
            SELECT 1 FROM registrations r 
            WHERE r.event_id = e.id AND r.student_id = ?
        )
        AND NOT EXISTS (
            SELECT 1 FROM reviews rev 
            WHERE rev.event_id = e.id AND rev.student_id = ?
        )
    ''', (event_id, session['user_id'], session['user_id'])).fetchone()
    
    if not event:
        flash('您无法评价此活动（可能未报名、活动未结束或已评价过）。', 'error')
        conn.close()
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        content_score = int(request.form['content_score'])
        organization_score = int(request.form['organization_score'])
        comment = request.form['comment']
        
        # 验证评分范围
        if not (1 <= content_score <= 5) or not (1 <= organization_score <= 5):
            flash('评分必须在1-5分之间。', 'error')
            conn.close()
            return render_template('review_event.html', event=event)
        
        try:
            # 插入评价记录
            conn.execute('''
                INSERT INTO reviews (student_id, event_id, content_score, organization_score, comment)
                VALUES (?, ?, ?, ?, ?)
            ''', (session['user_id'], event_id, content_score, organization_score, comment))
            
            # 立即提交事务，确保数据保存
            conn.commit()
            conn.close()
            
            flash('评价提交成功！感谢您的反馈。', 'success')
            
            # 重定向到仪表盘，确保数据刷新
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            conn.close()
            flash(f'评价提交失败：{str(e)}', 'error')
    
    conn.close()
    return render_template('review_event.html', event=event)

# 活动报告
@app.route('/event_report/<int:event_id>')
def event_report(event_id):
    """查看活动详细报告"""
    if 'user_id' not in session or session['role'] != 'club':
        flash('只有社团用户可以查看活动报告。', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return redirect(url_for('dashboard'))
    
    # 验证活动属于当前社团
    event = conn.execute(
        'SELECT * FROM events WHERE id = ? AND club_id = ?',
        (event_id, session['user_id'])
    ).fetchone()
    
    if not event:
        flash('无权访问此活动报告或活动不存在。', 'error')
        conn.close()
        return redirect(url_for('dashboard'))
    
    try:
        # 获取报名数据
        registrations = conn.execute('''
            SELECT r.registered_at, u.username, u.email
            FROM registrations r
            JOIN users u ON r.student_id = u.id
            WHERE r.event_id = ?
            ORDER BY r.registered_at
        ''', (event_id,)).fetchall()
        
        # 获取评价数据
        reviews = conn.execute('''
            SELECT r.content_score, r.organization_score, r.comment, r.reviewed_at, u.username
            FROM reviews r
            JOIN users u ON r.student_id = u.id
            WHERE r.event_id = ?
            ORDER BY r.reviewed_at DESC
        ''', (event_id,)).fetchall()
        
        # 计算平均分
        avg_content = 0
        avg_organization = 0
        if reviews:
            avg_content = sum([r['content_score'] for r in reviews]) / len(reviews)
            avg_organization = sum([r['organization_score'] for r in reviews]) / len(reviews)
        
        conn.close()
        
        return render_template('event_report.html', 
                             event=event, 
                             registrations=registrations,
                             reviews=reviews,
                             avg_content=round(avg_content, 2),
                             avg_organization=round(avg_organization, 2))
    except Exception as e:
        conn.close()
        flash(f'生成报告失败：{str(e)}', 'error')
        return redirect(url_for('dashboard'))

# API: 获取报名趋势数据
@app.route('/api/registration_trend/<int:event_id>')
def registration_trend(event_id):
    """API接口：获取活动报名趋势数据"""
    if 'user_id' not in session:
        return jsonify({'error': '未登录'}), 401
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': '数据库连接失败'}), 500
    
    # 验证活动属于当前社团（如果是社团用户）
    if session['role'] == 'club':
        event = conn.execute(
            'SELECT * FROM events WHERE id = ? AND club_id = ?',
            (event_id, session['user_id'])
        ).fetchone()
        
        if not event:
            conn.close()
            return jsonify({'error': '无权访问此活动数据'}), 403
    
    try:
        # 获取按日期分组的报名人数
        registrations_by_date = conn.execute('''
            SELECT DATE(registered_at) as date, COUNT(*) as count
            FROM registrations
            WHERE event_id = ?
            GROUP BY DATE(registered_at)
            ORDER BY date
        ''', (event_id,)).fetchall()
        
        conn.close()
        
        # 准备图表数据
        dates = [row['date'] for row in registrations_by_date]
        counts = [row['count'] for row in registrations_by_date]
        
        cumulative_counts = []
        total = 0
        for count in counts:
            total += count
            cumulative_counts.append(total)
        
        return jsonify({
            'dates': dates,
            'daily_counts': counts,
            'cumulative_counts': cumulative_counts
        })
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# 搜索活动
@app.route('/search_events')
def search_events():
    """搜索活动"""
    if 'user_id' not in session or session['role'] != 'student':
        flash('请先登录以搜索活动。', 'warning')
        return redirect(url_for('login'))
    
    query = request.args.get('q', '')
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return render_template('search_events.html', events=[], query=query)
    
    try:
        if query:
            events = conn.execute('''
                SELECT e.*, u.username as club_name, 
                       (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id) as registered_count,
                       (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id AND r.student_id = ?) as is_registered
                FROM events e
                JOIN users u ON e.club_id = u.id
                WHERE (e.title LIKE ? OR e.description LIKE ? OR u.username LIKE ?)
                AND (e.status = 'upcoming' OR e.status = 'ongoing')
                ORDER BY e.date_time
            ''', (session['user_id'], f'%{query}%', f'%{query}%', f'%{query}%')).fetchall()
        else:
            events = conn.execute('''
                SELECT e.*, u.username as club_name, 
                       (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id) as registered_count,
                       (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id AND r.student_id = ?) as is_registered
                FROM events e
                JOIN users u ON e.club_id = u.id
                WHERE (e.status = 'upcoming' OR e.status = 'ongoing')
                ORDER BY e.date_time
            ''', (session['user_id'],)).fetchall()
        
        conn.close()
        return render_template('search_events.html', events=events, query=query)
    except Exception as e:
        conn.close()
        flash(f'搜索失败：{str(e)}', 'error')
        return render_template('search_events.html', events=[], query=query)

# 修改密码
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """修改用户密码"""
    if 'user_id' not in session:
        flash('请先登录以修改密码。', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('新密码与确认密码不匹配。', 'error')
            return render_template('change_password.html')
        
        if len(new_password) < 6:
            flash('新密码至少需要6个字符。', 'error')
            return render_template('change_password.html')
        
        conn = get_db_connection()
        if not conn:
            flash('数据库连接失败，请检查系统配置。', 'error')
            return render_template('change_password.html')
        
        user = conn.execute(
            'SELECT * FROM users WHERE id = ? AND password = ?',
            (session['user_id'], current_password)
        ).fetchone()
        
        if not user:
            flash('当前密码错误。', 'error')
            conn.close()
            return render_template('change_password.html')
        
        try:
            conn.execute(
                'UPDATE users SET password = ? WHERE id = ?',
                (new_password, session['user_id'])
            )
            conn.commit()
            conn.close()
            
            flash('密码修改成功！', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            conn.close()
            flash(f'密码修改失败：{str(e)}', 'error')
    
    return render_template('change_password.html')

# 用户个人资料 - 修复版本
@app.route('/profile')
def profile():
    """用户个人资料页面"""
    if 'user_id' not in session:
        flash('请先登录以查看个人资料。', 'warning')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return redirect(url_for('dashboard'))
    
    user = conn.execute(
        'SELECT * FROM users WHERE id = ?', (session['user_id'],)
    ).fetchone()
    
    if session['role'] == 'student':
        try:
            # 获取学生统计数据 - 修复统计逻辑
            registered_count = conn.execute(
                'SELECT COUNT(*) FROM registrations WHERE student_id = ?', 
                (session['user_id'],)
            ).fetchone()[0]
            
            # 修复：正确统计已评价的活动数量
            reviewed_count = conn.execute(
                'SELECT COUNT(DISTINCT event_id) FROM reviews WHERE student_id = ?', 
                (session['user_id'],)
            ).fetchone()[0]
            
            conn.close()
            return render_template('student_profile.html', 
                                 user=user, 
                                 registered_count=registered_count,
                                 reviewed_count=reviewed_count)
        except Exception as e:
            conn.close()
            flash(f'加载个人资料失败：{str(e)}', 'error')
            return render_template('student_profile.html', user=user, registered_count=0, reviewed_count=0)
    else:
        try:
            # 获取社团统计数据
            events_count = conn.execute(
                'SELECT COUNT(*) FROM events WHERE club_id = ?', 
                (session['user_id'],)
            ).fetchone()[0]
            
            total_participants = conn.execute('''
                SELECT COUNT(*) as total
                FROM registrations r
                JOIN events e ON r.event_id = e.id
                WHERE e.club_id = ?
            ''', (session['user_id'],)).fetchone()[0]
            
            # 计算平均评分
            avg_rating_result = conn.execute('''
                SELECT AVG((content_score + organization_score) / 2.0) as avg_rating
                FROM reviews r
                JOIN events e ON r.event_id = e.id
                WHERE e.club_id = ?
            ''', (session['user_id'],)).fetchone()
            
            avg_rating = round(avg_rating_result[0], 2) if avg_rating_result[0] is not None else 0
            
            conn.close()
            return render_template('club_profile.html', 
                                 user=user, 
                                 events_count=events_count,
                                 total_participants=total_participants,
                                 avg_rating=avg_rating)
        except Exception as e:
            conn.close()
            flash(f'加载个人资料失败：{str(e)}', 'error')
            return render_template('club_profile.html', user=user, events_count=0, total_participants=0, avg_rating=0)

# 活动收藏功能
@app.route('/favorite_event/<int:event_id>')
def favorite_event(event_id):
    """收藏活动"""
    if 'user_id' not in session or session['role'] != 'student':
        flash('只有学生可以收藏活动。', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        # 检查是否已收藏
        existing = conn.execute(
            'SELECT * FROM favorites WHERE student_id = ? AND event_id = ?',
            (session['user_id'], event_id)
        ).fetchone()
        
        if existing:
            flash('您已收藏此活动。', 'info')
        else:
            # 添加收藏
            conn.execute(
                'INSERT INTO favorites (student_id, event_id) VALUES (?, ?)',
                (session['user_id'], event_id)
            )
            conn.commit()
            flash('活动收藏成功！', 'success')
            
    except Exception as e:
        flash(f'收藏失败：{str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/unfavorite_event/<int:event_id>')
def unfavorite_event(event_id):
    """取消收藏活动"""
    if 'user_id' not in session or session['role'] != 'student':
        flash('只有学生可以取消收藏活动。', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        conn.execute(
            'DELETE FROM favorites WHERE student_id = ? AND event_id = ?',
            (session['user_id'], event_id)
        )
        conn.commit()
        flash('已取消收藏活动。', 'success')
    except Exception as e:
        flash(f'取消收藏失败：{str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/favorites')
def favorites():
    """查看收藏的活动"""
    if 'user_id' not in session or session['role'] != 'student':
        flash('只有学生可以查看收藏。', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return render_template('favorites.html', events=[])
    
    try:
        events = conn.execute('''
            SELECT e.*, u.username as club_name, 
                   (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id) as registered_count,
                   (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id AND r.student_id = ?) as is_registered,
                   f.created_at
            FROM events e
            JOIN users u ON e.club_id = u.id
            JOIN favorites f ON e.id = f.event_id
            WHERE f.student_id = ? AND (e.status = 'upcoming' OR e.status = 'ongoing')
            ORDER BY f.created_at DESC
        ''', (session['user_id'], session['user_id'])).fetchall()
        
        conn.close()
        return render_template('favorites.html', events=events)
    except Exception as e:
        conn.close()
        flash(f'加载收藏失败：{str(e)}', 'error')
        return render_template('favorites.html', events=[])

# 活动分类功能
@app.route('/categories')
def categories():
    """查看活动分类"""
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return render_template('categories.html', categories=[])
    
    try:
        # 修复：获取分类及其活动数量
        categories = conn.execute('''
            SELECT ec.*, COUNT(ecr.event_id) as event_count
            FROM event_categories ec
            LEFT JOIN event_category_relations ecr ON ec.id = ecr.category_id
            LEFT JOIN events e ON ecr.event_id = e.id AND (e.status = 'upcoming' OR e.status = 'ongoing')
            GROUP BY ec.id
            ORDER BY ec.name
        ''').fetchall()
        conn.close()
        return render_template('categories.html', categories=categories)
    except Exception as e:
        conn.close()
        print(f"加载分类错误: {e}")  # 调试信息
        flash(f'加载分类失败：{str(e)}', 'error')
        return render_template('categories.html', categories=[])
@app.route('/events_by_category/<int:category_id>')
def events_by_category(category_id):
    """按分类查看活动"""
    if 'user_id' not in session or session['role'] != 'student':
        flash('请先登录以查看活动。', 'warning')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return render_template('search_events.html', events=[], category_id=category_id)
    
    try:
        # 获取分类信息
        category = conn.execute(
            'SELECT * FROM event_categories WHERE id = ?', (category_id,)
        ).fetchone()
        
        # 获取该分类下的活动
        events = conn.execute('''
            SELECT e.*, u.username as club_name, 
                   (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id) as registered_count,
                   (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id AND r.student_id = ?) as is_registered
            FROM events e
            JOIN users u ON e.club_id = u.id
            JOIN event_category_relations ecr ON e.id = ecr.event_id
            WHERE ecr.category_id = ? AND (e.status = 'upcoming' OR e.status = 'ongoing')
            ORDER BY e.date_time
        ''', (session['user_id'], category_id)).fetchall()
        
        conn.close()
        return render_template('category_events.html', 
                             events=events, 
                             category=category,
                             category_id=category_id)
    except Exception as e:
        conn.close()
        flash(f'加载活动失败：{str(e)}', 'error')
        return render_template('search_events.html', events=[], category_id=category_id)

# 数据导出功能
@app.route('/export_event_data/<int:event_id>')
def export_event_data(event_id):
    """导出活动数据为CSV"""
    if 'user_id' not in session or session['role'] != 'club':
        flash('只有社团用户可以导出数据。', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if not conn:
        flash('数据库连接失败，请检查系统配置。', 'error')
        return redirect(url_for('dashboard'))
    
    # 验证活动属于当前社团
    event = conn.execute(
        'SELECT * FROM events WHERE id = ? AND club_id = ?',
        (event_id, session['user_id'])
    ).fetchone()
    
    if not event:
        flash('无权访问此活动数据或活动不存在。', 'error')
        conn.close()
        return redirect(url_for('dashboard'))
    
    try:
        import csv
        import io
        from datetime import datetime
        
        # 创建内存文件
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 写入表头
        writer.writerow(['活动数据导出 - ' + event['title']])
        writer.writerow(['导出时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow([])
        writer.writerow(['活动信息'])
        writer.writerow(['标题', event['title']])
        writer.writerow(['描述', event['description'] or ''])
        writer.writerow(['开始时间', event['date_time']])
        writer.writerow(['结束时间', event['end_time']])
        writer.writerow(['地点', event['location']])
        writer.writerow(['最大参与人数', event['max_participants']])
        writer.writerow(['状态', event['status']])
        writer.writerow([])
        
        # 报名数据
        writer.writerow(['报名名单'])
        writer.writerow(['用户名', '邮箱', '报名时间'])
        
        registrations = conn.execute('''
            SELECT u.username, u.email, r.registered_at
            FROM registrations r
            JOIN users u ON r.student_id = u.id
            WHERE r.event_id = ?
            ORDER BY r.registered_at
        ''', (event_id,)).fetchall()
        
        for reg in registrations:
            writer.writerow([reg['username'], reg['email'] or '', reg['registered_at']])
        
        writer.writerow([])
        writer.writerow(['总计报名人数', len(registrations)])
        writer.writerow(['报名率', f"{(len(registrations) / event['max_participants'] * 100):.1f}%"])
        writer.writerow([])
        
        # 评价数据
        writer.writerow(['评价数据'])
        writer.writerow(['用户名', '内容丰富度', '组织有序性', '评价内容', '评价时间'])
        
        reviews = conn.execute('''
            SELECT u.username, r.content_score, r.organization_score, r.comment, r.reviewed_at
            FROM reviews r
            JOIN users u ON r.student_id = u.id
            WHERE r.event_id = ?
            ORDER BY r.reviewed_at DESC
        ''', (event_id,)).fetchall()
        
        for review in reviews:
            writer.writerow([
                review['username'],
                review['content_score'],
                review['organization_score'],
                review['comment'] or '',
                review['reviewed_at']
            ])
        
        writer.writerow([])
        writer.writerow(['总计评价数', len(reviews)])
        
        if reviews:
            avg_content = sum([r['content_score'] for r in reviews]) / len(reviews)
            avg_organization = sum([r['organization_score'] for r in reviews]) / len(reviews)
            writer.writerow(['平均内容评分', f"{avg_content:.2f}"])
            writer.writerow(['平均组织评分', f"{avg_organization:.2f}"])
            writer.writerow(['综合评分', f"{(avg_content + avg_organization) / 2:.2f}"])
        
        conn.close()
        
        # 准备下载响应
        output.seek(0)
        filename = f"event_{event_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        from flask import Response
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment;filename={filename}"}
        )
        
    except Exception as e:
        conn.close()
        flash(f'导出数据失败：{str(e)}', 'error')
        return redirect(url_for('event_report', event_id=event_id))

# 登出
@app.route('/logout')
def logout():
    """用户登出"""
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('index'))

# 错误处理
@app.errorhandler(404)
def page_not_found(e):
    """404错误处理"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """500错误处理"""
    return render_template('500.html'), 500

# 健康检查端点
@app.route('/health')
def health_check():
    """健康检查端点"""
    try:
        conn = get_db_connection()
        if conn:
            conn.execute('SELECT 1')
            conn.close()
            return jsonify({'status': 'healthy', 'database': 'connected'})
        else:
            return jsonify({'status': 'unhealthy', 'error': 'Database connection failed'}), 500
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

# 关于页面
@app.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')

# 帮助页面
@app.route('/help')
def help_page():
    """帮助页面"""
    return render_template('help.html')

if __name__ == '__main__':
    # 确保数据库存在
    initialize_database()
    
    # 运行应用
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )