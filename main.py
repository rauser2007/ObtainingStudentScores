import sqlite3

# Підключення до бази даних users.db
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Створення таблиці students, якщо вона не існує
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
);
""")

# Створення таблиці grades, якщо вона не існує
cursor.execute("""
CREATE TABLE IF NOT EXISTS grades (
    student_id INTEGER,
    subject TEXT NOT NULL,
    grade REAL NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
""")

# Заповнення таблиць тестовими даними (тільки якщо вони порожні)
cursor.execute("SELECT COUNT(*) FROM students")
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO students (student_id, name, age) VALUES (?, ?, ?)", [
        (1, 'Андрій', 19),
        (2, 'Марія', 21),
        (3, 'Іван', 18),
        (4, 'Олена', 20),
        (5, 'Петро', 17)
    ])
    cursor.executemany("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)", [
        (1, 'Математика', 85),
        (1, 'Фізика', 78),
        (2, 'Математика', 92),
        (3, 'Математика', 88),
        (3, 'Фізика', 81),
        (4, 'Фізика', 79),
        (5, 'Математика', 95),
        (5, 'Фізика', 87)
    ])
    print("Таблиці заповнено тестовими даними.")

# Виконання SQL-запиту для отримання середнього бала по предметах для студентів до 20 років
query = """
SELECT g.subject, AVG(g.grade) AS average_grade
FROM grades g
JOIN students s ON g.student_id = s.student_id
WHERE s.age < 20
GROUP BY g.subject;
"""

cursor.execute(query)
results = cursor.fetchall()

# Вивід SQL-запиту
print("\nSQL-запит:")
print(query)

# Вивід результатів
print("\nРезультати:")
if results:
    for subject, avg_grade in results:
        print(f"{subject}: {avg_grade:.2f}")
else:
    print("Немає даних для студентів молодше 20 років.")

# Закриття підключення
conn.commit()
conn.close()
print("\nЗ'єднання з базою даних закрито.")
