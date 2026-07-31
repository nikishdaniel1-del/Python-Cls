from fpdf import FPDF,FontFace
from datetime import datetime
# from fpdf import Align
pdfCreator = FPDF()
pdfCreator.add_page()
pdfCreator.line(10,10,200,10)
pdfCreator.set_font('Times','B',18)
pdfCreator.cell(w=0,h=10,text='Hi Welcome to FPDF.',align='C',center=True)
pdfCreator.ln(10)
data = [['Name','Age'],['Daniel',22],['Ram',18],['Ravi',30]]
with pdfCreator.table() as tab:
    for i in data:
        if i[0]=='Name':fonts = FontFace(family='Times',emphasis='I',size_pt=14)
        else:fonts = FontFace(family='Times',emphasis='',size_pt=10)
        currentRow = tab.row()
        currentRow.cell(i[0],style=fonts);currentRow.cell(str(i[1]),style=fonts)
pdfCreator.cell(0,10,'Google',link='https:\\google.com')
# pdfCreator.multi_cell(w=0,h=10,markdown=True,text='**bold** ~~strike~~')
pdfCreator.set_author('Nikish Daniel')
pdfCreator.add_page()
# pdfCreator.set_creation_date(datetime(2026,7,31))
# pdfCreator.set_encryption(owner_password='Daniel',user_password='Nikish')
pdfCreator.output('samplePdf.pdf')