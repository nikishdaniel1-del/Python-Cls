import pandas , os
from faker import Faker
from openpyxl import *
from openpyxl.worksheet.table import Table,TableStyleInfo
from openpyxl.comments import Comment
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
path = r'Data\EmployeeManagement.xlsx'
if not os.path.exists(path):
    workBook = Workbook()
    workBook[workBook.sheetnames[0]].title = 'Data1'
    workBook.save(path)
workBook = load_workbook(path)
workSheet = workBook.active
if 'Employee_Table' not in workSheet.tables.keys():
    workSheet.append(['ID','Name','Age','Languages Known','Gender','Comments'])
    genderValidater = DataValidation(type='list',formula1='"Male,Female"',allow_blank=True)
    workSheet.add_data_validation(genderValidater)
    genderValidater.add('E2:E1048576')
    table = Table(displayName='Employee_Table',ref='A1:F1')
    table.tableStyleInfo = TableStyleInfo(name='TableStyleMedium15',showFirstColumn=False,showLastColumn=False,showColumnStripes=True,showRowStripes=True)
    workSheet.add_table(table)
else:table = workSheet.tables['Employee_Table']
# workBook.create_sheet('New Next Sheet')
workSheet.title = 'First sheet'
# print(workBook.sheetnames)
# workSheet = workBook['New Next Sheet']
# print(workBook.active)
# workBook.active = workBook.index(workSheet)
# print(workBook.active)
generator = Faker()
for i in range(15):workSheet.append([generator.random_int(1,1000),generator.name(),generator.random_int(20,70),generator.language_name(),'',''])
for i in workSheet.iter_rows():print(i[0].value)
table.ref = f'A1:{get_column_letter(workSheet.max_column)}{workSheet.max_row}'
# workSheet.delete_rows(1,4)
workSheet['F2'].comment = Comment(text='This is a Comment',author='Nikish Daniel')
workBook.save(path)
workBook.close()