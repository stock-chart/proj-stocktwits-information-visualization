# !/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import json
import random

class DatabaseQuery:
    def __init__(self):
        try:
            self.conn = MySQLdb.connect(host='localhost', user='root', passwd='root',
                                    db='StockTwits', port=8889,
                                    unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock')
            self.cur = self.conn.cursor()
            print 'Connect to database successfully.'
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            print "Program is halted."
            exit()

    def close_db(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()

    def get_top_symbol_list(self, number):
        self.cur.execute("SELECT symbol_id, symbol, count FROM symbol ORDER BY count DESC LIMIT %d;" % number)
        rows = self.cur.fetchall()
        counter = 0;
        symbol_list = []
        for (symbol_id, symbol, count) in rows:
            counter += 1
            print counter, symbol_id, symbol
            item = {"id":symbol_id, "title":symbol, "count":count}
            symbol_list.append(item)

        return json.dumps({"top_list":symbol_list})

    def get_top_symbol_detail(self, number):
        self.cur.execute("SELECT symbol_id FROM symbol ORDER BY count DESC LIMIT %d" % number)
        symbol_list = self.cur.fetchall()
        print symbol_list
        print '-------'
        for symbol_id in symbol_list:
            self.cur.execute("SELECT body, sentiment  FROM message WHERE symbol_id=%d" % symbol_id[0])
            row = self.cur.fetchall()
            for (body, sentiment) in row:
                print symbol_id[0], body, sentiment

    def get_combined_string(self):
        self.cur.execute("SELECT DISTINCT body FROM message")
        rows = self.cur.fetchall()
        result = ""
        for msg in rows:
            result += msg[0] + '\n'
        return result

    def total_volume_of_ideas(self, symbol_id):
        self.cur.execute("SELECT count FROM symbol WHERE symbol_id=%d;" % symbol_id)
        result = self.cur.fetchone()
        return result[0]

    def get_json_test(self):
        json_obj = {}
        json_obj.update({"abc":"def"})
        json_obj.update({"abcd":"defd"})
        return json.dumps(json_obj)

    def get_treemap_json(self):
        self.cur.execute("SELECT DISTINCT sector FROM symbol;")
        sector_list = self.cur.fetchall()

        children_list = []
        for each_sector in sector_list:
            sector = each_sector[0]
            self.cur.execute("SELECT title, count, bull FROM symbol WHERE sector='%s'" % sector)
            symbol_list = self.cur.fetchall()
            sector_children = []
            for (title, count, bull) in symbol_list:
                symbol_item = {"title:": title, "count:": count, "sentiment": bull}
                sector_children.append(symbol_item)
            sector_json_obj = {"name":sector,"children":sector_children}
            children_list.append(sector_json_obj)

        json_obj = {"name": "treemap", "children": children_list}
        return json.dumps(json_obj)

    def get_latest_message(self, number):
        self.cur.execute("SELECT DISTINCT message_id FROM message ORDER BY created_at DESC LIMIT %d;" % number)
        msg_id_list = self.cur.fetchall()
        json_list = []
        for message_id in msg_id_list:

            #make up a sentiment
            pseudo_sentiment = "bull"
            if (random.getrandbits(1) == 0):
                pseudo_sentiment = "bull"
            else:
                pseudo_sentiment = "bear"

            self.cur.execute("SELECT body, user_id, created_at, sentiment FROM message WHERE message_id=%d;" % message_id[0])
            message_item = self.cur.fetchone()

            # query username
            self.cur.execute("SELECT username FROM user WHERE user_id=%d" % message_item[1])
            user_info = self.cur.fetchone()

            item = {"message_id":message_id[0], "username":user_info[0], "body":message_item[0], "created_at":str(message_item[2]), "sentiment":pseudo_sentiment}
            json_list.append(item)
        return json.dumps(json_list)

if __name__ == "__main__":
    dq = DatabaseQuery()
    # get_top_symbol_detail()
    # ret = dq.get_combined_string()
    res = dq.get_latest_message(50)
    output = open('latest_50_messages.json', 'w')
    output.write(res)
    output.close
    dq.close_db()
