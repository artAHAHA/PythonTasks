# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Имя файла базы данных
DATABASE = 'database.sql'


def init_db():
    """Инициализация базы данных с тестовыми данными"""
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Создаем тестовую таблицу
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Добавляем тестовые данные
        test_users = [
            ('John Doe', 'john@example.com', 30),
            ('Jane Smith', 'jane@example.com', 25),
            ('Bob Johnson', 'bob@example.com', 40),
            ('Alice Brown', 'alice@example.com', 35)
        ]

        cursor.executemany('''
            INSERT INTO users (name, email, age) VALUES (?, ?, ?)
        ''', test_users)

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
        ids = request.form.getlist('ids[]')
        if not ids:
            return jsonify({"status": "error", "message": "No IDs provided"}), 400

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Безопасное формирование запроса
        placeholders = ','.join('?' for _ in ids)
        query = f"DELETE FROM users WHERE id IN ({placeholders})"

        cursor.execute(query, ids)
        conn.commit()

        return jsonify({
            "status": "success",
            "message": f"Deleted {cursor.rowcount} rows"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)