from Classys import GeneralReport, ProductionSummary, Report
from calendar import monthrange
from datetime import date
import os
from os import kill


# class logic:
#     def ControllLogic(self, quitCheck=1):
#         while(1):

#             if (quitCheck == 1):
#                 SimplyDayliReport()
#             else:
#                 break

#         print('gagaga')


def ControllLogic(quitCheck):
    while(1):

        if (quitCheck == 1):
            SimplyDayliReport()
        else:
            break

    if (quitCheck == 2):
        MonthlyReportToExcel()


def SimplyDayliReport():

    print('Podaj Datę: (yyyy.mm.dd)')
    inputDate = input()

    if (inputDate == 'quit'):
        ControllLogic(0)
    else:
        year = int(inputDate[:4])
        month = int(inputDate[5:7])
        day = int(inputDate[8:])

        DateRange = date(year, month, day)

        gp = GeneralReport(DateRange, DateRange)
        cols = ['Brygada', 'Warsztat', 'Kategoria', 'Forma',
                'Odbiorca', 'Brutto', 'ProdukcjaNetto', 'ProcentOdpadu']

        df1 = gp.GeneralDailyReport()

        df2 = df1.groupby('Brygada')
        brigadeQuality = 1 - \
            (df2['ProdukcjaNetto'].sum() / df2['Brutto'].sum())

        print(df1[cols].to_string(index=False))
        print(brigadeQuality.to_string())
        generalDefects = 1 - (df1['ProdukcjaNetto'].sum()/df1['Brutto'].sum())
        print('Odpad całkowity: {} procent'.format(generalDefects))


def MonthlyReportToExcel():

    year = int(input('podaj rok raportu (YYYY): '))
    month = int(input('podaj miesiąc raportu (MM): '))
    st = monthrange(year, month)

    FirstDayOfMonth = date(year, month, 1)
    LastDayOfMonth = date(year, month, st[1])
    reportName = 'Raport_' + str(year) + '_' + str(month)

    pr = GeneralReport(FirstDayOfMonth, LastDayOfMonth)
    ps = ProductionSummary(FirstDayOfMonth, LastDayOfMonth)

    listOfDataFrames = [pr.ProductionReport(), ps.ProductionSummary()]
    sheetNames = ['Production_Report', 'Summary']

    r = Report(listOfDataFrames, sheetNames)

    r.ReportToExcel(reportName=reportName)
