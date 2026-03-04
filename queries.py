import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import date, timedelta
import sqlite3

# DB connection (keep one connection for simple apps)
conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

st.title("Cross Market Analysis")

# --- Sidebar menu ---
with st.sidebar:
    # 3 items => provide 3 icons; fix icon names and spelling
    selected = option_menu(
        "Main Menu",
        ["Market Overview", "SQL Queries Runner", "Top Three Crypto Analysis"],
        icons=["house", "funnel", "gear"],  # pick any valid icons
        menu_icon="cast",
        default_index=0
    )

# --- Market Overview ---

if selected == "Market Overview":
    
    col1, col2 = st.columns(2)
    with col1:
        Start_date = st.date_input("Start Date", format="YYYY-MM-DD")
    with col2:
        end_date = st.date_input("End Date", format="YYYY-MM-DD")
    #st.subheader("BITCOIN") 
    sql = """select avg(price_usd) from CRYPTO_PRICES CP where ID = 'bitcoin' and CP.date >= ? and CP.date <= ? """
    df_btc=pd.read_sql(sql,con=conn,params=[Start_date, end_date])
    #st.dataframe(df,use_container_width=True)
    #st.subheader("Oil Price") 
    sql = """ Select avg(Price_USD) from oiltbl ot where ot.date >=? and ot.date<=? """
    df_oil=pd.read_sql(sql,con=conn,params=[Start_date, end_date])
    #st.dataframe(df,use_container_width=True)
    avg_row = pd.DataFrame({
    "BITCOIN": [df_btc.iloc[0, 0]],
    "OIL": [df_oil.iloc[0, 0]]
    })
    st.dataframe(avg_row,use_container_width=True)
    st.subheader("Daily Price Trend") 
    sql =""" select cp.date, cp.price_usd, ot.Price_Usd from CRYPTO_PRICES cp , oiltbl ot
             where ot.date = cp.date and cp.id = 'bitcoin' and
             cp.date >=? and Cp.date<=? order by cp.date ASC"""

    #sql = """ select * from cryptotbl where Last_Updated >= ? and Last_updated <=? order by Last_updated ASC"""
    df = pd.read_sql_query(sql,con=conn,params=[Start_date,end_date])
    st.dataframe(df,use_container_width=True)

# --- FILTERS (placeholder) ---
elif selected == "Top Three Crypto Analysis":

    c = conn.cursor()
   # st.info("Filters coming soon...")
    
    default_end = date.today()               
    default_start = default_end - timedelta(days=30)  

    col1, col2 = st.columns(2)
    with col1:
        Start_date = st.date_input("Start Date", value=default_start, format="YYYY-MM-DD")
    with col2:    
        end_date = st.date_input("End Date", value=default_end, format="YYYY-MM-DD")


    c.execute("SELECT  Name FROM CRYPTOTBL order by MARKET_CAP_RANK ASC limit 3")
    
    rows = c.fetchall()
    id_list = []
    for row in rows:
        id_list.append(row[0])
    
    option = st.selectbox("Select ID", id_list)

    sql = """
    SELECT DATE, PRICE_USD
    FROM CRYPTO_PRICES CP,CRYPTOTBL CT
    WHERE CP.ID = CT.ID 
      AND CT.NAME = ?
      AND CP.DATE >= ?
      AND CP.DATE <= ?
    ORDER BY DATE ASC
    """
    params = (option, Start_date, end_date)
    c.execute(sql, params)
    rows = c.fetchall()
    
    df = pd.DataFrame(rows, columns=["DATE", "PRICE_USD"])
    if df.empty:
        st.warning("No price data found for this coin and date range.")
    else:
        df["DATE"] = pd.to_datetime(df["DATE"])
        df = df.sort_values("DATE")
        st.subheader(f"Price Trend: {option}")
        st.line_chart(df.set_index("DATE"))

    df = pd.read_sql_query(sql,con=conn,params=[option, Start_date,end_date])
    st.dataframe(df)

