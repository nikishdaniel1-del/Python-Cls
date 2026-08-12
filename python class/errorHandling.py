try:
    number1 , number2 = int(input()) , int(input())
    result = number1/number2
# except ZeroDivisionError as zero:
#     print(f'{zero} error')
except ZeroDivisionError:
    print("The input values can't be zero")
except ValueError:
    print('The input only takes integer values')
except Exception as error:
    print(type(error).__name__)
else:
    print(result)
finally:
    print('Program Ended')