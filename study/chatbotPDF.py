from tkinter.filedialog import askopenfilenames
import numpy
from transformers import pipeline

files = askopenfilenames(title="Select PDF(s) to Feed",filetypes=[('All Files','*.*'),('PDF files','.pdf')])
for i in files:print(i)