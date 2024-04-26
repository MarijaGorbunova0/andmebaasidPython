
from multiprocessing import connection
from sqlite3 import *
from sqlite3 import Error 
from os import path

def create_connect(path:str):
    connection = None
    try:
        connection = connect(path)
        print("Ühendus loodud")
    except Error as e:
        print(f"Tekkis viga: {e}")
    return connection

def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Tabel on loodud või andmed on sisestatu")      
    except Error as e:
        print(f"Tekkis viga: {e}")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except Error as e:
        print(f"Tekkis viga: {e}")
    return result

def execute_insert_query(connection, data):
    query = "INSERT INTO kasutajad(Eesnimi, Perenimi, Vanus, Lapsed, Juuksed, Pikkus) VALUES(?,?,?,?,?,?)"
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()

def dropTable(connection, table):
    try:
        cursor = connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS{table}")
        connection.commit()
    except Error as e:
        print(f"Tekkis viga: {e}")
create_kasutajate_tabel = """
CREATE TABLE IF NOT EXISTS kasutajad(
Id INTEGER PRIMARY KEY AUTOINCREMENT,
Eesnimi TEXT NOT NULL,
Perenimi TEXT NOT NULL,
Vanus INTEGER NOT NULL,
Lapsed INTEGER NOT NULL,
Juuksed TEXT NOT NULL,
Pikkus INTEGER NOT NULL
)
"""

insert_kasutajad = """
INSERT INTO
kasutajad(Eesnimi, Perenimi, Vanus, Lapsed, Juuksed, Pikkus)
VALUES
('Marija', 'Gorbunova', 16, 0, 'pruunid', 165),
('Nikel', 'Nikelevith', 51, 1, 'valged', 200),
('Roman', 'Sandakov', 25, 9, 'pruunid', 600),
('Jimmy', 'Magil', 40, 0, 'mustad', 180)
"""
posetiteli_salona = """
CREATE TABLE IF NOT EXISTS posetiteli(
Id INTEGER PRIMARY KEY AUTOINCREMENT,
Teenus TEXT NOT NULL,
Hind INTEGER NOT NULL,
Külastaja INTEGER NOT NULL,
FOREIGN KEY (Külastaja) REFERENCES kasutajad(Id)
)
"""

insert_posetiteli = """
INSERT INTO
posetiteli(Teenus, Hind, Külastaja)
VALUES
('juukselõikus', 10, 1),
('värvimine', 90, 3)
"""

valige_kasutajad_posetiteli = """
SELECT kasutajad.Eesnimi, kasutajad.Perenimi, posetiteli.Teenus, posetiteli.Hind
FROM kasutajad
INNER JOIN posetiteli ON kasutajad.Id = posetiteli.Külastaja
"""

filename=path.abspath(__file__)
dbdir=filename.rstrip('andmebaasidPython.py')
dbpath=path.join(dbdir,"data.db")
conn=create_connect(dbpath)

execute_query(conn, create_kasutajate_tabel)
execute_query(conn, insert_kasutajad)
execute_query(conn, posetiteli_salona)
execute_query(conn, insert_posetiteli)

lisage_kasutaja_andmed = (
    input("Eesnimi: "),
    input("Perenimi: "),
    int(input("Vanus: ")),
    int(input("Lapsed: ")),
    input("Juuksed: "),
    int(input("Pikkus: "))
)
execute_insert_query(conn, lisage_kasutaja_andmed)

kasutajad = execute_read_query(conn, "SELECT * FROM kasutajad")
print("Kasutajate tabel:")
for kasutaja in kasutajad:
    print(kasutaja)

kasutajad_posetiteli = execute_read_query(conn, valige_kasutajad_posetiteli)
print("Kasutajad posetiteliga:")
for kasutaja_posetiteli in kasutajad_posetiteli:
    print(kasutaja_posetiteli)
