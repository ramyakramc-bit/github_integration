#python - Create the Table 
import sqlite3
conn = sqlite3.connect('mydb.db')
c = conn.cursor()
c.execute(''' CREATE TABLE IF NOT EXISTS CRYPTOTBL(
          ID VARCHAR(50) PRIMARY KEY,
          SYMBOL VARCHAR(10),
          NAME VARCHAR(100),
          CURRENT_PRICE DECIMAL(18,6),
          MARKET_CAP BIGINT,
          MARKET_CAP_RANK INT,
          TOTAL_VOLUME BIGINT,
          CIRCULATING_SUPPLY DECIMAL(18,6),
          TOTAL_SUPPLY DECIMAL(20,6),
          ATH DECIMAL(18,6),
          ATL DECIMAL(18,6),
          LAST_UPDATED DATE)
''')

c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS CRYPTO_PRICES (
       PRICE_USD NUMERIC NOT NULL,
       DATE      DATE    NOT NULL,
       ID        TEXT    NOT NULL,
  FOREIGN KEY (ID) REFERENCES CRYPTOTBL(ID)
    ON UPDATE CASCADE
    ON DELETE CASCADE)
          ''')

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS oiltbl (
          date Date Primary key, 
          Price_USD Decimal(18,6)
)''')

c=conn.cursor()
c.execute ('''create table if not exists stocktbl(
date Date,
open decimal(18,6),
high decimal(18,6),
low decimal(18,6),
close decimal(18,6),
volume bigint,
ticker_name varchar(20)
)''')
conn.commit()

import pandas as pd
path = r"C:\Users\Ramya\crypto_data.csv"
coin_df = pd.read_csv(path)
#print(coin_df)

# insert in to table
c = conn.cursor()
c.execute("Delete from Cryptotbl")
c = conn.cursor()
c.executemany("insert into cryptotbl values(?,?,?,?,?,?,?,?,?,?,?,?)",coin_df.values.tolist())
conn.commit()
print("after inserting cryptotbl")

#### Crypto_History###
path = r"C:\Users\Ramya\coin_his.csv"
coin_his_df = pd.read_csv(path)
#print(coin_df)

# insert in to table
c = conn.cursor()
c.execute("Delete from CRYPTO_PRICES")
c = conn.cursor()
c.executemany("insert into CRYPTO_PRICES values(?,?,?)",coin_his_df.values.tolist())
conn.commit()
print("after Inserting CRYPTO_PRICES")

import pandas as pd
path = r"C:\Users\Ramya\oil_prices.csv"
oil_df = pd.read_csv(path)
#print(oil_df)
c = conn.cursor()
c.execute("Delete from oiltbl")
c = conn.cursor()
c.executemany("insert into oiltbl values(?,?)",oil_df.values.tolist())
conn.commit()
print("after Inserting oiltbl")
# stocktbl 
import sqlite3
conn=sqlite3.connect('mydb.db')



#print(stock_df)

save_dir = r"C:\Users\Ramya"
import sqlite3
conn=sqlite3.connect('mydb.db')
c=conn.cursor()

sdf1=pd.read_csv(rf"{save_dir}\^GSPC.csv")
sdf1 = sdf1.rename(columns={
    "Date": "date",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume"
})

sdf1["date"] = pd.to_datetime(sdf1["date"], errors="coerce").dt.strftime("%Y-%m-%d")
sdf1 = sdf1.dropna(subset=["date"])
sdf1 = sdf1[["date", "open", "high", "low", "close", "volume", "ticker_name"]]
c.executemany("insert into stocktbl(date,open,high,low,close,volume,ticker_name) values(?,?,?,?,?,?,?)",sdf1.values.tolist())
conn.commit()

sdf1=pd.read_csv(rf"{save_dir}\^IXIC.csv")
sdf1 = sdf1.rename(columns={
    "Date": "date",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume"
})

sdf1["date"] = pd.to_datetime(sdf1["date"], errors="coerce").dt.strftime("%Y-%m-%d")
sdf1 = sdf1.dropna(subset=["date"])
sdf1 = sdf1[["date", "open", "high", "low", "close", "volume", "ticker_name"]]
c.executemany("insert into stocktbl(date,open,high,low,close,volume,ticker_name) values(?,?,?,?,?,?,?)",sdf1.values.tolist())
conn.commit()

sdf1=pd.read_csv(rf"{save_dir}\^NSEI.csv")
sdf1 = sdf1.rename(columns={
    "Date": "date",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume"
})

sdf1["date"] = pd.to_datetime(sdf1["date"], errors="coerce").dt.strftime("%Y-%m-%d")
sdf1 = sdf1.dropna(subset=["date"])
sdf1 = sdf1[["date", "open", "high", "low", "close", "volume", "ticker_name"]]
c.executemany("insert into stocktbl(date,open,high,low,close,volume,ticker_name) values(?,?,?,?,?,?,?)",sdf1.values.tolist())
conn.commit()
print("after Inserting stocktbl")
