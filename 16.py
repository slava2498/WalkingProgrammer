import sqlite3
import time


conn = sqlite3.connect('sqlite.db')
cursor = conn.cursor()

# Список данных для добавления
employees = [('Employee ' + str(i), 30 + i % 10, 'Position ' + str(i % 5)) for i in range(1000000)]

# Вставка данных через цикл
start_time = time.time()

cursor.executemany("INSERT INTO employees (name, age, position) VALUES (?, ?, ?)", employees)

# Сохраняем изменения
conn.commit()

# Замер времени
end_time = time.time()
print(f"Время вставки данных через цикл: {end_time - start_time:.10f} секунд")


# # Вставка данных за один запрос
# start_time = time.time()
#
# cursor.executemany("INSERT INTO employees (name, age, position) VALUES (?, ?, ?)", employees)
#
# # Сохраняем изменения
# conn.commit()
#
# # Замер времени
# end_time = time.time()
# print(f"Время множественной вставки: {end_time - start_time:.2f} секунд")


# # Вставка данных с управлением транзакциями
# start_time = time.time()
#
# # Открываем транзакцию вручную
# conn.execute("BEGIN")
#
# for emp in employees:
#     cursor.execute("INSERT INTO employees (name, age, position) VALUES (?, ?, ?)", emp)
#
# # Закрываем транзакцию вручную
# conn.commit()
#
# # Замер времени
# end_time = time.time()
# print(f"Время вставки с ручным управлением транзакциями: {end_time - start_time:.2f} секунд»)
