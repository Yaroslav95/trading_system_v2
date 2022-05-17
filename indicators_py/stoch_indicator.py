import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def get_stoch_osc(high, low, close, k_lookback, d_lookback):
    
    lowest_low = low.rolling(k_lookback).min()
    highest_high = high.rolling(k_lookback).max()
    k_line = ((close - lowest_low) / (highest_high - lowest_low)) * 100
    d_line = k_line.rolling(d_lookback).mean()
    
    return k_line, d_line

def stoch_signals(prices, k, d):    
    
    buy_price = []
    sell_price = []
    stoch_signal = []
    signal = 0

    for i in range(len(prices)):
        if k[i] < 20 and d[i] < 20 and k[i] < d[i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                stoch_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                stoch_signal.append(0)
        elif k[i] > 80 and d[i] > 80 and k[i] > d[i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                stoch_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                stoch_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            stoch_signal.append(0)
            
    return buy_price, sell_price, stoch_signal

    
def signals_plot(df, buy_price, sell_price, prod_name):

    plt.figure(figsize=(16,12))     
    ax1 = plt.subplot2grid((9, 1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((9, 1), (6,0), rowspan = 3, colspan = 1)
    ax1.plot(df['close'], color = 'skyblue', label = 'NFLX')
    ax1.plot(df.index, buy_price, marker = '^', color = 'green', markersize = 10, label = 'BUY SIGNAL', linewidth = 0)
    ax1.plot(df.index, sell_price, marker = 'v', color = 'r', markersize = 10, label = 'SELL SIGNAL', linewidth = 0)
    ax1.legend(loc = 'upper left')
    ax1.set_title('STOCHASTIC ' + prod_name)
    ax2.plot(df['%k'], color = 'deepskyblue', linewidth = 1.5, label = '%K')
    ax2.plot(df['%d'], color = 'orange', linewidth = 1.5, label = '%D')
    ax2.axhline(80, color = 'black', linewidth = 1, linestyle = '--')
    ax2.axhline(20, color = 'black', linewidth = 1, linestyle = '--')
    ax2.set_title('STOCHASTIC ' + prod_name)
    ax2.legend()
    plt.show()
    
    
def get_position(df, stoch_signal):
    
    position = []
    for i in range(len(stoch_signal)):
        if stoch_signal[i] > 1:
            position.append(0)
        else:
            position.append(1)
            
    for i in range(len(df['close'])):
        if stoch_signal[i] == 1:
            position[i] = 1
        elif stoch_signal[i] == -1:
            position[i] = 0
        else:
            position[i] = position[i-1]
            
    k = df['%k']
    d = df['%d']
    close_price = df['close']
    stoch_signal = pd.DataFrame(stoch_signal).rename(columns = {0:'stoch_signal'}).set_index(df.index)
    position = pd.DataFrame(position).rename(columns = {0:'stoch_position'}).set_index(df.index)
    
    frames = [close_price, k, d, stoch_signal, position]
    strategy = pd.concat(frames, join = 'inner', axis = 1)
    
    return strategy


def get_signals(prod_name, df):
    
    print('----------------------------')
    print(prod_name)
    
    df['%k'], df['%d'] = get_stoch_osc(df['high'], df['low'], df['close'], 14, 3)
    df = df.dropna()
    
    buy_price, sell_price, stoch_signal = stoch_signals(df['close'], df['%k'], df['%d'])

    signals_plot(df, buy_price, sell_price, prod_name)
    
    strategy = get_position(df, stoch_signal)
    
    return strategy