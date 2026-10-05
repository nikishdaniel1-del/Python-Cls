import pandas as pd
data = pd.read_excel('Data\EmployeeManagement.xlsx',sheet_name='Data1')
# pd.read_sql_table()
print(pd.DataFrame(data).dropna().to_dict())