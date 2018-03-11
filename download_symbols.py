import datetime
import pandas_datareader.data as wb
import sqlite3

from_date = datetime.date(2000, 1, 1)
to_date = datetime.date(2018, 3, 6)

cnx = sqlite3.connect('stocks.db')

symbols_already_downloaded = []

cur = cnx.cursor()
try:
    cur.execute('SELECT DISTINCT(Symbol) FROM stocks')
    for s in cur.fetchall():
        symbols_already_downloaded.append(s[0])
except sqlite3.OperationalError:
    print('Stocks table doesn\'t exist yet')
finally:
    cur.close()

with open('symbols.csv', 'r') as symbols_file:
    first_symbol = True
    for line in symbols_file:
        v = line.split('|')

        symbol = v[0]

        if symbol in symbols_already_downloaded:
            print('Already have %s' % symbol)
            continue

        print('Downloading %s' % symbol)

        try:
            symbol_df = wb.DataReader(symbol,
                                      "google",
                                      from_date,
                                      to_date)

            symbol_df = symbol_df.assign(Symbol=symbol)

            symbol_df.to_sql('stocks',
                             cnx,
                             if_exists='append')
            first_symbol = False
        except:
            print('Problem with %s' % symbol)
