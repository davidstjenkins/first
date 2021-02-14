#!/usr/bin/python3

import sqlite3

from os import popen

def ip2num(String):
    L = String.split('.')
    return((16777216 * int(L[0])) + (65536 * int(L[1])) + (256 * int(L[2])) + int(L[3]))

def estab_conns():
    tcp_est = popen("cat out1 | grep ESTAB | awk '{print $5}' | cut -d: -f1 | sort | uniq | sed -e 's/\./,/g' -e 's/^/[/' -e 's/$/]/' | tr '\012' ',' | sed -e 's/^/[/' -e 's/,$/]/'").read()

    M = eval(tcp_est)

    if 0 == len(M):
        print("No current connections.")
        exit(0)

    return(M)

def db_queries(connection_list):
    conn = sqlite3.connect("mydatabase.db")

    cursor = conn.cursor()

    for m in connection_list:
        ip_num = (16777216 * int(m[0])) + (65536 * int(m[1])) + (256 * int(m[2])) + int(m[3])
        print(str(m[0]) + '.' + str(m[1]) + '.' + str(m[2]) + '.' + str(m[3]))
        sql = "SELECT city, state, continent FROM ip_records WHERE num_start <= %d AND num_finish >= %d" % (ip_num, ip_num)
        cursor.execute(sql)
        print(cursor.fetchall())

    conn.close()

def main():
    conns_list = estab_conns()
    db_queries(conns_list)

if __name__ == '__main__':
    main()
