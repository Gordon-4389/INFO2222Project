import sqlite3

conn = sqlite3.connect("user1.db")
curr = conn.cursor()

curr.execute("SELECT * FROM Users")
result = curr.fetchall()
if result != None:
    print(result)
else:
    print("Nothing inside!!!")