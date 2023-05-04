import psycopg2
from config import DATABASE_URL

print("DATABASE: ", DATABASE_URL)

CONNECTIONS = 0


def create_connection():
    global CONNECTIONS
    if CONNECTIONS > 10:
        return -1, -1
    CONNECTIONS += 1
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    return conn, cursor


def delete_connection(conn, cursor):
    global CONNECTIONS
    CONNECTIONS -= 1
    cursor.close()
    conn.close()


def get_users() -> list:
    conn, cursor = create_connection()
    cursor.execute("SELECT ids FROM Users")
    res = cursor.fetchone()[0].split(',')
    delete_connection(conn, cursor)
    try:
        res = list(map(int, res))
    except:
        return []
    return res


def add_user(id):
    users = get_users()
    users.append(id)
    res = "".join([str(e) + ',' for e in users]).rstrip(',')
    conn, cursor = create_connection()
    cursor.execute("UPDATE Users SET ids='%s'" % res)
    conn.commit()
    delete_connection(conn, cursor)
