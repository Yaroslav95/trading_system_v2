import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def CCI(df): 
    
    df['TP'] = (df['high'] + df['low'] + df['close']) / 3 
    df['sma'] = df['TP'].rolling(20).mean()
    df['mad'] = df['TP'].rolling(20).apply(lambda x: pd.Series(x).mad())
    df['cci'] = (df['TP'] - df['sma']) / (0.015 * df['mad']) 
    
    return df['cci']

def cci_signals(prices, cci):
    
    buy_price = []
    sell_price = []
    cci_signal = []
    signal = 0
    
    lower_band = (-80)
    upper_band = 80
    
    for i in range(len(prices)):
        if cci[i-1] > lower_band and cci[i] < lower_band:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                cci_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                cci_signal.append(0)
                
        elif cci[i-1] < upper_band and cci[i] > upper_band:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                cci_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                cci_signal.append(0)
                
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            cci_signal.append(0)
            
    return buy_price, sell_price, cci_signal


def signals_plot(df, buy_price, sell_price, prod_name):

    plt.figure(figsize=(16,12))    
    ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((10,1), (6,0), rowspan = 4, colspan = 1)
    ax1.plot(df['close'], color = 'skyblue', label = 'FB')
    ax1.plot(df.index, buy_price, marker = '^', markersize = 12, linewidth = 0, label = 'BUY SIGNAL', color = 'green')
    ax1.plot(df.index, sell_price, marker = 'v', markersize = 12, linewidth = 0, label = 'SELL SIGNAL', color = 'r')
    ax1.set_title('CCI ' + prod_name)
    ax1.legend()
    ax2.plot(df['cci'], color = 'orange')
    ax2.set_title('CCI ' + prod_name)
    ax2.axhline(100, linestyle = '--', linewidth = 1, color = 'black')
    ax2.axhline(-100, linestyle = '--', linewidth = 1, color = 'black')
    plt.show()

    
def get_position(df, cci_signal):

    position = []
    for i in range(len(cci_signal)):
        if cci_signal[i] > 1:
            position.append(0)
        else:
            position.append(1)
            
    for i in range(len(df['close'])):
        if cci_signal[i] == 1:
            position[i] = 1
        elif cci_signal[i] == -1:
            position[i] = 0
        else:
            position[i] = position[i-1]
            
    cci = df['cci']
    close_price = df['close']
    cci_signal = pd.DataFrame(cci_signal).rename(columns = {0:'cci_signal'}).set_index(df.index)
    position = pd.DataFrame(position).rename(columns = {0:'cci_position'}).set_index(df.index)
    
    frames = [close_price, cci, cci_signal, position]
    strategy = pd.concat(frames, join = 'inner', axis = 1)
    
    return strategy


def get_signals(prod_name, df):
    
    print('----------------------------')
    print(prod_name)
    
    df['cci'] = CCI(df)
    df = df.dropna()
    
    buy_price, sell_price, cci_signal = cci_signals(df['close'], df['cci'])

    signals_plot(df, buy_price, sell_price, prod_name)
    strategy = get_position(df, cci_signal)
    
    return strategy