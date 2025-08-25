import mysql.connector

def get_conn():
    conn = mysql.connector.connect(
        host='localhost', 
        user='root', 
        password='root',
    )
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS candidatesBD')
    cursor.close()
    conn.database = 'candidatesBD'
    return conn