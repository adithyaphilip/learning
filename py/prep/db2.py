import sqlite3
import re
from datetime import date
import datetime
db = sqlite3.connect(":memory:", isolation_level=None, detect_types=sqlite3.PARSE_DECLTYPES)
db.execute("Create table bday (name text, dob date)")
l = []
for i in range(4):
    name = input()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", input())
    d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    l.append((name, m.group()))

db.executemany("INSERT INTO bday VALUES(?, ?)", l)

for i in db.execute("SELECT name, dob from bday"):
    print(i)

for i in db.execute("SELECT * from bday"):
    print(i[0],(date.today() - i[1]).total_seconds()//datetime.timedelta(days=365).total_seconds())
