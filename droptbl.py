import sqlite3
conn = sqlite3.connect('mydb.db')
c = conn.cursor()

c.execute('''DROP TABLE IF EXISTS CRYPTOTBL''')
c.execute('''DROP TABLE IF EXISTS oiltbl''')
c.execute('''DROP TABLE IF EXISTS stocktbl''')
c.execute('''DROP TABLE IF EXISTS CRYPTO_PRICES''')

conn.commit()
conn.close()