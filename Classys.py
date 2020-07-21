import pandas as pd
from pandas import DataFrame, ExcelWriter
import numpy as np
from connectFDB import TableGenerator, GetDataFromFDB
import calendar
from calendar import monthrange
import datetime
import matplotlib.pyplot as plt


class GeneralReport:

    # columns = ['Data', 'Brygada', 'Warsztat', 'NrKarty', 'Kategoria', 'Forma',
        #        'Odbiorca', 'Brutto', 'BrakiMasyMl', 'BRAKI_MASY_BZB', 'BrakiFormowania',
        #        'BrakiOdprezania', 'BrakiOpekiwania', 'Stluczka', 'BrakiInne', 'BrakiRazem',
        #        'WAGA_BRUTTO', 'WAGA_NETTO', 'CzasPracy', 'WYKONANIE']

    def __init__(self, begin, end):

        self.__Data = pd.DataFrame(
            GetDataFromFDB(begin, end, 'ProductionReport'))

    def ProductionReport(self):

        cols = ['Data', 'Brygada', 'Warsztat', 'NrKarty', 'Kategoria', 'Forma',
                'Odbiorca', 'Brutto', 'BrakiRazem', 'WAGA_BRUTTO', 'WAGA_NETTO', 'CzasPracy']

        print(self.__Data[cols].to_string(index=False))

    def GeneralDailyReport(self):

        self.__Data['ProdukcjaNetto'] = self.__Data['Brutto'] - \
            self.__Data['BrakiRazem']

        self.__Data['ProcentOdpadu'] = self.__Data['BrakiRazem'] / \
            self.__Data['Brutto']

        cols = ['Data', 'Brygada', 'Kategoria', 'Forma',
                'Odbiorca', 'Brutto', 'ProdukcjaNetto', 'ProcentOdpadu']

        print(self.__Data[cols].to_string(index=False))


begin = datetime.date(2020, 7, 13)
end = datetime.date(2020, 7, 17)
gp = GeneralReport(begin, end)
gp.ProductionReport()


class Summary:

    def __init__(self, begin, end):
        self.SummaryData = DataFrame(
            GetDataFromFDB(begin, end, 'DailySummary'))

    def DailyProductionSummary(self):

        DailyPullRate = self.SummaryData.groupby(
            self.SummaryData['Data'])

        print(DailyPullRate)


# begin = datetime.date(2020, 7, 13)
# end = datetime.date(2020, 7, 17)

# summ = Summary(begin, end)

# summ.DailyProductionSummary()


class ProductionSummary:

    def __init__(self, start, stop):
        self.__Data = pd.DataFrame(
            TableGenerator(start, stop, 'ProductionReport'))

    def ProductionSummary(self):

        df = self.__Data

        arr = np.zeros([df[0].unique().size, 5], dtype=float)

        Tab = pd.DataFrame()
        Tab['Data'] = df[0]
        Tab['Brygada'] = df[1]
        Tab['Produkcja_Brutto'] = df[7]
        Tab['Braki_Razem'] = df[15]
        # Tab['Srednia_mc'] = self.__Data[]
        Tab['Wydobycie_Brutto'] = df[7] * df[16] / 1000

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


# summ = ProductionSummary('01.07.2020', '17.07.2020')
# print(summ.ProductionSummary())


class Report:

    def ReportToExcel(self, listOfDataFrames, sheetNames):

        # Create some Pandas dataframes from some data.
        df1 = listOfDataFrames[0]
        df2 = listOfDataFrames[1]

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = ExcelWriter('Report.xlsx', engine='openpyxl')

        # Write each dataframe to a different worksheet.
        df1.to_excel(writer, index=False, sheet_name=sheetNames[0])
        df2.to_excel(writer, index=False, sheet_name=sheetNames[1])

        writer.index = False
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()


# df1 = GeneralReport('01.07.2020', '15.07.2020')
# df2 = ProductionSummary('01.07.2020', '15.07.2020')

# sheetNames = ['Productron_Report', 'Summary']
# listOfDataFrames = [df1.ProductionReport(), df2.ProductionSummary()]

# report = Report()

# report.ReportToExcel(listOfDataFrames, sheetNames)
