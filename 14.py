import sqlite3

# # Подключаемся к базе данных (или создаем её, если она не существует)
# conn = sqlite3.connect('example.db')
#
# # Создаем курсор для выполнения SQL-запросов
# cursor = conn.cursor()
#
# # Создаем таблицу
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         name TEXT,
#         age INTEGER
#     )
# ''')
#
# # Сохраняем изменения
# conn.commit()
#
# # Закрываем соединение
# conn.close()

# conn = sqlite3.connect('example.db')
# cursor = conn.cursor()
#
# # Вставляем данные в таблицу
# cursor.execute('''
#     INSERT INTO users (name, age)
#     VALUES (?, ?)
# ''', ('Alice', 30))
#
# cursor.execute('''
#     INSERT INTO users (name, age)
#     VALUES (?, ?)
# ''', ('Bob', xxx))
#
# # Сохраняем изменения
# conn.commit()
#
# conn.close()
#
#
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Извлекаем данные из таблицы
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
#
#
# conn = sqlite3.connect('example.db')
# cursor = conn.cursor()
#
# # Обновляем данные в таблице
# cursor.execute('''
#     UPDATE users
#     SET age = ?
#     WHERE name = ?
# ''', (31, 'Alice'))
#
# # Удаляем данные из таблицы
# cursor.execute('''
#     DELETE FROM users
#     WHERE name = ?
# ''', ('Bob',))
#
# # Сохраняем изменения
# conn.commit()
#
# conn.close()