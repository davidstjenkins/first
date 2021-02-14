#!/usr/bin/python3

import sqlite3

def ip2num(String):
    L = String.split('.')
    return((16777216 * int(L[0])) + (65536 * int(L[1])) + (256 * int(L[2])) + int(L[3]))

ip_file = open('filename.csv', 'r')

ip_data = []

for line in iter(ip_file):
    line.rstrip()
    line_split = line.split(',')
    if line_split[0].count(':') > 0:
        continue
    line_split[7] = line_split[7].rstrip('\n')
    ip_num0, ip_num1 = ip2num(line_split[0]),  ip2num(line_split[1])
    #ip_num0, ip_num1 = str(ip2num(line_split[0])),  str(ip2num(line_split[1]))
    line_split.append(ip_num0)
    line_split.append(ip_num1)
    tpl = tuple(line_split)
    ip_data.append(tpl)

ip_file.close()

conn = sqlite3.connect("mydatabase.db")

cursor = conn.cursor()

#cursor.execute("""DROP TABLE ip_records""")

cursor.execute("""CREATE TABLE ip_records
                  (ip_start, ip_finish, continent, country, state, city, lat, long, num_start, num_finish)
               """)
cursor.execute("""CREATE UNIQUE INDEX idx_numbers ON ip_records(num_start ASC, num_finish ASC)
               """)

for datum in ip_data:
    if len(datum) != 10:
        continue
    cursor.execute("INSERT INTO ip_records VALUES (?,?,?,?,?,?,?,?,?,?)", datum)   
#cursor.executemany("INSERT INTO ip_records VALUES (?,?,?,?,?,?,?,?,?,?)", ip_data)
conn.commit()
