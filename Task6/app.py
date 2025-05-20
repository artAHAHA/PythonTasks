# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, session
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session

# Имя файла базы данных
DATABASE = 'database.sql'


def init_db():
    """Инициализация базы данных с тестовыми данными"""
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Создаем основную таблицу пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Создаем таблицу для хранения истории изменений
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                changed_by TEXT,
                action TEXT NOT NULL,  -- 'INSERT', 'UPDATE' или 'DELETE'
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        # Добавляем тестовые данные
        test_users = [
            ('John Doe', 'john@example.com', 30),
            ('Jane Smith', 'jane@example.com', 25),
            ('Bob Johnson', 'bob@example.com', 40),
            ('Alice Brown', 'alice@example.com', 35)
        ]

        for user in test_users:
            cursor.execute('''
                INSERT INTO users (name, email, age) VALUES (?, ?, ?)
            ''', user)
            # Записываем в историю
            cursor.execute('''
                INSERT INTO users_history 
                (user_id, name, email, age, changed_by, action)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (cursor.lastrowid, user[0], user[1], user[2], 'system', 'INSERT'))

        conn.commit()
        conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query:
            try:
                conn = sqlite3.connect(DATABASE)
                conn.row_factory = sqlite3.Row  # Для доступа к столбцам по имени
                cursor = conn.cursor()

                # Выполняем запрос
                cursor.execute(query)

                # Если это SELECT, получаем данные
                if query.lower().startswith('select'):
                    rows = cursor.fetchall()
                    columns = [description[0] for description in cursor.description]
                    return render_template('index.html',
                                           rows=rows,
                                           columns=columns,
                                           query=query)
                else:
                    conn.commit()
                    return render_template('index.html',
                                           message=f"Query executed successfully. Rows affected: {cursor.rowcount}",
                                           query=query)

            except sqlite3.Error as e:
                return render_template('index.html', error=str(e), query=query)
            finally:
                conn.close()

    return render_template('index.html')


@app.route('/delete', methods=['POST'])
def delete_rows():
    try:
        data = request.get_json()
        ids = data.get('ids', [])
        if not ids:
            return jsonify({"status": "error", "message": "No IDs provided"}), 400

        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Получаем данные для истории перед удалением
        placeholders = ','.join('?' for _ in ids)
        cursor.execute(f'SELECT * FROM users WHERE id IN ({placeholders})', ids)
        users_to_delete = cursor.fetchall()

        # Счетчик удаленных строк
        total_deleted = 0

        # Удаляем пользователей и записываем в историю в одной транзакции
        for user in users_to_delete:
            # Удаляем одного пользователя
            cursor.execute('DELETE FROM users WHERE id = ?', (user['id'],))
            total_deleted += cursor.rowcount

            # Записываем в историю
            cursor.execute('''
                INSERT INTO users_history 
                (user_id, name, email, age, changed_by, action)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user['id'], user['name'], user['email'], user['age'],
                  session.get('username', 'anonymous'), 'DELETE'))

        conn.commit()
        return jsonify({
            "status": "success",
            "message": f"Deleted {total_deleted} rows"
        })

    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if conn:
            conn.close()
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            age = request.form['age']

            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            # Вставляем нового пользователя
            cursor.execute('''
                INSERT INTO users (name, email, age) VALUES (?, ?, ?)
            ''', (name, email, age))

            # Записываем в историю
            user_id = cursor.lastrowid
            cursor.execute('''
                INSERT INTO users_history 
                (user_id, name, email, age, changed_by, action)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, name, email, age, session.get('username', 'anonymous'), 'INSERT'))

            conn.commit()
            return jsonify({"status": "success", "message": "User added successfully"})

        except sqlite3.IntegrityError:
            return jsonify({"status": "error", "message": "Email already exists"}), 400
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
        finally:
            conn.close()

    return render_template('insert_form.html')


@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            age = request.form['age']

            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            # Получаем текущие данные для истории
            cursor.execute('SELECT name, email, age FROM users WHERE id = ?', (user_id,))
            old_data = cursor.fetchone()

            # Обновляем пользователя
            cursor.execute('''
                UPDATE users 
                SET name = ?, email = ?, age = ? 
                WHERE id = ?
            ''', (name, email, age, user_id))

            # Записываем в историю
            cursor.execute('''
                INSERT INTO users_history 
                (user_id, name, email, age, changed_by, action)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, old_data[0], old_data[1], old_data[2], 'system', 'UPDATE'))

            conn.commit()
            return jsonify({"status": "success", "message": "User updated successfully"})

        except sqlite3.IntegrityError:
            return jsonify({"status": "error", "message": "Email already exists"}), 400
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
        finally:
            conn.close()

    # GET request - показать форму с текущими данными
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return "User not found", 404

    return render_template('update_form.html', user=user)


@app.route('/history/<int:user_id>')
def history(user_id):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Получаем историю изменений для пользователя
    cursor.execute('''
        SELECT * FROM users_history 
        WHERE user_id = ? 
        ORDER BY changed_at DESC
    ''', (user_id,))
    history_rows = cursor.fetchall()

    # Получаем текущие данные пользователя
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    current_user = cursor.fetchone()

    conn.close()

    return render_template('history.html',
                           history_rows=history_rows,
                           current_user=current_user,
                           columns=['id', 'name', 'email', 'age', 'changed_at', 'changed_by', 'action'])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)