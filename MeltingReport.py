import pandas as pd
from pandas import DataFrame, Series
import numpy as np
from datetime import datetime
import pyodbc


class GetDataFromXlsx:

    def __init__(self, procedure):
        self.__meltingReport = pd.read_excel(
            './Resources/Tabele.xlsx', procedure)

        self.__meltingReport['Data'] = pd.to_datetime(
            self.__meltingReport['Data']) + pd.to_timedelta(self.__meltingReport['Godzina'], unit='h')

        self.__meltingReport = self.__meltingReport.drop(
            columns=['Godzina', 'Uwagi'])

        self.__meltingReport = self.__ConvertValuesInXlsx(
            self.__meltingReport)

    def __ConvertValuesInXlsx(self, df):
        x = df.shape[0]

        for i in range(x):
            df.iloc[i, 1] = self.__FixXlsxFeedAndLevel(df.iloc[i, 1])
            df.iloc[i, 2] = self.__FixXlsxFeedAndLevel(df.iloc[i, 2])
            df.iloc[i, 5] = self.__FixXlsxFeedAndLevel(df.iloc[i, 5])
            df.iloc[i, 6] = self.__FixXlsxFeedAndLevel(df.iloc[i, 6])

            df.iloc[i, 4] = self.__FixXlsxBatch(df.iloc[i, 4])
            df.iloc[i, 8] = self.__FixXlsxBatch(df.iloc[i, 8])

            df.iloc[i, 3] = np.float(self.__FixXlsxPower(df.iloc[i, 3]))

        return df

    def __FixXlsxBatch(self, value):
        if (type(value) == str):
            return np.NaN
        else:
            return value

    def __FixXlsxFeedAndLevel(self, value):

        if (type(value) != str):
            value = str(value)
            if (len(value) > 3):
                return np.NaN
            else:
                return value
        else:
            return value

    def __FixXlsxPower(self, value):

        if(type(value) == str):

            newValue = ''
            char = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

            for v in value:
                for c in char:
                    if(v == c):
                        newValue = newValue + v

            parsValue = float(newValue)

            if(parsValue > 1000):
                parsValue = parsValue / 10

            return parsValue

        else:
            return value

    def ShowMeltingReport(self, begin, end):

        df = self.__meltingReport[(self.__meltingReport['Data'] >= begin) & (
            self.__meltingReport['Data'] < end)]

        print(df)

        # WGBatches = df.iloc[:, 8].sum()
        # WGPullRate = WGBatches * 471

        # WEBatches = df.iloc[:, 4].sum()

        # print('Baniaki WG:', WGBatches)
        # print('Wydobycie WE', WGPullRate)
        # print('Baniaki WE:', WEBatches)

        # print('Gaz [Nm3/h]:', df.iloc[:, 7].sum())
        # print('Moc [KWh]:', df.iloc[:, 3].sum())


class MeltingReport:

    def __Constring(self):
        path = './Resources/ConnectionStrings/ConnectionMSSQL.txt'
        file = open(path, 'r')
        constring = file.read()
        file.close()

        return constring

    def ShowMeltingReport(self):

        querry = 'select CzasWpisu, ZasypWE, PoziomWE, Moc, BaniakWE, ZasypWG, PoziomWG, Gaz, BaniakWG from RaportTopiarza'

        conn = pyodbc.connect(self.__Constring())
        self.__meltingReport = pd.read_sql(querry, conn)

        print(self.__meltingReport)

    def InsertRowToDB(self, paramList):
        querry = 'insert into RaportTopiarza(CzasWpisu,ZasypWE,PoziomWE,Moc,BaniakWE,ZasypWG,PoziomWG,Gaz,BaniakWG) values(?,?,?,?,?,?,?,?,?)'

        conn = pyodbc.connect(self.__Constring())

        cursor = conn.cursor()

        cursor.execute(querry, paramList[0], paramList[1], paramList[2], paramList[3],
                       paramList[4], paramList[5], paramList[6], paramList[7], paramList[8])
        conn.commit()

        conn.close()


# date = '2020.08.07 13:00'
# zasypWE = None
# poziomWE = None
# moc = None
# baniakWE = None
# zasypWG = None
# poziomWG = None
# gaz = 95
# baniakWG = None

# parametersList = [date, zasypWE, poziomWE, moc,
#                   baniakWE, zasypWG, poziomWG, gaz, baniakWG]

# mr = MeltingReport()
# mr.InsertRowToDB(parametersList)
