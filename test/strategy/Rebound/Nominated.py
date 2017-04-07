# -*- coding: utf-8 -*-
# By jiazheng2222
# 7 Apr 2017

import tushare as ts
from datetime import date, datetime
import MySQLdb

from DBConfig import *

def geneNominated(dbConn):

    # candidate list
    candiList = []
    lstChgRtoList = []
    lstDateList = []

    dbCur = dbConn.cursor()
    dbCur.execute('SET NAMES utf8;')
    dbCur.execute('SET CHARACTER SET utf8;')
    dbCur.execute('SET character_set_connection=utf8;')

    dbCur.execute("select * from  fin.candidate where latestflag = 'Y'")
    for candiItem in dbCur.fetchall():
        candiList.append(candiItem[1])
        lstChgRtoList.append(candiItem[4])
        lstDateList.append(candiItem[8])

    # Load data from tushare
    todayData = ts.get_today_all()

    # Initialise variable
    dateToday = date.today().strftime('%Y-%m-%d')

    for id, dataItem in todayData.iterrows():
        contractCode, contractName, changePercent, currentPrice, openPrice = dataItem[:5]

        # only check the candidates
        if contractCode not in candiList:
            continue
        loc = candiList.index(contractCode)

        lastPrice = dataItem[7]
        volume = dataItem[8]

        # this one may be suspended
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
        # the second day
        if changePercent < -3.0:
            # Write to DB : nominated
            # Sample:
            #
            timeStamp = datetime.now().strftime("%s")

            print contractCode, contractName, lstChgRtoList[loc],lstDateList[loc], dailyChange, dateToday, timeStamp

            dbCur.execute("INSERT INTO `fin`.`nominate` \
            (`contractid`, `contractname`, `lastchangeratio`, \
            `lastdate`, `currchangeratio`, `checkdate`, `createtime`) VALUES \
            (%s, %s, %s, %s, %s, %s, %s);",
            (contractCode, contractName, lstChgRtoList[loc],
            lstDateList[loc], dailyChange, dateToday, timeStamp))
            dbConn.commit()

def nominated():
    # create DB connection
    dbConn = MySQLdb.connect(user=DB_USER,
                            passwd=DB_PASSWD,
                            host=DB_HOST,
                            db=DB_DB)
    dbConn.set_character_set('utf8')
    geneNominated(dbConn)

    # close DB
    dbConn.close()

