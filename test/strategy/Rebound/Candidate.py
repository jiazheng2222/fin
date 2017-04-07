# -*- coding: utf-8 -*-
# By jiazheng2222
# 7 Apr 2017

import tushare as ts
from datetime import date, datetime
import MySQLdb

from DBConfig import *

def geneCandidate(dbConn):

    dbCur = dbConn.cursor()
    dbCur.execute('SET NAMES utf8;')
    dbCur.execute('SET CHARACTER SET utf8;')
    dbCur.execute('SET character_set_connection=utf8;')

    # Load data from tushare
    todayData = ts.get_today_all()
    # Initialise variable
    dateToday = date.today().strftime('%Y-%m-%d')

    for id, dataItem in todayData.iterrows():
        contractCode, contractName, changePercent, currentPrice, openPrice = dataItem[:5]
        lastPrice = dataItem[7]
        volume = dataItem[8]
        if volume == 0:
            continue

        if abs(lastPrice) > 0.0001:
            dailyChange = (currentPrice - lastPrice )/lastPrice * 100
        else:
            dailyChange = 0.0
        if abs(dailyChange - changePercent) > 0.1:
            print "Error Data or Market is still running! {0}".format(contractCode)
            break

        # Check daily change
        if changePercent < -4.0:
            # Write to DB
            # Sample:
            #('600036', u'招商银行', '3.21', '5.68', '19.01', '18.22', '2017-04-06', '1491478722')
            timeStamp = datetime.now().strftime("%s")
            print timeStamp

            print contractCode, contractName, currentPrice-lastPrice,dailyChange,lastPrice

            dbCur.execute("INSERT INTO `fin`.`candidate` \
            (`contractid`, `contractname`, `dailychangenum`, \
            `dailychangeratio`, `lastprice`, `closeprice`, \
            `checkdate`, `createtime`) VALUES \
            (%s, %s, %s, %s, %s, %s, %s, %s);",
            (contractCode, contractName, currentPrice-lastPrice,
            dailyChange,lastPrice, currentPrice, dateToday, timeStamp))
            dbConn.commit()

def candidate():
    # create DB connection
    dbConn = MySQLdb.connect(user=DB_USER,
                            passwd=DB_PASSWD,
                            host=DB_HOST,
                            db=DB_DB)
    dbConn.set_character_set('utf8')
    geneCandidate(dbConn)

    # close DB
    dbConn.close()


