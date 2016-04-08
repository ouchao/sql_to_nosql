#!/usr/bin/python
#coding=utf-8
# -*- coding: utf-8 -*- 
import sys 
#reload(sys) 
#Python2.5 初始化后会删除sys.setdefaultencoding这个方法，我们需要重新载入 
#sys.setdefaultencoding('utf-8') 

import MySQLdb.cursors
import MySQLdb
import json
import re

from decimal import Decimal

from pprint import pprint
import pymongo
import random
import time

def list_to_dict(list,data=''):
    if len(list)==1 :
        t=list.pop()
        return {t:data}
    else:
        t=list.pop()
        return {t:list_to_dict(list,data)}

class mysql_crud():

    def __init__(self):
        self.conn= MySQLdb.connect(
                host    ='192.168.1.51',
                port    = 3306,
                user    ='root',
                passwd  ='rootroot',
                db      ='b2bvip_out',
                use_unicode = True,
                charset ='utf8',
                cursorclass = MySQLdb.cursors.DictCursor,
                )
        self.prefix     = 'b2bvip_'
        self.suffix     = '_sum'
        self.mysql_db   = self.conn.cursor()

    def get_crud(self):
        return self

    def execute(self,sql):
        data=self.mysql_db.execute(sql)
        return self.mysql_db.fetchmany(data)

    def get_fields(self):
        fields = self.mysql_db.execute("SHOW COLUMNS FROM b2bvip_member_sum")
        for field in cur.fetchmany(member_fields):
            print field

    def row_to_json(self,kwdata):
        datas = self.execute("select * from %s limit 1000; "%(kwdata['from_primary_table']))

        #from_table  = re.sub(self.prefix,'',from_table)
        #index_field = re.sub(self.suffix,'',from_table)

        key=kwdata['index_field'].split('.')
        index_field=list_to_dict(key[::-1])

        list=[]
        for row in datas:
            #pid=row.pop(from_primary_field)
            index_field=list_to_dict(key[::-1],row)
            pid=row[kwdata['from_primary_field']]
            list.append(dict({kwdata['to_primary_field']:pid},**index_field))
        return list

    def __del__(self):
        self.mysql_db.close()
        self.conn.commit()
        self.conn.close()

class MyDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


class mongo_crud():
    def __init__(self):
        self.mongo_conn  = pymongo.MongoClient("mongodb://192.168.1.62:28881" )
        self.mongo_db    = self.mongo_conn.qilong_logs

        #用户认证
        self.mongo_db.authenticate("qilong","qilong")

        print self.mongo_db.profiling_info
        print self.mongo_db.name

    def get_crud(self,collection):
        self.mongo_collection=eval("self.mongo_db.%s"%(collection))
        return self.mongo_collection


    #打印所有数据
    def show_table(self,table,fields):
        data2 = eval("self.mongo_db.%s.find({},%s)"%(table,fields))
        for i in data2:
            print i['pid']

    def __del__(self):
        self.mongo_conn.close();

class mysql_to_mongodb_conv():

    def __init__(self):
        self.mysql_ins=mysql_crud()
        self.mongo_ins=mongo_crud()

    def primary_table_conv(self,kwdata):
        mysql=self.mysql_ins.get_crud()
        mongo=self.mongo_ins.get_crud(kwdata['to_collection'])

        #data=mongo.find({},{kwdata['index_field']:{'$exists': True }})
        #if not data :
        #    mongo.update({},{'$set':{kwdata['index_field']:[]}},upsert=True,multi=True)
        #    print({'$set':{kwdata['index_field']:[]}})

        data = self.mysql_ins.row_to_json(kwdata)
        for row in data:
            json_row=json.dumps(row,cls=MyDataEncoder)
            mongo.update({'pid':row['pid']},{'$set':eval(json_row)},upsert=True)

    def nosql_join_sql(self,kwdata):
        mysql=self.mysql_ins.get_crud()
        mongo=self.mongo_ins.get_crud(kwdata['nosql_collection'])

        mysql.execute('drop table if exists tmp;')
        mysql.execute('create table tmp(`%s` bigint(20)  NOT NULL) ENGINE=InnoDB;'%(kwdata['nosql_join_field']))

        tmp_tab='insert into tmp VALUES '
        joinid=mongo.find({},{kwdata['nosql_join_field']:True})
        for i in joinid:
            tmp_tab+='(%s),'%(i[kwdata['nosql_join_field']])
        sql=re.sub(',$',';',tmp_tab)
        mysql.execute(sql)

        '''
        data=mongo.find({},{kwdata['index_field']:{'$exists': True }})
        if not data :
            mongo.update({},{'$set':{kwdata['index_field']:[]}},upsert=True,multi=True)
            print({'$set':{kwdata['index_field']:[]}})
        '''

        #key=kwdata['index_field'].split('.')

        rows=mysql.execute('select a.* from %s as a join tmp as b on a.%s = b.%s '%(kwdata['sql_table'],kwdata['sql_join_field'],kwdata['nosql_join_field']))
        for row in rows:
            index_field=list_to_dict(key[::-1],row)
            #json_row=json.dumps({'$set':kwdata['index_field']:row},cls=MyDataEncoder,ensure_ascii=False,indent=4)
            json_row=json.dumps({'$set':{kwdata['index_field']:row}},cls=MyDataEncoder,ensure_ascii=False,indent=4)
            mongo.update({kwdata['nosql_join_field']:row[kwdata['sql_join_field']]},eval(json_row),upsert=True)
            #print        {kwdata['nosql_join_field']:row[kwdata['sql_join_field']]},eval(json_row)

ee=mysql_to_mongodb_conv()
pconf={'from_primary_table':'b2bvip_member_sum','from_primary_field':'userid','to_collection':'test','to_primary_field':'pid','index_field':'member.this'}
ee.primary_table_conv(pconf)

confs=[
        {'nosql_collection':'test','nosql_join_field':'pid','sql_table':'b2bvip_member_setting_sum'  ,'sql_join_field':'userid','index_field':'member.setting'  },
        {'nosql_collection':'test','nosql_join_field':'pid','sql_table':'b2bvip_member_savetable_sum','sql_join_field':'userid','index_field':'member.savetable'},
        {'nosql_collection':'test','nosql_join_field':'pid','sql_table':'b2bvip_member_order_sum'    ,'sql_join_field':'userid','index_field':'member.order'    },
        {'nosql_collection':'test','nosql_join_field':'pid','sql_table':'b2bvip_member_credit_sum'   ,'sql_join_field':'userid','index_field':'member.credit'   },
        {'nosql_collection':'test','nosql_join_field':'pid','sql_table':'b2bvip_member_contact_sum'  ,'sql_join_field':'userid','index_field':'member.contact'  },
        {'nosql_collection':'test','nosql_join_field':'pid','sql_table':'b2bvip_member_collect_sum'  ,'sql_join_field':'userid','index_field':'member.collect'  },

        {'nosql_collection':'test','nosql_join_field':'pid','sql_table':'b2bvip_company_sum'         ,'sql_join_field':'userid','index_field':'company.this'    },
        {'nosql_collection':'test','nosql_join_field':'pid','sql_table':'b2bvip_company_setting_sum' ,'sql_join_field':'userid','index_field':'company.setting' },
    ]

for c in confs:
    ee.nosql_join_sql(c)
