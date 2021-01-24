from django.db import connection

def check_tables(table_name):
    with connection.cursor() as cursor:
        stmt = "SHOW TABLES LIKE '%s' "% ('%'+str(table_name)+'%')
        cursor.execute(stmt)
        result = cursor.fetchone()  
    return result