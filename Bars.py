import os.path
import pandas as pd
from QuikPy import QuikPy  # Работа с Quik из Python через LUA скрипты QuikSharp


def SaveCandlesToFile(classCode='TQBR', secCodes=('SBER'), timeFrame='D', compression=1, qpProvider=1):
    interval = compression  # Для минутных временнЫх интервалов ставим кол-во минут
    
    if timeFrame == '4H':  # Дневной временной интервал
        interval = 240  # В минутах
    if timeFrame == '2H':  # Дневной временной интервал
        interval = 120  # В минутах
    if timeFrame == '1H':  # Дневной временной интервал
        interval = 60  # В минутах
    if timeFrame == 'D':  # Дневной временной интервал
        interval = 1440  # В минутах
    elif timeFrame == 'W':  # Недельный временной интервал
        interval = 10080  # В минутах
    elif timeFrame == 'MN':  # Месячный временной интервал
        interval = 23200  # В минутах

    print('Таймфрейм:', timeFrame)
    print('Список котировок', secCodes)

    for secCode in secCodes:  # Пробегаемся по всем тикерам
        
        print(secCode)
        
        fileName = f'.\Data\{classCode}.{secCode}_{timeFrame}.txt'
        #{compression}
        #print(fileName)
        
        isFileExists = os.path.isfile(fileName)  # Существует ли файл
        if not isFileExists:  # Если файл не существует
            print(f'Файл {fileName} не найден и будет создан')
            
        else:  # Файл существует
            
            os.remove(fileName)
            
 
        newBars = qpProvider.GetCandlesFromDataSource(classCode, secCode, interval, 0)["data"]  # Получаем все свечки
        pdBars = pd.DataFrame.from_dict(pd.json_normalize(newBars), orient='columns')  # Внутренние колонки даты/времени разворачиваем в отдельные колонки
        pdBars.rename(columns={'datetime.year': 'year', 'datetime.month': 'month', 'datetime.day': 'day',
                               'datetime.hour': 'hour', 'datetime.min': 'minute', 'datetime.sec': 'second'},
                      inplace=True)  # Чтобы получить дату/время переименовываем колонки
        print(pdBars.columns)
        pdBars.index = pd.to_datetime(pdBars[['year', 'month', 'day', 'hour', 'minute', 'second']])  # Собираем дату/время из колонок
        pdBars = pdBars[['open', 'high', 'low', 'close', 'volume']]  # Отбираем нужные колонки
        pdBars.index.name = 'datetime'  # Ставим название индекса даты/времени
        pdBars.volume = pd.to_numeric(pdBars.volume, downcast='integer')  # Объемы могут быть только целыми
        #print(f'- Первая запись в QUIK: {pdBars.index[0]}')
        #print(f'- Последняя запись в QUIK: {pdBars.index[-1]}')
        #print(f'- Кол-во записей в QUIK: {len(pdBars)}')
    
        pdBars.to_csv(fileName, sep='\t', date_format='%d.%m.%Y %H:%M')
        #print(f'- В файл {fileName} сохранено записей: {len(pdBars)}')


#if __name__ == '__main__':  # Точка входа при запуске этого скрипта

def start_func(qpProvider, timeFrame):
    
    #qpProvider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK
    # qpProvider = QuikPy(Host='192.168.0.17')  # Вызываем конструктор QuikPy с подключением к удаленному компьютеру с QUIK
    # qpProvider = QuikPy(Host='192.168.43.194')

    classCode = 'TQBR'  # Акции ММВБ
    #timeFrame = 'D'
    compression = 1
    #secCodes = ('SBER', 'GAZP', 'YNDX', 'ROSN', 'OZON', 'SBERP', 'TCSG', 'NVTK', 'POLY', 'SIBN')
    
    secCodes = ('SBER', 'GAZP', 'ROSN')
    
    #secCodes = ('SBER', 'GMKN', 'GAZP', 'LKOH', 'TATN', 'YNDX', 'TCSG', 'ROSN', 'NVTK', 'MVID',
    #            'CHMF', 'POLY', 'OZON', 'ALRS', 'MAIL', 'MTSS', 'NLMK', 'MAGN', 'PLZL', 'MGNT',
    #            'MOEX', 'TRMK', 'RUAL', 'SNGS', 'AFKS', 'SBERP', 'SIBN', 'FIVE', 'SNGSP', 'AFLT',
    #            'IRAO', 'PHOR', 'TATNP', 'VTBR', 'QIWI', 'CBOM', 'FEES', 'BELU', 'TRNFP', 'FIXP')  # TOP 40 акций ММВБ

    SaveCandlesToFile(classCode, secCodes, timeFrame, compression, qpProvider)  # По умолчанию получаем дневные бары
    
    classCode = 'TQTF'
    secCodes = ('VTBX',)
    SaveCandlesToFile(classCode, secCodes, timeFrame, compression, qpProvider)
    
    
    classCode = 'TQTD'
    secCodes = ('VTBA',)
    SaveCandlesToFile(classCode, secCodes, timeFrame, compression, qpProvider)
    
    #classCode = 'SPBFUT'  # Фьючерсы РТС
    #secCodes = ('SiZ1', 'RIZ1')  # Формат фьючерса: <Тикер><Месяц экспирации><Последняя цифра года> Месяц экспирации: 3-H, 6-M, 9-U, 12-Z
    #SaveCandlesToFile(classCode, secCodes)  # По умолчанию получаем дневные бары

    #timeFrame = 'М'  # Временной интервал: 'M'-Минуты, 'D'-дни, 'W'-недели, 'MN'-месяцы
    #compression = 240  # Кол-во минут для минутного графика. Для остальных = 1
    #SaveCandlesToFile(classCode, secCodes, timeFrame, compression)  # Получаем 5-и минутные бары

    #qpProvider.CloseConnectionAndThread()  # Перед выходом закрываем соединение и поток QuikPy из любого экземпляра
