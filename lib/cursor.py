try:
    import MySQLdb
except DeprecationWarning:
    pass

def get_cursor():
    conn = MySQLdb.connect( host = "localhost",
                            user = "root",
                            passwd = "nineteen81",
                            db = "pychee" )

    return conn.cursor()

def execute(to_exec):
    cursor = get_cursor()
    cursor.execute(to_exec)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def insert(table, **kwargs):
    query_str = "INSERT INTO %s (%s) VALUES (%s)" % \
        (table, 
         ",".join(kwargs.keys()),
         ",".join( [ "'%s'" % v for v in kwargs.values() ] )
         )
    execute(query_str)
    
def load(table, col_list):
    query_str = "SELECT %s FROM %s" % \
        (",".join(col_list),
         table)
    
    return execute(query_str)
