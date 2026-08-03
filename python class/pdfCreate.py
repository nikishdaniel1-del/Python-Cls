from fpdf import FPDF,FontFace
from datetime import datetime
# from fpdf import Align
normalFont = FontFace(family='Times',emphasis='',size_pt=10)
pdfCreator = FPDF()
pdfCreator.set_title('Sample PDF')
pdfCreator.add_page()
pdfCreator.line(10,10,200,10)
pdfCreator.set_font('Times','B',18)
pdfCreator.cell(w=0,h=10,text='Hi Welcome to FPDF.',align='C',center=True)
pdfCreator.ln(10)
data = [['Name','Age'],['Daniel',22],['Ram',18],['Ravi',30]]
with pdfCreator.table() as tab:
    for i in data:
        fonts = FontFace(family='Times',emphasis='I',size_pt=14) if i[0]=='Name' else normalFont
        currentRow = tab.row()
        currentRow.cell(i[0],style=fonts);currentRow.cell(str(i[1]),style=fonts)
pdfCreator.cell(0,10,'Google',link='https:\\google.com')
# pdfCreator.multi_cell(w=0,h=10,markdown=True,text='**bold** ~~strike~~')
# pdfCreator.set_author('Nikish Daniel')
pdfCreator.ln(10)
introductionLink = pdfCreator.add_link()
pdfCreator.cell(0,10,'Introduction',link=introductionLink)
pdfCreator.ln(10)
sampleLink = pdfCreator.add_link()
pdfCreator.cell(0,10,'Sample',link=sampleLink)
pdfCreator.add_page()
pdfCreator.set_link(introductionLink,page=2)
pdfCreator.cell(0,10,'Introduction')
page3 = pdfCreator.add_page()
pdfCreator.set_link(sampleLink,page=3)
pdfCreator.cell(0,10,'Sample')
# pdfCreator.set_encryption(owner_password='Daniel',user_password='Nikish')
pdfCreator.output('samplePdf.pdf')