# !/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import json

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
        self.cur.execute("SELECT symbol_id, symbol FROM symbol ORDER BY count DESC LIMIT %d;" % number)
        rows = self.cur.fetchall()
        counter = 0;
        for (symbol_id, symbol) in rows:
            counter += 1
            print counter, symbol_id, symbol

    def get_combined_string(self):
        self.cur.execute("SELECT body FROM message")
        rows = self.cur.fetchall()
        result = ""
        for msg in rows:
            result += ' ' + msg[0]
        return result

    def total_volume_of_ideas(self, symbol_id):
        self.cur.execute("SELECT count FROM symbol WHERE symbol_id=%d;" % symbol_id)
        result = self.cur.fetchone()
        return result[0]

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
            self.cur.execute("SELECT title, count FROM symbol WHERE sector='%s'" % sector)
            symbol_list = self.cur.fetchall()
            sector_children = []
            for (title, count) in symbol_list:
                symbol_item = {"sector:": sector, "title:": title, "count:": count}
                sector_children.append(symbol_item)
            sector_json_obj = {"name":sector,"children":sector_children}
            children_list.append(sector_json_obj)

        json_obj = {"name": "treemap", "children": children_list}
        return json.dumps(json_obj)

if __name__ == "__main__":
    dq = DatabaseQuery()
    dq.close_db()
