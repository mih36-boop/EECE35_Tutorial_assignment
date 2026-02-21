# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 13:40:28 2026

@author: User
"""

import sqlite3


conn = sqlite3.connect(':memory:')


conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()


def print_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"\nTable: {table_name}")
    print(" | ".join(columns))
    print("-" * 30)

    for row in rows:
        print(" | ".join(str(value) for value in row))
        
        
cursor.execute("""
CREATE TABLE student (
    student_id INT PRIMARY KEY,
    name TEXT NOT NULL,
    age INT
)
""")
student = [
    (1, 'Alice', 20),
    (2, 'Bob', 22),
    (3, 'Charlie', 21)
]
cursor.executemany("INSERT INTO student VALUES (?, ?, ?)", student)
conn.commit()

print_table(cursor, "student")


cursor.execute("""
CREATE TABLE registered_courses (
    student_id INT, course_id INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
   
)
""")
registered_courses = [
    (1, 101),
    (1, 102),
    (2, 101),
    (3, 103)
]

cursor.executemany("INSERT INTO registered_courses VALUES (?, ?)", registered_courses)
conn.commit()
print_table(cursor, "registered_courses")


cursor.execute("""
CREATE TABLE grades (
    student_id INT , course_id INT, grade REAL,
    PRIMARY KEY(student_id,course_id),
    FOREIGN KEY (student_id,course_id)
    REFERENCES registered_courses(student_id,course_id)
)
""")
grades = [
    (1, 101, 85),
    (1, 102, 92),
    (2, 101, 78),
    (3, 103, 88)
]

cursor.executemany("INSERT INTO grades VALUES (?, ?, ?)", grades)
conn.commit()
print_table(cursor, "grades")

cursor.execute("""
SELECT student_id,  
AVG(grade) AS avg_grade FROM grades GROUP BY student_id 

               """)
               
rows = cursor.fetchall()
print(rows)

cursor.execute(""" 
SELECT student_id,
MAX(grade) AS max_grade FROM grades GROUP BY student_id 


""")            
rows = cursor.fetchall()
print(rows)





























