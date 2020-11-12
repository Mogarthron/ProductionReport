import pandas as pd
from pandas import DataFrame, ExcelWriter, Series
import numpy as np
from connectFDB import TableGenerator, GetDataFromFDB
import calendar
from calendar import monthrange
import datetime
import matplotlib.pyplot as plt


class GeneralReport:

    def __init__(self, begin, end):

        self.__Data = pd.DataFrame(
            GetDataFromFDB(begin, end, 'ProductionReport'))

        self.columns = ['Data', 'Brygada', 'Warsztat', 'NrKarty', 'Kategoria', 'Forma',
                        'Odbiorca', 'Brutto', 'BrakiMasyMl', 'BRAKI_MASY_BZB', 'BrakiFormowania',
                        'BrakiOdprezania', 'BrakiOpekiwania', 'Stluczka', 'BrakiInne', 'BrakiRazem',
                        'WAGA_BRUTTO', 'WAGA_NETTO', 'CzasPracy', 'WYKONANIE']

    def ProductionReport(self):

        # cols = ['Data', 'Brygada', 'Warsztat', 'NrKarty', 'Kategoria', 'Forma',
        #         'Odbiorca', 'Brutto', 'BrakiRazem', 'WAGA_BRUTTO', 'WAGA_NETTO', 'CzasPracy']

        # print(self.__Data[cols].to_string(index=False))
        return self.__Data[self.columns]

    def GeneralDailyReport(self):

        self.__Data['ProdukcjaNetto'] = self.__Data['Brutto'] - \
            self.__Data['BrakiRazem']

        self.__Data['ProcentOdpadu'] = self.__Data['BrakiRazem'] / \
            self.__Data['Brutto']

        cols = ['Data', 'Brygada', 'Warsztat', 'Kategoria', 'Forma',
                'Odbiorca', 'Brutto', 'ProdukcjaNetto', 'ProcentOdpadu', 'WAGA_BRUTTO']

        return self.__Data[cols]

    def MixedCulletSummary(self, Wytop=0):
        '''Wytop = Suma wytopu bez wylewania'''
        df_1 = pd.DataFrame()
        df_1['Odpad'] = self.__Data['BrakiRazem'] * \
            self.__Data['WAGA_BRUTTO'] / 1000

        df_1['Netto'] = (self.__Data['Brutto'] -
                         self.__Data['BrakiRazem'])  # sztuk netto

        # Waga Kapy
        df_2 = self.__Data[['WAGA_BRUTTO', 'WAGA_NETTO']]
        df_2['Kapa'] = (self.__Data['WAGA_BRUTTO'] - self.__Data['WAGA_NETTO']).where(
            self.__Data['WAGA_NETTO'] != 0, 300)

        df = DataFrame()
        df['Wytop_Brutto'] = self.__Data['Brutto'] * \
            self.__Data['WAGA_BRUTTO'] / 1000
        df['Odpad'] = df_1['Odpad']
        df['Kapa'] = df_1['Netto'] * df_2['Kapa'] / 1000

        print(df.sum())

        RuznicaWytopProdukcja = Wytop - df['Wytop_Brutto'].sum()

        StluczkaMieszana = RuznicaWytopProdukcja + \
            df['Odpad'].sum() + df['Kapa'].sum()

        return StluczkaMieszana


class Summary:

    def __init__(self, begin, end):
        self.SummaryData = DataFrame(
            GetDataFromFDB(begin, end, 'DailySummary'))

    def DailyProductionSummary(self):

        DailyPullRate = self.SummaryData.groupby(
            self.SummaryData['Data'])

        print(DailyPullRate.sum())


class ProductionSummary:

    def __init__(self, start, stop):

        self.df = GetDataFromFDB(start, stop, 'ProductionReport')

    def ProductionSummary(self):

        arr = np.zeros([self.df['Data'].unique().size, 5], dtype=float)

        Tab = pd.DataFrame()
        Tab['Data'] = self.df['Data']
        Tab['Brygada'] = self.df['Brygada']
        Tab['Produkcja_Brutto'] = self.df['Brutto']
        Tab['Braki_Razem'] = self.df['BrakiRazem']
        # Tab['Srednia_mc'] = self.__Data[]
        Tab['Wydobycie_Brutto'] = self.df['Brutto'] * \
            self.df['WAGA_BRUTTO'] / 1000

        self.__SredniOdpadBrygady(arr, Tab)
        self.__SredniOdpadDzienny(arr, Tab)
        self.__WydobycieBruttoDzien(arr, Tab)

        Summary = pd.DataFrame()

        Summary['Data'] = Tab['Data'].unique()
        Summary['Brygada_1'] = arr[0:, 0]
        Summary['Brygada_2'] = arr[0:, 1]
        Summary['Brygada_3'] = arr[0:, 2]
        Summary['Odpad_na_Dzien'] = arr[0:, 3]
        Summary['Wydobycie_Brutto'] = arr[0:, 4]

        return Summary

    def __SredniOdpadBrygady(self, arr, Tab):
        _data = Tab['Data'][0]

        i = 0

        for (Data, Brygada), group in Tab.groupby(['Data', 'Brygada']):

            if (Data != _data):
                _data = Data
                i = i + 1

            if (Brygada == 1):
                arr[i][0] = group['Braki_Razem'].sum(
                ) / group['Produkcja_Brutto'].sum()
            elif (Brygada == 2):
                arr[i][1] = group['Braki_Razem'].sum(
                ) / group['Produkcja_Brutto'].sum()
            else:
                arr[i][2] = group['Braki_Razem'].sum(
                ) / group['Produkcja_Brutto'].sum()

        return arr

    def __SredniOdpadDzienny(self, arr, Tab):
        _data = Tab['Data'][0]
        i = 0

        for Data, group in Tab.groupby(['Data']):

            if (Data != _data):
                _data = Data
                i = i + 1

            arr[i][3] = group['Braki_Razem'].sum(
            ) / group['Produkcja_Brutto'].sum()

        return arr

    def __WydobycieBruttoDzien(self, arr, Tab):
        _data = Tab['Data'][0]
        i = 0

        for Data, group in Tab.groupby(['Data']):

            if (Data != _data):
                _data = Data
                i = i + 1

            arr[i][4] = group['Wydobycie_Brutto'].sum()

        return arr


class Report:

    def __init__(self, listOfDataFrames, sheetNames):
        self.__listOfDataFrames = listOfDataFrames
        self.__sheetNames = sheetNames

    def ReportToExcel(self, reportName='Report'):

        # Create a Pandas Excel writer using openpyxl as the engine

        outputPath = './Resources/Output/' + reportName + '.xlsx'
        writer = ExcelWriter(outputPath, engine='openpyxl')

        # Write each dataframe to a different worksheet.

        sn = 0
        for df in self.__listOfDataFrames:
            df.to_excel(
                writer, index=False, sheet_name=self.__sheetNames[sn])
            sn = sn + 1

        writer.index = False

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()


class BulbAverageWeight:

    def __init__(self):
        self.ListOfMeasurements = list()

    def AddMeasurement(self, value):
        self.ListOfMeasurements.append(value)

    def ShowAverageValue(self):

        value = 0

        for i in self.ListOfMeasurements:
            value = value + i

        avr = value/len(self.ListOfMeasurements)

        return avr


# BAW = BulbAverageWeight()

# while(True):
#     val = input('dodaj pomiar: ')

#     BAW.AddMeasurement(int(val))
#     print(BAW.ShowAverageValue())


# class SummaryPlot:
#     def __init__(self):
