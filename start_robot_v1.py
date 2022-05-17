import pandas as pd
import numpy as np
from datetime import datetime
import os
import Bars
import new_transaction
import macd_indicator
from QuikPy import QuikPy  # Работа с Quik из Python через LUA скрипты QuikSharp

print('ddddd')
qpProvider = QuikPy()
print(qpProvider)

Bars.start_func(qpProvider, '1H')
print('!!!')
new_transaction.start_func(qpProvider, 'TQBR', 'SBER', 'NEW_ORDER', 'BUY', 0, 1)
print('!!!')
new_transaction.start_func(qpProvider, 'TQBR', 'SBER', 'NEW_STOP_ORDER', 'SELL', 143.6, 1)
print('!!!')

qpProvider.CloseConnectionAndThread()