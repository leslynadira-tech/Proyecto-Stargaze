import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        self.connection = pymysql.connect(
            host='altaria.proxy.rlwy.net',
            user='root',
            password='gxbKiKMmtvTInKuCtDUCFDPoWEwuEeML',
            db=db,
            port=50700,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("Error de base de datos:", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)