# --- QUERIES ---
elif selected == "SQL Queries Runner":
    # Only define and use `option` inside this block
    option = st.selectbox(
        "Select a query",
        (
            "Display the entire table",
            "Display top 3 crypto currencies by Market Cap",
            "Display coins where circulating supply exceeds 90% of total Supply",
            "Display the coins that are within 10% of their all time high(ATH)",
            "Display average Market Cap Rank of Coins with Volumne above $1B",
            "Display the most recently Updated Coin",
            #Crypto_Price
            "Display highest daily price of Bitcoin in the last 365 days",
            "Display average daily price of Ethereum in Past 1 Year",
            "Display Daily price trend of Bitcoin in Jan 2025",
            "Display the coin with the highest avg Price over 1 Year",
            "Display %change in bitcoin price between Sep 2024 and Sep 2025",
            #Oil_Price
            "Display the highest oil Price in the last 5 years",
            "Display Average oil price per year",
            "Display Oil Price during Covid Crash",
            "Display Lowest Oil Price in last 10 Years",
            "Display the volatility of oil Price",
            "Display price",
            #stock
            "Get all stock prices for a given ticker",
            "Find the highest closing price for NASDAQ (^IXIC)",
            "List top 5 days with highest price difference (high - low) for S&P 500 (^GSPC)",
            "Get monthly average closing price for each ticker",
            "Get average trading volume of NSEI in 2024",
#Join Queries
            "Compare AVG Bitcoin vs Oil Price in 2025",
            "Check if Bitcoin moves with S&P 500",
            "Compare Ehereum and NASDAQ daily Price in 2025",
            "Find days when Oil Price Spiked and compare with Bitcoin Price Change",
            "Compare top 3 coins daily Price Trend ns Nifity",
            "Compare Stock Price ^GSPC with Crude Oil Price on the same dates",
            "Correlate Bitcoin Closing Price with Crude Oil closing Price",
            "Compare NASDAQ With Ethereum Price Trend",
            "Join top 3 Crypto Coins with Stock Indices for 2025",
            "Stock Price, Oil Price, and BITCOIN Daily Comparison"
        ),
        index=0
    )

    # Now safely branch on `option`
    if option == "Display the entire table":
        df = pd.read_sql("SELECT * FROM CryptoTbl", con=conn)
        st.dataframe(df)
    if option == "Display top 3 crypto currencies by Market Cap":
            df = pd.read_sql("""
                SELECT *
                FROM CryptoTbl
                ORDER BY Current_price DESC
                LIMIT 3
            """, con=conn)
            st.dataframe(df)
    if option == "Display coins where circulating supply exceeds 90% of total Supply":
       df = pd.read_sql("""SELECT * FROM CRYPTOTBL WHERE TOTAL_SUPPLY IS NOT NULL AND TOTAL_SUPPLY > 0
                          AND CIRCULATING_SUPPLY IS NOT NULL
                          AND (CIRCULATING_SUPPLY * 1.0) / TOTAL_SUPPLY >= 0.9
                          ORDER BY CIRCULATING_SUPPLY  DESC""" , con=conn)
       st.dataframe(df)
    if option == "Display the coins that are within 10% of their all time high(ATH)":
        df=pd.read_sql(""" SELECT * FROM CRYPTOTBL WHERE
                       Current_Price > 0 and
                       ATH > 0 AND
                       Current_Price < ATH AND
                       CUrrent_Price >= (ATH*0.9)""", con=conn)
        st.dataframe(df)
    if option == "Display average Market Cap Rank of Coins with Volumne above $1B":
        df=pd.read_sql(""" Select avg(MARKET_CAP_RANK) FROM CRYPTOTBL where total_volume > 10000000  """, con=conn)
        st.dataframe(df)
    if option == "Display the most recently Updated Coin":
        df=pd.read_sql(""" select * from CRYPTOTBL order by last_updated desc limit 1""", con=conn)
        st.dataframe(df)
    if option == "Display highest daily price of Bitcoin in the last 365 days":
        df=pd.read_sql(""" select ID, Max(price_usd) from CRYPTO_PRICES Where ID = 'bitcoin' 
                           And Date >= date('now','-365 day')
                       """, con=conn)
        st.dataframe(df)
    if option == "Display average daily price of Ethereum in Past 1 Year":
        df=pd.read_sql(""" select AVG(price_usd),date from CRYPTO_PRICES Where ID = 'ethereum' 
                           And Date >= date('now','-365 day')
                           group by date
                       """, con=conn)
        st.dataframe(df)
    if option == "Display Daily price trend of Bitcoin in Jan 2025":
         df=pd.read_sql(""" select * from CRYPTO_PRICES Where ID = 'bitcoin' 
                        and date > '2025-01-01'  AND date < '2026-01-31' """, con=conn)
         st.dataframe(df)
    if option == "Display the coin with the highest avg Price over 1 Year":
        df=pd.read_sql("""
                       SELECT ID, ROUND(AVG(PRICE_USD), 6) AS avg_price_1y_usd
                        FROM CRYPTO_PRICES
                        WHERE date("DATE") >= date('now','-365 day')
                        GROUP BY ID ORDER BY avg_price_1y_usd DESC LIMIT 1""", con=conn)
        st.dataframe(df)
    if option == "Display %change in bitcoin price between Sep 2024 and Sep 2025":
        Sep2024 = pd.read_sql(""" Select avg(Price_USD) from Crypto_Prices where id = "bitcoin"
                              and date between '2024-09-01'AND '2024-09-30' """, con=conn)
        sep2025 = pd.read_sql(""" Select avg(Price_USD) from Crypto_Prices where id = "bitcoin"
                              and date between '2024-09-01'AND '2024-09-30' """, con=conn)
        
        
        df=sep2025
        
        st.dataframe(df)
    if option == "Display the highest oil Price in the last 5 years":
        df=pd.read_sql(""" select MAX(Price_USD) from oiltbl Where date > date('now','-5 years') 
                       """, con=conn)
        st.dataframe(df)
    if option == "Display Average oil price per year":              
        df=pd.read_sql(""" SELECT strftime('%Y', "date") AS year, ROUND(AVG(price_usd), 2) AS avg_price_usd
                        FROM oiltbl where date > date('now','-5 years') 
                        GROUP BY strftime('%Y', "date")
                        ORDER BY year""", con=conn)
        st.dataframe(df)
    if option == "Display Oil Price during Covid Crash":
        df=pd.read_sql(""" SELECT date, price_usd FROM oiltbl WHERE date BETWEEN 
                           date('2020-03-01') AND date('2020-04-30') """, con=conn)
        st.dataframe(df)
    if option == "Display Lowest Oil Price in last 10 Years":
        df=pd.read_sql(""" SELECT date, Min(price_usd) FROM oiltbl WHERE date >=date('now','-10 years') 
                            """, con=conn)
        st.dataframe(df)
    if option == "Display the volatility of oil Price":
        df=pd.read_sql("""SELECT
        strftime('%Y', date) AS year,
        MAX(price_usd) AS max_price,
        MIN(price_usd) AS min_price,
        (MAX(price_usd) - MIN(price_usd)) AS volatility
        FROM oiltbl
        WHERE year BETWEEN '2020' AND '2026'
        GROUP BY strftime('%Y', date)
        ORDER BY year """, con=conn)
        st.dataframe(df)
    if option == "Get all stock prices for a given ticker":
        df=pd.read_sql("""select open,low,high,close from 'stocktbl' where ticker_name ='^IXIC' """, con=conn)
        st.dataframe(df)
    
    if option == "Get monthly average closing price for each ticker":
        c=conn.cursor()
        c.execute("SELECT distinct ticker_name FROM stockTBL")
        rows = c.fetchall()
        id_list = []
        for row in rows:
            id_list.append(row[0])
        option = st.selectbox("Select ID", id_list)

        sql = """SELECT ticker_name,
        strftime('%Y-%m', date) AS month,
        AVG(close) AS avg_close FROM stocktbl
                       where ticker_name = ?
        GROUP BY ticker_name, month
        ORDER BY ticker_name, month """
        df_btc=pd.read_sql(sql,con=conn,params=[option])
        st.dataframe(df_btc,use_container_width=True)
    
    if option == "Find the highest closing price for NASDAQ (^IXIC)":
        df=pd.read_sql("""SELECT max(close)
        FROM stocktbl
        WHERE ticker_name = '^NSEI'
        AND date BETWEEN '2024-01-01' AND '2024-12-31' """, con=conn)
        st.dataframe(df)

    if option == "List top 5 days with highest price difference (high - low) for S&P 500 (^GSPC)":
        df=pd.read_sql("""SELECT avg(high)- avg(low) from stocktbl where ticker_name ='^GSPC'order by date LIMIT 5""", con=conn)
        st.dataframe(df)
    if option == "Get monthly average closing price for each ticker":
        df=pd.read_sql(""" SELECT ticker_name,
                    strftime('%Y-%m', date) AS month,
                    AVG(close) AS avg_close FROM stocktbl
                    GROUP BY ticker_name, month
                    ORDER BY ticker_name, month """, con=conn)
        st.dataframe(df)
    if option == "Get average trading volume of NSEI in 2024":
        df=pd.read_sql(""" SELECT AVG(volume) from stocktbl WHERE ticker_name = '^NSEI'
                            AND date BETWEEN '2024-01-01' AND '2024-12-31' """, con=conn)
        st.dataframe(df)   
    
    if option == "Compare AVG Bitcoin vs Oil Price in 2025":
        df=pd.read_sql(""" Select avg(Cp.Price_USD) as crypto_Price, Avg(OT.Price_USD) as Oil_price
                         from Crypto_Prices CP , Oiltbl OT
                        where ot.date = cp.date and cp.id = 'bitcoin' and
                        cp.date >='2025-01-01' and Cp.date<='2025-12-31' """, con=conn)
        st.dataframe(df)
    if option == "Check if Bitcoin moves with S&P 500":
        df=pd.read_sql("""SELECT DATE(b.last_updated) AS date, b.current_price AS bitcoin_price,
                        s.close AS stock_close_price FROM cryptotbl b JOIN stocktbl s ON DATE(b.last_updated) = DATE(s.date)
                         """,con=conn)
        st.dataframe(df)
    if option == "Compare Ehereum and NASDAQ daily Price in 2025":
        df=pd.read_sql("""select Cp.date , CP.Price_usd as ETH_PRICE, sp.close as NASDAQ_PRICE from 
                       CRYPTO_PRICES CP, stocktbl sp where cp.date = sp.date
                       and id = 'ethereum' and cp.date between '2025-01-01' and '2025-12-31'""",con=conn) 
        st.dataframe(df)
    if option == "Find days when Oil Price Spiked and compare with Bitcoin Price Change":
        df =pd.read_sql("""select date(b.last_updated), o.price_usd as oil_price, b.current_price as bitcoin_price from oiltbl o 
            join cryptotbl b on strftime('%Y', b.last_updated)=strftime('%Y', o.date) and 
            strftime('%M', b.last_updated)=strftime('%M', o.date) where b.id = 'bitcoin'""",con=conn)
        st.dataframe(df)
    if option == "Compare top 3 coins daily Price Trend ns Nifity":
        c=conn.cursor()
        default_end = date.today()               
        default_start = default_end - timedelta(days=30)  
        col1, col2 = st.columns(2)
        with col1:
            Start_date = st.date_input("Start Date", value=default_start, format="YYYY-MM-DD")
        with col2:    
            end_date = st.date_input("End Date", value=default_end, format="YYYY-MM-DD")
    
        sql = """
        SELECT CP.DATE, CT.NAME, CP.PRICE_USD, SP.OPEN as STOCK_PRICE
        FROM CRYPTO_PRICES CP,CRYPTOTBL CT,Stocktbl SP
        WHERE CP.ID = CT.ID 
        AND CP.DATE = SP.DATE
        AND CT.NAME in (SELECT  Name FROM CRYPTOTBL order by MARKET_CAP_RANK ASC limit 3)
        AND CP.DATE >= ?
        AND CP.DATE <= ?
        AND SP.ticker_name = '^NSEI'
        ORDER BY CP.DATE ASC
        """
        df = pd.read_sql_query(sql,con=conn,params=[ Start_date,end_date])
        st.dataframe(df)
    
    if option == "Compare Stock Price ^GSPC with Crude Oil Price on the same dates":
        col1, =  st.columns(1)
        with col1:
            Closing_date = st.date_input("Closing Date", format="YYYY-MM-DD")
        sql= """ Select distinct SP.OPEN as Stock_Price, OT.Price_USD as Oil_Closing_price
                        from stocktbl SP , Oiltbl OT
                        where sp.date = ot.date and SP.ticker_name = '^GSPC' and
                        Sp.date =? """
        df_btc=pd.read_sql(sql,con=conn,params=[Closing_date])
        st.dataframe(df_btc,use_container_width=True)
    if option == "Correlate Bitcoin Closing Price with Crude Oil closing Price":
        col1, =  st.columns(1)
        with col1:
            Closing_date = st.date_input("Closing Date", format="YYYY-MM-DD")
        sql= """ Select distinct Cp.Price_USD as crypto_Closing_Price, OT.Price_USD as Oil_Closing_price
                        from Crypto_Prices CP , Oiltbl OT
                        where ot.date = cp.date and cp.id = 'bitcoin' and
                        cp.date =? """
        df_btc=pd.read_sql(sql,con=conn,params=[Closing_date])
        st.dataframe(df_btc,use_container_width=True)
    if option == "Compare NASDAQ With Ethereum Price Trend":
        c=conn.cursor()
        default_end = date.today()               
        default_start = default_end - timedelta(days=30)  
        col1, col2 = st.columns(2)
        with col1:
            Start_date = st.date_input("Start Date", value=default_start, format="YYYY-MM-DD")
        with col2:    
            end_date = st.date_input("End Date", value=default_end, format="YYYY-MM-DD")
    
        sql = """
        select distinct Cp.date , CP.Price_usd as ETH_PRICE, sp.close as NASDAQ_PRICE from
        CRYPTO_PRICES CP, stocktbl sp where cp.date = sp.date
        and id = 'ethereum'  
        AND CP.DATE >= ?
        AND CP.DATE <= ?
        AND SP.ticker_name = '^IXIC'
        ORDER BY CP.DATE ASC
        """
        df_btc=pd.read_sql(sql,con=conn,params=[Start_date,end_date])
        st.dataframe(df_btc,use_container_width=True)

    if option == "Join top 3 Crypto Coins with Stock Indices for 2025":
        df = pd.read_sql("""select date(c.last_updated) as date, c.id as crypto_id, avg(c.current_price) as crypto_price, s.ticker_name as source,s.close as stock_price
        from cryptotbl c join stocktbl s on  s.date = date(c.last_updated) where strftime('%Y', c.last_updated) = '2026'
        group by date(c.last_updated), c.id, s.ticker_name, s.close order by crypto_price desc""",con=conn)

        st.dataframe(df)
    if option == "Stock Price, Oil Price, and BITCOIN Daily Comparison":
        c=conn.cursor()
        default_end = date.today()               
        default_start = default_end - timedelta(days=30)  
        col1, col2 = st.columns(2)
        with col1:
            Start_date = st.date_input("Start Date", value=default_start, format="YYYY-MM-DD")
        with col2:    
            end_date = st.date_input("End Date", value=default_end, format="YYYY-MM-DD")
        sql = """select distinct Cp.date, CP.ID, CP.Price_USD as Cypto_price, OT.Price_USD as OIL_PRICE, 
                       SP.OPEN AS Stock_Price
                       from CRYPTO_PRICES CP, oiltbl OT, stocktbl SP
                       Where 
                             CP.DATE = OT.DATE AND
                             OT.DATE = SP.DATE AND
                             CP.DATE >= ? AND
                             CP.DATE <= ? AND
                            CP.ID = 'bitcoin'""" 
        df_btc=pd.read_sql(sql,con=conn,params=[Start_date,end_date])
        st.dataframe(df_btc,use_container_width=True)