import pandas
import sqlite3

from scipy.stats import linregress


cnx = sqlite3.connect('stocks.db')

symbols = []
db_symbols = cnx.execute('SELECT DISTINCT (Symbol) FROM stocks')
for db_symbol in db_symbols.fetchall():
    symbols.append(db_symbol[0])


symbol_stats = pandas.DataFrame(columns=['symbol', 'stderr', 'slope', 'first_date'])
i = 0
for symbol in symbols:
    stock_df = pandas.read_sql_query(
        "SELECT * FROM stocks WHERE symbol = '%s'" % symbol,
        cnx,
        parse_dates=['Date']
    )

    close_vals = stock_df.Close.values
    mini = min(close_vals)
    maxi = max(close_vals)

    first_date = min(stock_df.Date)

    norm_close_vals = [(x - mini) / float(maxi) for x in close_vals]

    obj = linregress(norm_close_vals, stock_df.index.values)

    symbol_stats.loc[i] = [symbol, obj.stderr, obj.slope, first_date]
    i += 1

sorted_stderr = symbol_stats.sort_values(by=['stderr'])

sorted_stderr.to_sql('linreg',
                     cnx,
                     if_exists='replace')

print(sorted_stderr)
