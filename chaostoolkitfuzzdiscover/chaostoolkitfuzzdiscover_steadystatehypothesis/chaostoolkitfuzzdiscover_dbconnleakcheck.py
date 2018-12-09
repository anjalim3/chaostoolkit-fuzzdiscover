import pymysql
from filenames import mysql_conn_pool_status, probe_file_destination
import os
import sys

def __check_mysqldb_connection_leak(__stage, __hostname, __user, __password):
    if not os.path.exists(probe_file_destination):
        os.makedirs(probe_file_destination)
    __max_connections = None
    __current_connections = None
    connection = pymysql.connect(host=__hostname,
                                 user=__user,
                                 password=__password,
                                 db='sys',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            __sql = "SHOW VARIABLES LIKE 'max_connections'"
            cursor.execute(__sql)
            result = cursor.fetchone()
            __max_connections = int(result['Value'])
        with connection.cursor() as cursor:
            __sql = "select count(*) as current_conn_count from processlist"
            cursor.execute(__sql)
            result = cursor.fetchone()
            __current_connections = result['current_conn_count']
    finally:
        connection.close()
    with open(mysql_conn_pool_status, 'a') as __mysql_status_file:
        if __max_connections is None or __current_connections is None:
            __mysql_status_file.write("[WARNING]: DB Connection failed")
        else:
            if "final" in __stage:
                __mysql_status_file.write("\n")
            __mysql_status_file.write("["+str(__stage)+"][LOG] MaxConnections: "+str(__max_connections)+ " CurrentConnections: "+str(__current_connections))

if len(sys.argv) == 4:
    __password = ''
elif len(sys.argv) == 5:
    __password = sys.argv[4]
__check_mysqldb_connection_leak(sys.argv[1], sys.argv[2], sys.argv[3], __password)
