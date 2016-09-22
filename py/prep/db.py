import sqlite3
db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE employee (id int primary key, name text, age int, salary int, deptid integer references dept(id))")
db.execute("CREATE TABLE dept (id int primary key, name text)")
db.execute("INSERT INTO dept values(1, 'CS')")
db.execute("INSERT INTO dept values(2, 'BT')")
db.execute("INSERT INTO employee VALUES (1,'Adi', 21, 5000000, 1)")
db.execute("INSERT INTO employee VALUES (2,'Adi2', 21, 3000000, 1)")
db.execute("INSERT INTO employee VALUES (3,'Adi3', 21, 4000000, 2)")
#db.execute("INSERT INTO employee VALUES (4,'Adi4', 21, 1000000, 2)")

for i in db.execute("SELECT dept.NAME, MAX(salary)  from employee JOIN dept where employee.deptid == dept.id"):
    print(i)
db.close()
