import sqlite3

# Connect to SQLite database (creates 'chatdatabase.db' if it doesn't exist)
connection = sqlite3.connect('chatdatabase.db')

# Creating cursor
cursor = connection.cursor()

#Creating Table
table_info="""
Create table STUDENT(NAME VARCHAR(24),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT);
"""
cursor.execute(table_info)

#insert some records
import sqlite3

# Connect to SQLite database
connection = sqlite3.connect('chatdatabase.db')
cursor = connection.cursor()

# Sample data: 50 records
students = [
    ('Awais', 'Data Science', 'A', 120),
    ('John', 'Machine Learning', 'B', 115),
    ('Emma', 'Computer Vision', 'A', 110),
    ('Liam', 'Cyber Security', 'C', 105),
    ('Olivia', 'Software Engineering', 'B', 98),
    ('Noah', 'AI & Robotics', 'A', 125),
    ('Sophia', 'Big Data', 'C', 102),
    ('Mason', 'Data Science', 'B', 117),
    ('Isabella', 'Cloud Computing', 'A', 130),
    ('James', 'Data Science', 'C', 99),
    ('Lucas', 'Blockchain', 'A', 128),
    ('Mia', 'Cyber Security', 'B', 96),
    ('Benjamin', 'IoT', 'C', 108),
    ('Charlotte', 'AI & Robotics', 'A', 121),
    ('Ethan', 'Machine Learning', 'B', 123),
    ('Amelia', 'Computer Science', 'A', 112),
    ('Alexander', 'Blockchain', 'C', 95),
    ('Harper', 'Software Engineering', 'B', 118),
    ('Daniel', 'Data Science', 'A', 107),
    ('Ella', 'Big Data', 'C', 115),
    ('Matthew', 'Cyber Security', 'B', 104),
    ('Avery', 'AI & Robotics', 'A', 126),
    ('Henry', 'Cloud Computing', 'C', 101),
    ('Scarlett', 'Machine Learning', 'B', 119),
    ('Joseph', 'Blockchain', 'A', 129),
    ('Grace', 'IoT', 'C', 97),
    ('Samuel', 'Computer Vision', 'B', 113),
    ('Chloe', 'Big Data', 'A', 120),
    ('David', 'Software Engineering', 'C', 100),
    ('Lily', 'Data Science', 'B', 122),
    ('Andrew', 'Cloud Computing', 'A', 127),
    ('Aria', 'Machine Learning', 'C', 94),
    ('Christopher', 'AI & Robotics', 'B', 109),
    ('Sofia', 'Cyber Security', 'A', 124),
    ('Jack', 'Computer Vision', 'C', 111),
    ('Ella', 'Software Engineering', 'B', 97),
    ('Ryan', 'Blockchain', 'A', 103),
    ('Zoey', 'Data Science', 'C', 106),
    ('Nathan', 'IoT', 'B', 116),
    ('Madison', 'Machine Learning', 'A', 131),
    ('William', 'Big Data', 'C', 90),
    ('Hannah', 'Cyber Security', 'B', 125),
    ('Logan', 'Computer Science', 'A', 110),
    ('Evelyn', 'AI & Robotics', 'C', 112),
    ('Dylan', 'Cloud Computing', 'B', 127),
    ('Abigail', 'Software Engineering', 'A', 121),
    ('Jayden', 'Machine Learning', 'C', 105),
    ('Aubrey', 'Big Data', 'B', 98),
    ('Gabriel', 'IoT', 'A', 123),
    ('Elizabeth', 'Cyber Security', 'C', 102),
]

# Inserting multiple records at once
cursor.executemany("INSERT INTO STUDENT VALUES (?, ?, ?, ?)", students)


print("50 records inserted successfully!")
data=cursor.execute("SELECT * FROM STUDENT")

for row in data:
    print(row)


# Commit and close the connection
connection.commit()
connection.close()


