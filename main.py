import BusinessLogic as logic

print('1: Skrócony dzienny raport')
print('2: Wydrukowanie raportu do excela za dany miesiąc')
quitCheck = int(input('Rodzaj raportu: '))

logic.ControllLogic(quitCheck)
