import sqlite3

connection = sqlite3.connect('Users.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Users
               (User_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
               First_Name NVARCHAR(20), 
               Last_Name NVARCHAR(20),
               Email TEXT)''')


users = [("Usain", "Bolt", "usain.bolt@yahoo.com"),
         ("Karl", "Sagen", "karl.sagen@iobm.pk"),
         ("Mooli", "Gandalf", "mooli@yahoo.com"),
         ("Fake Boy", "Zombie", "fakeboyzombie@gmail.com"),
         ("Samsunta", "Pantaw", "samsuntapantaw@gmail.com")]

cursor.executemany('INSERT INTO Users VALUES (?,?,?)', users)

cursor.execute("SELECT Email FROM Users")

print(cursor.fetchall())

connection.commit()
connection.close()
