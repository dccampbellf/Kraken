import requests
import pandas as pd
from datetime import date, datetime, time, timedelta
import urllib.parse
import hmac
import base64
from json import JSONDecodeError
import krakenex
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import time
import random


class choice:

#Variables
    def __init__(self, time_span=None,coin_choice=None):
        self.time_span=time_span
        self.coin_choice=coin_choice

#Methods
def get_span(span):
        
    if span=='day':
        delta=datetime.now()-timedelta(days=1)
        timestamp=(datetime.timestamp(delta))
        days=1

    elif span=='week':
        delta=datetime.now()-timedelta(days=7)
        timestamp=(datetime.timestamp(delta))
        days=7

    elif span=='month':
        delta=datetime.now()-timedelta(days=30)
        timestamp=(datetime.timestamp(delta))
        days=30

    elif span=='six_months':
        delta=datetime.now()-timedelta(days=182.5)
        timestamp=(datetime.timestamp(delta))
        days=182.5

    elif span=='one_year':
        delta=datetime.now()-timedelta(days=365)
        timestamp=(datetime.timestamp(delta))
        days=365
        
    else:
        delta="timestamp span function is not working"

    return(delta, days)

def main():   
    
    st.markdown("Welcome, please choose a coin pair")

    global coin_pair
    coin_pair=st.selectbox('Coin/Pair',['XXBTZUSD','ZRXXBT','BCHUSD',
    '1INCHEUR','1INCHUSD','AAVEAUD','AAVEETH','AAVEEUR','AAVEGBP','AAVEUSD','AAVEXBT','ADAAUD',
    'ADAETH','ADAEUR','ADAGBP','ADAUSD','ADAUSDT','ADAXBT','ALGOETH','ALGOEUR'])
        
    global time_frame_input
    time_frame_input=st.selectbox('Time',['day','week','month','six_months','one_year']) 
    
    df = load_data()
    ###figure this out
    
    #x='time_frame_selection_'+str(datetime.now())
    #x=choice()
    #x.coin_choice=coin_pair
    #x.time_span=time_frame_input
    
    #x_axis='value_fiat_currency'
    #y_axis='date'

    #visualize_data(df, x='date', y='value_fiat_currency')

    st.title("Data Exploration")

    x_axis = 'date'
    y_axis = 'value_fiat_currency'

    visualize_data(df, x_axis, y_axis)


def load_data():
    
    start_time=get_span(time_frame_input)[0]
    end_time=datetime.now()-timedelta(hours=1)
    new_since=start_time


    df=pd.DataFrame(columns=['value_fiat_currency','volume_ecoin','timestamp','buy_sell','limit_market','misc','date'])
    
    base_url = 'https://api.kraken.com/0/public/Trades?pair={}&since={}'
    url=base_url.format(coin_pair,datetime.timestamp(start_time))
    resp=requests.get(url)
    coin_trans= resp.json()['result'][coin_pair]
        
    df=pd.DataFrame(coin_trans, columns=['value_fiat_currency', 'volume_ecoin','timestamp','buy_sell','limit_market','misc'])
    df['date'] = df['timestamp'].map(datetime.fromtimestamp) 

    while new_since< end_time:     

        new_since=df['date'].iloc[-1]
        base_url = 'https://api.kraken.com/0/public/Trades?pair={}&since={}'
        url=base_url.format(coin_pair,new_since)
        resp=requests.get(url)
        coin_trans= resp.json()['result'][coin_pair]

        dfx=pd.DataFrame(coin_trans, columns=['value_fiat_currency', 'volume_ecoin','timestamp','buy_sell','limit_market','misc'])
        dfx['date'] = dfx['timestamp'].map(datetime.fromtimestamp)
 #      dfx['vwap'] = (int(dfx.volume_ecoin)*float(df.value_fiat_currency.max())+float(df.value_fiat_currency.min()))/2).cumsum() / float(df.volume_ecoin).cumsum())



        df.append(dfx)

        time.sleep(random.randint(1, 4))
        return(df)
 #   return(df)
    

def visualize_data(df, x_axis, y_axis):
    
    graph = go.Figure(px.line(df, x_axis, y_axis))
    st.plotly_chart(graph)
    st.write()
    st.write(df)

if __name__ == "__main__":
    main()
