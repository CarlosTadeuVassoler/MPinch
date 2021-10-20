import sqlite3
import hashlib

def commit_close(func):
    def decorator(*args):
        con = sqlite3.connect("base_de_dados.db")
        cur = con.cursor()
        sql = func(*args)
        cur.execute(sql)
        con.commit()
        con.close()
    return decorator

@commit_close
def db_criar(i, j, si, sj, sk, k, q, thki, thkf, tcki, tckf, thski, thskf, tcski, tcskf, fh, fc):
    return """  INSERT INTO dados (i, j, si, sj, sk, k, q, thki, thkf, tcki, tckf, thski, thskf, tcski, tcskf, fh, fc)
                            values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}') """.format(i, j, si, sj, sk, k, q, thki, thkf, tcki, tckf, thski, thskf, tcski, tcskf, fh, fc)


def db_read():
    con = sqlite3.connect("base_de_dados.db")
    cur = con.cursor()
    sql = """ SELECT i, j, si, sj, sk, k, q, thki, thkf, tcki, tckf, thski, thskf, tcski, tcskf, fh, fc FROM dados """
    cur.execute(sql)
    valores = cur.fetchall()
    con.close()
    return valores

@commit_close
def db_delete(i, j, si, sj, sk, k):
    return """ DELETE FROM dados WHERE i = '{}' AND j = '{}' AND si = '{}' AND sj = '{}' AND sk = '{}' AND k = '{}' """.format(i, j, si, sj, sk, k)
