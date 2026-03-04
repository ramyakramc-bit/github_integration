#this is for yahoo finance code(stock)--------------------------------------------------
import yfinance as yf
import pandas as pd
# choose indices
tickers = ["^GSPC", "^IXIC", "^NSEI"]
start_date = "2020-01-01"
end_date = "2026-12-01"
save_dir = r"C:\Users\Ramya"

#download stock data
stocks_df = yf.download(tickers, start=start_date, end=end_date,group_by="ticker")
for ticker in tickers:
  stocks_df[ticker].reset_index()
  stocks_df[ticker].to_csv(rf"{save_dir}\{ticker}.csv")
  df=pd.read_csv(rf"{save_dir}\{ticker}.csv")
  df['ticker_name'] = ticker

  df.to_csv(rf"{save_dir}\{ticker}.csv",index=False)
  #df=pd.read_csv(f'{ticker}.csv')
  #print(df)


#---------------------------------------------------------------------------------------
#this is for oil code
#python
#filter for years between 2020 t0 2026


#----------------------------------------------------------------------------------------
#this is for cryptocurrency
from numpy._core import records
import requests # use string formating and for loop and scroll through 5 pages to collect data
import pandas as pd
from datetime import datetime
records =[]
for j in range(1,5):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&per_page=250&order=market_cap_desc&page={j}&sparkline=False"
    response = requests.get(url)
    #print('response code == 200',response.status_code)
    if response.status_code == 200:
    #print('response code == 200')
        data=response.json()
     
        for i in range(len(data)):
              records.append(dict(
                  id = data[i]['id'],
                  symbol = data[i]['symbol'],
                  Name = data[i]['name'],
                  Current_price = data[i]['current_price'],
                  market_cap = data[i]['market_cap'],
                  market_cap_rank = data[i]['market_cap_rank'],
                  total_volume = data[i]['total_volume'],
                  circulating_supply = data[i]['circulating_supply'],
                  total_supply = data[i]['total_supply'],
                  ath = data[i]['ath'],
                  atl = data[i]['atl'],
                  last_updated = data[i]['last_updated']))
              

for j in range(len(records)):
 ts = records[j]["last_updated"]
 dt = datetime.fromisoformat(ts.replace('z', '+00:00'))
 records[j]["last_updated"] = dt.date().isoformat()
 #print(records[j]["last_updated"])

crypto_df= pd.DataFrame(records)
save_dir = r"C:\Users\Ramya"
crypto_df.to_csv(rf"{save_dir}\crypto_data.csv",index=False)

#print(pd.read_csv(out_path))
# Oil Prices 
import pandas as pd
save_dir = r"C:\Users\Ramya"
oil_df = pd.read_csv("http://raw.githubusercontent.com/datasets/oil-prices/main/data/wti-daily.csv")
oil_df.to_csv(rf"{save_dir}\oil_prices.csv",index=False)
oil_df = pd.read_csv(rf"{save_dir}\oil_prices.csv")
print(oil_df)

#-----------------------------------------------------------------------
# Crypto_History

import requests
import sys
import pandas as pd
import json
from datetime import datetime
from pathlib import Path
out_path = Path.home() / 'coin_data.csv'
crypto_df.to_csv(out_path, index=False)
coins = ["bitcoin", "ethereum", "tether"]

for i in range(len(coins)-1):
    url = (f"https://api.coingecko.com/api/v3/coins/{coins[i]}/market_chart?vs_currency=usd&days=365")
    
    response = requests.get(url)
    data=response.json()
    # print("RSCode=", response.status_code)
    print ('coin:',coins[i])
    print ("response.status_code",response.status_code)
    if response.status_code == 200:
        df = pd.DataFrame(data["prices"], columns=['MillSecond', 'Price'])
        T1 = pd.to_datetime(df['MillSecond'], unit='ms', utc=True)
        df['Date'] = T1.dt.date
        df['Coin id'] = coins[i]
        df.drop(['MillSecond'], axis=1, inplace=True)
        out_path = Path.home() / 'coin_his.csv'
        df.to_csv(out_path, mode="a", index=False)
    else:
        print("Error Status Code :", response.status_code)



