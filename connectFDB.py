import fdb
import pandas as pd
from datetime import date


def DataFromTxt(path):

    file = open(path, 'r')
    data = file.read()
    file.close()

    return data


def GetDataFromFDB(begin, end, sp):
    ''' begin, end mast be date object '''

    path = './Resources/Querrys/'

    path = path + sp + '.txt'
    cd = DataFromTxt('./Resources/ConnectionStrings/ConnectionFDB.txt')
    cd = cd.split(',')

    querry = DataFromTxt(path)

    Dane = pd.read_sql(querry, fdb.connect(
        dsn=cd[0], user=cd[1], password=cd[2]), params=[begin, end])

    return Dane


def TableGenerator(start, stop, sp):
    ''' start stop mast be str object and dd.mm.yyyy format'''
    path = './Resources/Querrys/'

    path = path + sp + '.txt'

    cd = DataFromTxt('./Resources/ConnectionStrings/ConnectionFDB.txt')
    querry = DataFromTxt(path)

    cd = cd.split(',')

    #########################################################################

    con = fdb.connect(dsn=cd[0], user=cd[1], password=cd[2])

    cur = con.cursor()

    cur.execute(querry, (start, stop))

    ##########################################################################

    Table = list()

    for i in cur.fetchall():
        Table.append(i)

    con.close()

    return Table


# start = date(2020, 10, 29)
# sp = 'ProductionReport'

# df = GetDataFromFDB(start, start, sp)

# df.to_excel('ProductionReport.xlsx')
