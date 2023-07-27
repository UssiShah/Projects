import sqlite3

connection = sqlite3.connect('Users.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Users
               (User_ID VARCHAR(20), 
               First_Name NVARCHAR(20), 
               Last_Name NVARCHAR(20),
               Email TEXT)''')


users = [(1, "Usama", "Shahid", "usama.shahd@yahoo.com"),
         (2, "Talha", "Shahid", "talha.siddiqui@iobm.pk"),
         (3, "Aliyaan", "Talha", "aliyaan@yahoo.com"),
         (4, "Fake Boy", "Zombie", "fakeboyzombie@gmail.com"),
         (5, "Samsunta", "Pantaw", "samsuntapantaw@gmail.com")]

cursor.executemany('INSERT INTO Users VALUES (?,?,?,?)', users)

cursor.execute("SELECT Email FROM Users")

print(cursor.fetchall())

connection.commit()
connection.close()