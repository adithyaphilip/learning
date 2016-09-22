import sqlite3
db = sqlite3.connect(":memory:")
db.execute("Create table person (name text, age int, areaofinterest text, occupation)")
l = [("Adi Sharma", 21, "Music", "Gangstah"), ("Badi babu", 20, "Sports", "SupahGangstah"), ("Lol Pop", 16, "Hmm", "shazzle"), ("P P", 1, "Music", "not")]
db.executemany("INSERT INTO person values (?, ?, ?, ?)", l)
for i in db.execute("SELECT * from person where name like '% Sharma'"):
    print(i)
for i in db.execute("SELECT areaofinterest from person group by areaofinterest order by count(*) DESC LIMIT 1"):
    print(i)
