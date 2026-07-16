import pandas , os
from faker import Faker
from openpyxl import *
from openpyxl.worksheet.table import Table,TableStyleInfo
from openpyxl.utils import get_column_letter
path = r'Data\EmployeeManagement.xlsx'
if not os.path.exists(path):
    workBook = Workbook()
    workBook[workBook.sheetnames[0]].title = 'Data1'
    workBook.save(path)
workBook = load_workbook(path)
workSheet = workBook.active
if 'Employee_Table' not in workSheet.tables:
    workSheet.append(['ID','Name','Age','Languages Known'])
    table = Table(displayName='Employee_Table',ref='A1:D2')
    workSheet.add_table(table)
else:
    table = workSheet.tables['Employee_Table']
generator = Faker()
for i in range(15):workSheet.append([generator.random_int(1,1000),generator.name(),generator.random_int(20,65),generator.language_name()])
table.ref = f'A1:{get_column_letter(workSheet.max_column)}{workSheet.max_row}'
table.tableStyleInfo = TableStyleInfo(name='TableStyleMedium2',showFirstColumn=False,showLastColumn=False,showColumnStripes=True,showRowStripes=True)
workBook.save(path)
workBook.close()