import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def sma(price, period):
    sma = price.rolling(period).mean()
    return sma

def ao(price, period1, period2):
    median = price.rolling(2).median()
    short = sma(median, period1)
    long = sma(median, period2)
    ao = short - long
    ao_df = pd.DataFrame(ao).rename(columns = {'Close':'ao'})
    return ao_df

#def implement_ao_crossover(price, ao):
#    buy_price = []
#    sell_price = []
#    ao_signal = []
#    signal = 0
#    
#    for i in range(len(ao)):
#        if ao[i] > 0 and ao[i-1] < 0:
#            if signal != 1:
#                buy_price.append(price[i])
#                sell_price.append(np.nan)
#                signal = 1
#                ao_signal.append(signal)
#            else:
#                buy_price.append(np.nan)
#                sell_price.append(np.nan)
#                ao_signal.append(0)
#        elif ao[i] < 0 and ao[i-1] > 0:
#            if signal != -1:
#                buy_price.append(np.nan)
#                sell_price.append(price[i])
#                signal = -1
#                ao_signal.append(signal)
#            else:
#                buy_price.append(np.nan)
#                sell_price.append(np.nan)
#                ao_signal.append(0)
#        else:
#            buy_price.append(np.nan)
#            sell_price.append(np.nan)
#            ao_signal.append(0)
#            
#    return buy_price, sell_price, ao_signal

def ao_signals(price, ao):
    buy_price = []
    sell_price = []
    ao_signal = []
    signal = 0
    
    for i in range(2, len(ao)):
        # На покупку
        if (ao[i] > 0 and ao[i-1] < 0) | (ao[i]>0 and ao[i-1]>0 and ao[i]>ao[i-1] and ao[i-1]<ao[i-2]):
            if signal != 1:
                buy_price.append(price[i])
                sell_price.append(np.nan)
                signal = 1
                ao_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ao_signal.append(0)
        # На продажу
        elif (ao[i] < 0 and ao[i-1] > 0) | (ao[i]<0 and ao[i-1]<0 and ao[i]<ao[i-1] and ao[i-1]>ao[i-2]):
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(price[i])
                signal = -1
                ao_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ao_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            ao_signal.append(0)
            
    return buy_price, sell_price, ao_signal

def signals_plot(df, buy_price, sell_price, ao_signal, prod_name):

    plt.figure(figsize=(16,12))
    ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 5, colspan = 1)
    ax1.plot(df.index, df['close'], label = 'BTC', color = 'skyblue')
    ax1.plot(df.index, buy_price, marker = '^', markersize = 12, color = '#26a69a', linewidth = 0, label = 'BUY SIGNAL')
    ax1.plot(df.index, sell_price, marker = 'v', markersize = 12, color = '#f44336', linewidth = 0, label = 'SELL SIGNAL')
    ax1.legend()
    ax1.set_title(prod_name + ' SIGNALS')
    ax2 = plt.subplot2grid((10,1), (6,0), rowspan = 4, colspan = 1)
    for i in range(1, len(df)):
        if df['ao'][i-1] > df['ao'][i]:
            ax2.bar(i, df['ao'][i], color = '#f44336') #df.index[i]
        else:
            ax2.bar(i, df['ao'][i], color = '#26a69a')
    ax2.set_title('AWESOME OSCILLATOR 5,34')
    plt.show()


def get_position(df, buy_price, sell_price, ao_signal):
    
    position = []
    for i in range(len(ao_signal)):
        if ao_signal[i] > 1:
            position.append(0)
        else:
            position.append(1)
            
    for i in range(len(df['close'])):
        if ao_signal[i] == 1:
            position[i] = 1
        elif ao_signal[i] == -1:
            position[i] = 0
        else:
            position[i] = position[i-1]
            
    ao = df['ao']
    close_price = df['close']
    ao_signal = pd.DataFrame(ao_signal).rename(columns = {0:'ao_signal'}).set_index(df.index)
    position = pd.DataFrame(position).rename(columns = {0:'ao_position'}).set_index(df.index)
    
    frames = [close_price, ao, ao_signal, position]
    strategy = pd.concat(frames, join = 'inner', axis = 1)
    
    return strategy


def get_signals(prod_name, df):
    
    print('----------------------------')
    print(prod_name)
    
    df['ao'] = ao(df['close'], 5, 34)
    df = df.dropna()
    
    buy_price, sell_price, ao_signal = ao_signals(df['close'], df['ao'])
    
    signals_plot(df[2:], buy_price, sell_price, ao_signal, prod_name)
    
    strategy = get_position(df[2:], buy_price, sell_price, ao_signal)
    
    return strategy