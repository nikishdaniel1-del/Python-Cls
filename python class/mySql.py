from mysql.connector import connect,Error

connection = connect(host='127.0.0.1',user='root',password='Nikish@2003',database='javacls')
currentCursor = connection.cursor()
currentCursor.execute(f'select *  from employee where empName = "{input()}"')
print(currentCursor.fetchall())
print(currentCursor.fetchone())
connection.close()