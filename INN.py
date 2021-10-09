"""
    Данный модуль реализован в рамках тестового задания.
    Модуль позволяет получить информацию о юр.лице,
    формирует выводы о благонадежности компании по данным юр лицам

    Тест 1 -  Balance_test
              Банас отрицательный - тест не пройдет
              Банас положительный - тест пройдет
    Тест 2  - Revenue_test
              Выручка отрицательная - тест не пройдет
              Выручка положительная - тетс пройден
              
    Total_test - Пройдет когда пройдены Тест 1 и 2,
                 в ином случае тест не пройден

    На вход модуля принимается строка из 10 цифр, формат str
    
    На выходе модуль выдет объект DataFrame со столбцами
    [inn, Status, Balance, Revenue, Tax, Balance_test, Revenue_test, Total_test]
    где,
    
    inn - ИНН компании
    Status - Статус компании: Действует/ Не действует
    Balance
    Revenue - Выручка компани за последний год
    Tax - размер уплаченных налогов
    Balance_test - результат Теста 1: True/False
    Revenue_test - результат Теста 2: True/False
    Total_test - итоговый результат по обоим тестам: True/False
    
"""


import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

class InnParser:
 
    def __init__(self, inn):
        
        self.inn = inn
    
    def company_test(self):
        
        # Создаем объект dataFrame в котором будет находиться вся финальная информация
        df = pd.DataFrame()   
        # Начальный индекс датафрейма
        ind = 0

        try:
            for inn_i in self.inn:
                print(inn_i)
                # Был выбран ресурс https://vbankcenter.ru
                url = 'https://vbankcenter.ru/contragent/search?searchStr=' + inn_i + '&type=LEGAL'
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Получаем статус юлица Действует/Не действует
                status = soup.findAll('gweb-partner-status-viewer', class_ = 'lg:hidden') 
                # Получаем ссылку на страницу с расширенной информацией о юрлице
                url_link = soup.findAll('a', class_ = 'overlap text-blue')             

                sts_activ = []
                hrf_activ = []
                
                # Так как бывают составные ИНН через /, то  обходим выдачу юрлиц циклом
                for link, stat in zip(url_link, status):
                    sts_activ.append(stat.text[:-1])
                    hrf_activ.append('https://vbankcenter.ru' + link.get('href'))
                
                # Заносим первые данные ИНН и Статус компании в наш датафрейм
                df.loc[ind,'inn'] = inn_i
                df.loc[ind,'Status'] = sts_activ
                
                # Открываем ссылку с детальной информацией о юрлице
                url_detail = hrf_activ[0]
                response = requests.get(url_detail)
                soup = BeautifulSoup(response.text, 'lxml')
                
                # парсим блок с расширенными данными
                data_statistic = soup.find('gweb-finanstat', 'gweb-finanstat col-span-full mt-5 bg-white font-normal')
                # Фин показатели юрлица
                data_profit  = data_statistic.findAll('gweb-finanstat-item', class_ = 'gweb-finanstat-item py-4 px-7 mb-0 bg-white')  
                
                # Пробегаемся по финпоказателям балансу, Выручке и Налогам внутри модуля
                for i in data_profit :
                    data = i.find('span', 'statistic-number text-base')
                    if data is not None:
                        header = i.find('h6', 'statistic-name pb-2 mb-0 text-black whitespace-nowrap increase').text[:-1]
                        if header == ' Баланс, ₽':
                            df.loc[ind,'Balance'] = float(data.text.replace(',','.'))
                            
                        if header == ' Выручка, ₽':
                            df.loc[ind,'Revenue'] = float(data.text.replace(',','.'))
                            
                        if header == ' Налоги, ₽':
                            df.loc[ind,'Tax'] = float(data.text.replace(',','.'))
                
                ++ind
            
            # Формируем столбцы с результатами тестов
            df['Balance_test'] = df.Balance > 0
            df['Revenue_test'] = df.Revenue > 0
            df['Total_test'] = df.Balance_test & df.Revenue_test
 
        except Exception:
            print('Что-то пошлоне так')
        
        finally:
            print('Done')
            
        return(df)



