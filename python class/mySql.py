from mysql.connector import connect,Error

connection = connect(host='127.0.0.1',user='root',password='Nikish@2003',database='javacls')
currentCursor = connection.cursor()
# currentCursor.execute(f'select *  from employee where empName = "{input()}"')
currentCursor.execute('insert into employee(empName,salary) values("%s",%2f)'%('Ram',20000.50,))
connection.commit()
currentCursor.execute('select *  from employee where empName = %s',('Ram',))
currentCursor.execute('update employee set salary = %2f where empName = %s'%(18000.00,'Ram'))
connection.commit()
currentCursor.execute('delete from employee where empid = %s',(1,))
connection.commit()
print(currentCursor.fetchall())
connection.close()