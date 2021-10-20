import sqlite3

def criar_db():
    con = sqlite3.connect('base_de_dados.db')
    cur = con.cursor()

    sql = """ CREATE TABLE IF NOT EXISTS dados(
    i INTEGER NOT NULL,
    j INTEGER NOT NULL,
    si INTEGER NOT NULL,
    sj INTEGER NOT NULL,
    sk INTEGER NOT NULL,
    k INTEGER NOT NULL,
    q REAL NOT NULL,
    thki REAL NOT NULL,
    thkf REAL NOT NULL,
    tcki REAL NOT NULL,
    tckf REAL NOT NULL,
    thski REAL NOT NULL,
    thskf REAL NOT NULL,
    tcski REAL NOT NULL,
    tcskf REAL NOT NULL,
    fh REAL NOT NULL,
    fc REAL NOT NULL
    ) """

    cur.execute(sql)
    con.commit()
    con.close()
