import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def get_macd(price, slow, fast, smooth):
    
    exp1 = price.ewm(span = fast, adjust = False).mean()
    exp2 = price.ewm(span = slow, adjust = False).mean()
    macd = pd.DataFrame(exp1 - exp2).rename(columns = {'close':'macd'})
    signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
    frames =  [macd, signal, hist]
    df = pd.concat(frames, join = 'inner', axis = 1)
    
    return df

def plot_macd(prices, macd, signal, hist):
    
    ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)

    ax1.plot(prices)
    ax2.plot(macd, color = 'grey', linewidth = 1.5, label = 'MACD')
    ax2.plot(signal, color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')

    for i in range(len(prices)):
        if str(hist[i])[0] == '-':
            ax2.bar(prices.index[i], hist[i], color = '#ef5350')
        else:
            ax2.bar(prices.index[i], hist[i], color = '#26a69a')

    plt.legend(loc = 'lower right')
    

def implement_macd_strategy(prices, data): 
    
    buy_price = []
    sell_price = []
    macd_signal = []
    signal = 0

    for i in range(len(data)):
        if (data['macd'][i] > data['signal'][i]) & (data['cci'][i] < -50):
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        elif (data['macd'][i] < data['signal'][i]) & (data['cci'][i] > 0):
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            macd_signal.append(0)
            
    return buy_price, sell_price, macd_signal


def signals_plot(df, buy_price, sell_price, macd_signal, prod_name):

    plt.figure(figsize=(16,12))
    ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
    ax2 = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)
    
    ax1.plot(df.index, df['close'], color = 'skyblue', linewidth = 2, label = 'GOOGL')
    ax1.plot(df.index, buy_price, marker = '^', color = 'green', markersize = 10, label = 'BUY SIGNAL', linewidth = 0)
    ax1.plot(df.index, sell_price, marker = 'v', color = 'r', markersize = 10, label = 'SELL SIGNAL', linewidth = 0)
    ax1.legend()
    ax1.set_title(prod_name + 'MACD SIGNALS')
    ax2.plot(df['macd'], color = 'grey', linewidth = 1.5, label = 'MACD')
    ax2.plot(df['signal'], color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')
    
    for i in range(len(df)):
        if str(df['hist'][i])[0] == '-':
            ax2.bar(i, df['hist'][i], color = '#ef5350') #df.index[i]
        else:
            ax2.bar(i, df['hist'][i], color = '#26a69a')
            
    plt.legend(loc = 'lower right')
    plt.show()
    
    
def get_position(df, buy_price, sell_price, macd_signal):
    
    position = []
    for i in range(len(macd_signal)):
        if macd_signal[i] > 1:
            position.append(0)
        else:
            position.append(1)
            
    for i in range(len(df['close'])):
        if macd_signal[i] == 1:
            position[i] = 1
        elif macd_signal[i] == -1:
            position[i] = 0
        else:
            position[i] = position[i-1]
            
    macd = df['macd']
    signal = df['signal']
    datetime = df['datetime']
    close_price = df['close']
    macd_signal = pd.DataFrame(macd_signal).rename(columns = {0:'macd_signal'}).set_index(df.index)
    position = pd.DataFrame(position).rename(columns = {0:'macd_position'}).set_index(df.index)
    
    frames = [datetime, close_price, macd, signal, macd_signal, position]
    strategy = pd.concat(frames, join = 'inner', axis = 1)
    
    return strategy    

    
def get_signals(prod_name ,df):
    
    df = pd.concat([df, get_macd(df['close'], 26, 12, 9)], axis=1)
    #plot_macd(df['close'], df['macd'], df['signal'], df['hist'])
    buy_price, sell_price, macd_signal = implement_macd_strategy(df['close'], df)
    signals_plot(df, buy_price, sell_price, macd_signal, prod_name)
    strategy = get_position(df, buy_price, sell_price, macd_signal)
    
    return strategy.set_index('datetime')