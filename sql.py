import sqlite3

conn=sqlite3.connect("mydb2.db")
cursor=conn.cursor()

cursor.execute("""create table if not exists posts(
                id integer not null primary key,
                content text
                                )

               """)

data=[("This is the 1st post",),("This is the 2nd post",),("This is the 3rd post",),]

cursor.executemany("Insert into posts (content) values (?)",data)
conn.commit()
conn.close()