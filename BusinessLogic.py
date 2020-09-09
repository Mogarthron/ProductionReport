from Classys import GeneralReport
from datetime import date


def SimplyDayliReport():

    print('Podaj Datę: (yyyy.mm.dd)')
    inputDate = input()

    year = int(inputDate[:4])
    month = int(inputDate[5:7])
    day = int(inputDate[8:])

    DateRange = date(year, month, day)

    gp = GeneralReport(DateRange, DateRange)
    cols = ['Brygada', 'Warsztat', 'Kategoria', 'Forma',
            'Odbiorca', 'Brutto', 'ProdukcjaNetto', 'ProcentOdpadu']

    df1 = gp.GeneralDailyReport()

    df2 = df1.groupby('Brygada')
    brigadeQuality = 1 - (df2['ProdukcjaNetto'].sum() / df2['Brutto'].sum())

    print(df1[cols].to_string(index=False))
    print(brigadeQuality.to_string())
