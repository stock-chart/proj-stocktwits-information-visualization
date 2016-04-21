# !/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import json
import random

input_path = '/Users/YuandaLi/Programs/ST_Data_Parser'
input_file_name = 'part_data_5K.json'

def parse_json(cur):
    cnt = 0
    for line in open(input_path + '/' + input_file_name):
        message = json.loads(line)
        # Parse message
        if 'symbols' in message:
            for symbol in message['symbols']:
                cur.execute("INSERT INTO message(message_id, body, created_at, user_id, symbol_id, sentiment) VALUES (%d, '%s', '%s', %d, %d, '%s');" % (message['id'], message['body'], message['created_at'], message['user']['id'], symbol['id'], message['entities']['sentiment']))
                # Insert symbol if not exists
                if (cur.execute("SELECT * FROM symbol WHERE symbol_id=%d" % symbol['id']) == 0):
                    cur.execute("INSERT INTO symbol(symbol_id, symbol, title, exchange, sector, industry, trending) VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s')" % (symbol['id'], symbol['symbol'], symbol['title'], symbol['exchange'], symbol['sector'], symbol['industry'], symbol['trending']))
                else:
                    cur.execute("UPDATE symbol SET symbol.count=symbol.count+1 WHERE symbol_id=%d;" % symbol['id'])
        else:
            cur.execute("INSERT INTO message(message_id, body, created_at, user_id, sentiment) VALUES (%d, '%s', '%s', %d, '%s');" % (message['id'], message['body'], message['created_at'], message['user']['id'], message['entities']['sentiment']))

        # Create user entry
        user_count = cur.execute("SELECT * FROM user WHERE user_id=%d;" % message['user']['id'])
        if (user_count == 0):
            cur.execute("INSERT INTO user (user_id, username, name) VALUES (%d, '%s', '%s')" % (message['user']['id'], message['user']['username'], message['user']['name']))
        else:
            pass

        cnt += 1
        print cnt, 'Message', message['id'], 'created.'

def generate_pseudo_sentiment_value(cur):
    cur.execute("SELECT symbol_id FROM symbol")
    symbol_list = cur.fetchall()
    for symbol in symbol_list:
        symbol_id = symbol[0]
        # print symbol_id
        cur.execute("UPDATE symbol SET symbol.bull=%d WHERE symbol_id=%d" % (random.randint(30, 95), symbol_id))

def create_database():
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='root',
                                db='StockTwits', port=8889,
                                unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock')
        cur = conn.cursor()
        # Create table if not exists
        cur.execute("DROP TABLE IF EXISTS message;")
        cur.execute("DROP TABLE IF EXISTS user;")
        cur.execute("DROP TABLE IF EXISTS symbol;")
        cur.execute("CREATE TABLE IF NOT EXISTS message(id INT PRIMARY KEY AUTO_INCREMENT, message_id INT, body TEXT, created_at DATETIME, user_id INT, symbol_id INT, sentiment VARCHAR(10)) CHARACTER SET utf8 COLLATE utf8_bin;")
        cur.execute("CREATE TABLE IF NOT EXISTS user(id INT PRIMARY KEY AUTO_INCREMENT, user_id INT, username VARCHAR(50), name VARCHAR(50), classification VARCHAR(15));")
        cur.execute("CREATE TABLE IF NOT EXISTS symbol(id INT PRIMARY KEY AUTO_INCREMENT, symbol_id INT, symbol VARCHAR(25), title VARCHAR(50), exchange VARCHAR(10), sector VARCHAR(50), industry VARCHAR(50), trending VARCHAR(10), count INT DEFAULT 1, bull INT DEFAULT 0, bear INT DEFAULT 0);")
        print 'Databases created.'

        # Insert entries
        parse_json(cur)
        generate_pseudo_sentiment_value(cur)

        cur.close()
        conn.commit()
        conn.close()
    except MySQLdb.Error, e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
    create_database()
