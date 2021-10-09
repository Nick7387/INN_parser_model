from INN import InnParser
import pandas as pd

inn_excel = pd.read_excel('ИНН.xlsx', index_col=0)  
inn_raw = inn_excel.index.tolist()

#inn_raw = [7736207543, 23, 1661056318, 111111111111111, 5752030868, 6732161906]

# составляем новый список ИНН с корректными значениями - ИНН состоит из 10 цифр
# и приводим их к типу str для подставновки в url
inn = [str(x) for x in inn_raw if len(str(x)) == 10]

innparser = InnParser(inn)
test = innparser.company_test()

test.to_excel("test_inn.xlsx") 