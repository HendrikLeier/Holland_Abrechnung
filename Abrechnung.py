import pandas
import operator
from Transaktion import Transaction as tr

controll = False

attendees = ['Adrian', 'Leander', 'Marius', 'Timo', 'Sebastian', 'Hendrik', 'Julius', 'Clara']

debt_list = {name: 0.0 for name in attendees}

before_payed_list = {name: 0.0 for name in attendees}

after_payed_list = {name: 0.0 for name in attendees}

df = pandas.read_csv("Holland Abrechnung.csv")

for m in range(df.shape[0]):
    val = float(df.iloc[m, 0].replace(' €', '').replace(',', '.'))
    exclude = df.iloc[m, 1].split(', ')
    num_payers = len(attendees) - len(exclude)
    payer = df.iloc[m, 2]

    for a in attendees:
        if a not in exclude and a != payer:
            debt_list[a] += val / num_payers

    debt_list[payer] -= val * ((num_payers - 1) / num_payers)
    before_payed_list[payer] += val

# Create debtors and creditors

debtors = {}
creditors = {}

for a in attendees:
    if debt_list[a] > 0:
        debtors[a] = debt_list[a]
    elif debt_list[a] < 0:
        creditors[a] = debt_list[a]

if controll:
    dsum = 0.0
    csum = 0.0

    for a in debtors:
        dsum += debtors[a]

    for a in creditors:
        csum += creditors[a]

    print("Kontrollsumme Schuldner {0:.2f}".format(dsum))
    print("Kontrollsumme Gläubiger {0:.2f}".format(csum))

for a in attendees:
    after_payed_list[a] = round((before_payed_list[a] + debt_list[a]), 2)
    before_payed_list[a] = round(before_payed_list[a], 2)
    debt_list[a] = round(debt_list[a], 2)

print("Bezahlte Summen vor Abrechnung {}".format(before_payed_list))
print("Schulden oder Rückzahlungen (- ist Rückzahlung) {}".format(debt_list))
print("Bezahlte Summen nach Abrechung {}".format(after_payed_list))

csum = 0.0

for a in after_payed_list:
    csum += after_payed_list[a]

if controll:
    print("Kontroll Summe insgesamt: {}".format(csum))

# Generate Transactions

debtors = sorted(debtors.items(), key=operator.itemgetter(1), reverse=True)
creditors = sorted(creditors.items(), key=operator.itemgetter(1))

if controll:
    print("Schuldner {}".format(debtors))
    print("Gläubiger {}".format(creditors))

print("-----------------------------")

print("Vorgeschlagene Transaktionen:")

transactions = []

tsum = 0.0

for di in range(len(debtors)):
    for ci in range(len(creditors)):
        d = debtors[di]
        c = creditors[ci]
        if abs(d[1]) > abs(c[1]) and d[1] != 0 and c[1] != 0:
            transactions.append(tr(d[0], c[0], abs(c[1])))
            tsum += abs(c[1])
            debtors[di] = (d[0], d[1] + c[1])
            creditors[ci] = (c[0], 0.0)
        elif d[1] != 0 and c[1] != 0:
            transactions.append(tr(d[0], c[0], abs(d[1])))
            tsum += abs(d[1])
            debtors[di] = (d[0], 0.0)
            creditors[ci] = (c[0], c[1] + d[1])
            break

for t in transactions:
    print(t)

if controll:
    print("Gesamt-Transaktionssumme {:.2f}€".format(tsum))
