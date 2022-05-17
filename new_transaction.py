from QuikPy import QuikPy  # Работа с Quik из Python через LUA скрипты QuikSharp
import random


def OnTransReply(data):
    """Обработчик события ответа на транзакцию пользователя"""
    print('OnTransReply')
    print(data['data'])  # Печатаем полученные данные

def OnOrder(data):
    """Обработчик события получения новой / изменения существующей заявки"""
    print('OnOrder')
    print(data['data'])  # Печатаем полученные данные

def OnTrade(data):
    """Обработчик события получения новой / изменения существующей сделки
    Не вызывается при закрытии сделки
    """
    print('OnTrade')
    print(data['data'])  # Печатаем полученные данные

def OnFuturesClientHolding(data):
    """Обработчик события изменения позиции по срочному рынку"""
    print('OnFuturesClientHolding')
    print(data['data'])  # Печатаем полученные данные

def OnDepoLimit(data):
    """Обработчик события изменения позиции по инструментам"""
    print('OnDepoLimit')
    print(data['data'])  # Печатаем полученные данные

def OnDepoLimitDelete(data):
    """Обработчик события удаления позиции по инструментам"""
    print('OnDepoLimitDelete')
    print(data['data'])  # Печатаем полученные данные

#if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    
def start_func(qpProvider, classCode, secCode, action, operation, price, cnt_lots, orderNum=0):
    
    #if _host == 'auto':
    #    qpProvider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK
    #else:
    #    qpProvider = QuikPy(Host=_host)
    
    #qpProvider = QuikPy(Host='192.168.0.17')  # Вызываем конструктор QuikPy с подключением к удаленному компьютеру с QUIK
    qpProvider.OnTransReply = OnTransReply  # Ответ на транзакцию пользователя. Если транзакция выполняется из QUIK, то не вызывается
    qpProvider.OnOrder = OnOrder  # Получение новой / изменение существующей заявки
    qpProvider.OnTrade = OnTrade  # Получение новой / изменение существующей сделки
    qpProvider.OnFuturesClientHolding = OnFuturesClientHolding  # Изменение позиции по срочному рынку
    qpProvider.OnDepoLimit = OnDepoLimit  # Изменение позиции по инструментам
    qpProvider.OnDepoLimitDelete = OnDepoLimitDelete  # Удаление позиции по инструментам
    
    TransId = random.randint(0, 100000)
    #quantity = 1  # Кол-во в лотах
     

    ## Покупка
    if (action=='NEW_ORDER') & (operation=='BUY'):

        transaction = {  # Все значения должны передаваться в виде строк
            'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
            'CLIENT_CODE': '10NY8F',  # Код клиента. Для фьючерсов его нет #10NY8F
            'ACCOUNT': 'L01-00000F00',  # Счет №HL1710270034 #MC0003300001 #30601810663390554769
            'ACTION': 'NEW_ORDER',  # Тип заявки: Новая лимитная/рыночная заявка
            'CLASSCODE': classCode,  # Код площадки
            'SECCODE': secCode,  # Код тикера
            'OPERATION': 'B',  # B = покупка, S = продажа
            'PRICE': str(0),  # Цена исполнения. Для рыночных фьючерсных заявок наихудшая цена в зависимости от направления. Для остальных рыночных заявок цена = 0
            'QUANTITY': str(cnt_lots),  # Кол-во в лотах
            'TYPE': 'M'}  # L = лимитная заявка (по умолчанию), M = рыночная заявка
        
        qpProvider.SendTransaction(transaction, TransId)  
        print('Заявка на покупку отправлена')
        #print(f'Новая лимитная/рыночная заявка отправлена на рынок: {qpProvider.SendTransaction(transaction)}') #["data"]

    
    ## Продажа
    if (action=='NEW_ORDER') & (operation=='SELL'):

        transaction = {  # Все значения должны передаваться в виде строк
            'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
            'CLIENT_CODE': '10NY8F',  # Код клиента. Для фьючерсов его нет #10NY8F
            'ACCOUNT': 'L01-00000F00',  # Счет №HL1710270034 #MC0003300001 #30601810663390554769
            'ACTION': 'NEW_ORDER',  # Тип заявки: Новая лимитная/рыночная заявка
            'CLASSCODE': classCode,  # Код площадки
            'SECCODE': secCode,  # Код тикера
            'OPERATION': 'S',  # B = покупка, S = продажа
            'PRICE': str(0),  # Цена исполнения. Для рыночных фьючерсных заявок наихудшая цена в зависимости от направления. Для остальных рыночных заявок цена = 0
            'QUANTITY': str(cnt_lots),  # Кол-во в лотах
            'TYPE': 'M'}  # L = лимитная заявка (по умолчанию), M = рыночная заявка
        
        qpProvider.SendTransaction(transaction, TransId)
        print('Заявка на продажу отправлена')

    # Новая стоп заявка
    if (action=='NEW_STOP_ORDER') & (operation=='SELL'):
    
        #StopSteps = 10  # Размер проскальзывания в шагах цены
        #slippage = float(qpProvider.GetSecurityInfo(classCode, secCode)['data']['min_price_step']) * StopSteps  # Размер проскальзывания в деньгах
        #print(slippage)
        #if slippage.is_integer():  # Целое значение проскальзывания мы должны отправлять без десятичных знаков
        #    slippage = int(slippage)  # поэтому, приводим такое проскальзывание к целому числу
            
        stop_price = round(price, 2)
        
        #stop_price = round(price, 2)
        print('Стоп-лосс по цене', stop_price)
            
        transaction = {  # Все значения должны передаваться в виде строк
            'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
            'CLIENT_CODE': '10NY8F',  # Код клиента. Для фьючерсов его нет
            'ACCOUNT': 'L01-00000F00',  # Счет
            'ACTION': 'NEW_STOP_ORDER',  # Тип заявки: Новая стоп заявка
            'CLASSCODE': classCode,  # Код площадки
            'SECCODE': secCode,  # Код тикера
            'OPERATION': 'S',  # B = покупка, S = продажа
            'PRICE': str(stop_price),  # Цена исполнения
            'QUANTITY': str(cnt_lots),  # Кол-во в лотах
            'STOPPRICE': str(stop_price),  # Стоп цена исполнения (price - slippage)
            'EXPIRY_DATE': 'GTC'}  # Срок действия до отмены
        
        qpProvider.SendTransaction(transaction, TransId) 
        #print(f'Новая стоп заявка отправлена на рынок: {qpProvider.SendTransaction(transaction)["data"]}')
        print('Заявка на стоп-лосс отправлена')
        
        
   ####
        #transaction = {  # Все значения должны передаваться в виде строк
        #    'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
        #    'CLIENT_CODE': '10NY8F',  # Код клиента. Для фьючерсов его нет
        #    'ACCOUNT': 'L01-00000F00',  # Счет
        #    'ACTION': 'NEW_STOP_ORDER',  # Тип заявки: Новая стоп заявка
        #    'CLASSCODE': classCode,  # Код площадки
        #    'SECCODE': secCode,  # Код тикера
        #    'OPERATION': 'S',  # B = покупка, S = продажа
        #    'PRICE': str(price),  # Цена исполнения
        #    'QUANTITY': str(cnt_lots),  # Кол-во в лотах
        #    'STOPPRICE': str(0),  # Стоп цена исполнения (price - slippage)
        #    'TYPE' : 'М', # 
        #    'STOP_ORDER_KIND' : 'TAKE_PROFIT_AND_STOP_LIMIT_ORDER',
        #    'STOPPRICE2': str(stop_price),
        #    'EXPIRY_DATE': 'GTC'}  # Срок действия до отмены
    
        # Снятие заявки 
    #TransId = random.randint(0, 100000)
    #print(TransId)
    ## Удаление существующей лимитной заявки
    #orderNum = 30870753159  # 19-и значный номер заявки
    #transaction = {
    #    'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
    #    'ACTION': 'KILL_ORDER',  # Тип заявки: Удаление существующей заявки
    #    'CLASSCODE': classCode,  # Код площадки
    #    'SECCODE': secCode,  # Код тикера
    #    'ORDER_KEY': str(orderNum)}  # Номер заявки
    #print(f'Удаление заявки отправлено на рынок: {qpProvider.SendTransaction(transaction)["data"]}')
    
    # Удаление существующей стоп заявки
    if (action=='KILL_STOP_ORDER') & (operation=='KILL'): #orderNum
     
         transaction = {
             'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
             'ACTION': 'KILL_STOP_ORDER',  # Тип заявки: Удаление существующей заявки
             'CLASSCODE': classCode,  # Код площадки
             'SECCODE': secCode,  # Код тикера
             'STOP_ORDER_KEY': str(orderNum)}  # Номер заявки
         print(f'Удаление стоп заявки отправлено на рынок: {qpProvider.SendTransaction(transaction)["data"]}')
            
            
    print('Номер транзакции:', TransId)  
    print(transaction)
    print('------------')
    #input('Enter - отмена')  # Ждем исполнение заявки
    #qpProvider.CloseConnectionAndThread()  # Перед выходом закрываем соединение и поток QuikPy из любого экземпляра
    
 
