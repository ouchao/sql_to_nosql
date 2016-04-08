# sql_to_nosql
这是一个将将关系型数据库转换为非关系型数据库的程序，本程序需要定义转换规则，转换规则可以理解为,将关系型数据库的表与表的关系描叙出来多条json数据。
本程序将一个sql类型的数据库中的多张关联表组合为nosql型数据库的一个collection。sql数据的一条由多张表联合后组成的一条数据将转为nosql数据的一条数据。
具体结构如图：

{
  "_id" : ObjectId("5707271b90e0f85c9535e60e"),
  "company" : {
    "this" : {
      "sellareaid" : "",
      "vipyear" : 44,
      "certification" : "",
      "isactivate" : 1,
      "annualrevenue" : 0,
      "baseinvestmentunit" : "",
      "postcode" : "518031",
      "size" : 0,
      "initialfeeunit" : "",
      "monthlyoutput" : 0.0,
      "agentlevel" : "",
      "homepage" : "",
      "buy" : "",
      "requirearea" : "",
      "collecttotal" : 0,
      "addtime" : 0,
      "brand" : "",
      "isvip" : 0,
      "plantarea" : 0.0,
      "clients" : "",
      "userid" : 52138,
      "starttime" : 0,
      "monthlyoutputunit" : "",
      "distribution" : "",
      "agent" : "",
      "sell" : "",
      "regcityid" : 233,
      "areaid" : 233,
      "lowestsalesyearunit" : "",
      "capital" : 50.0,
      "company" : "深圳市豫林实业有限公司",
      "map" : "",
      "business" : "456",
      "baseinvestment" : 0.0,
      "update" : 0,
      "qualitycertification" : "",
      "qaqc" : 0,
      "regunit" : "RMB",
      "address" : "广东深圳深南中路统建楼",
      "lowestsalesyear" : 0.0,
      "regyear" : "0",
      "endtime" : 0,
      "catids" : "40019",
      "typeid" : 0,
      "hits" : 30,
      "plantimg" : "",
      "initialfee" : 0.0,
      "modeids" : "1",
      "annualexportamount" : 0
    }
  },
  "member" : {
    "contact" : {
      "fax" : "755-83625911",
      "ali" : "",
      "company" : "深圳市豫林实业有限公司",
      "telephone" : "755-83635806",
      "truename" : "中原",
      "career" : "其他",
      "qq" : "",
      "mobile" : "",
      "gender" : 1,
      "userid" : 52138,
      "msn" : "",
      "department" : "其他",
      "mail" : "yyq@suminfo.com"
    },
    "savetable" : {
      "tableids" : "",
      "userid" : 52138,
      "tablemark" : "supply"
    },
    "this" : {
      "username" : "yyqyuani",
      "userid" : 52138,
      "useremail" : "yyq@suminfo.com",
      "password" : "f661230fc089e7f1",
      "money" : 0.0,
      "integrity_mark" : 0,
      "regip" : "",
      "loginip" : "",
      "sms" : 0,
      "usermobile" : "",
      "regtime" : 0,
      "update" : 0,
      "payword" : "f661230fc089e7f1",
      "lastlogintime" : 0,
      "locking" : 0.0,
      "groupid" : 4,
      "logintimes" : 1
    }
  },
  "pid" : 52138
}

