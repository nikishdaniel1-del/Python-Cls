from plotly import express
from tkinter import filedialog

# file = filedialog.askopenfilename(title='Select an Excel File',filetypes=[('Excel','.xlsx')])
# print(file)
data = {'category':['India','Pakistan'],'wins':[90,10]}
express.pie(data,names='category',values='wins').show()