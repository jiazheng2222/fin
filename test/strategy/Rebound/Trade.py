# -*- coding: utf-8 -*-
# By jiazheng2222
# 10 Apr 2017

import tushare as ts
from datetime import date, datetime
import MySQLdb

from DBConfig import *

def geneTrade(dbConn):

    # nominate list
    nomiIdList = []
    nomiList = []
    buypriceList = []
    buyflagList = []

    dbCur = dbConn.cursor()
    dbCur.execute('SET NAMES utf8;')
    dbCur.execute('SET CHARACTER SET utf8;')
    dbCur.execute('SET character_set_connection=utf8;')

    dbCur.execute("select * from fin.nominate ")
    for nomiItem in dbCur.fetchall():
        nomiIdList.append(nomiItem[0])
        nomiList.append(nomiItem[1])
        buyflagList.append(nomiItem[13])
        buypriceList.append(nomiItem[8])

    # Load data from tushare
    todayData = ts.get_today_all()

    # Initialise variable
    dateToday = date.today().strftime('%Y-%m-%d')

    for id, dataItem in todayData.iterrows():
        contractCode, contractName, changePercent, currentPrice, openPrice = dataItem[:5]

        # only check the nominate
        if contractCode not in nomiList:
            continue
        loc = nomiList.index(contractCode)

        lastPrice = dataItem[7]
        volume = dataItem[8]

        # this one may be suspended
        if volume == 0:
            continue

        print nomiIdList[loc], dateToday, buypriceList[loc]
        # start to buy
        if buyflagList[loc] == 'N':
            buyprice = currentPrice
            dbCur.execute ("UPDATE fin.nominate SET buyprice=%s , buydate = %s , buyflag = 'Y'\
            WHERE id=%s", (buyprice, dateToday, nomiIdList[loc]))
        # check the current price & update
        else:
            curprice = currentPrice
            chagratio = (currentPrice - float(buypriceList[loc]))/float(buypriceList[loc])
            dbCur.execute ("UPDATE fin.nominate SET curprice=%s , curdate = %s, chagratio = %s \
            WHERE id=%s", (curprice, dateToday, chagratio, nomiIdList[loc]))

        dbConn.commit()

def trade():
    # create DB connection
    dbConn = MySQLdb.connect(user=DB_USER,
                            passwd=DB_PASSWD,
                            host=DB_HOST,
                            db=DB_DB)
    dbConn.set_character_set('utf8')
    geneTrade(dbConn)

    # close DB
    dbConn.close()

trade()
