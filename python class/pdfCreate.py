from fpdf import FPDF,FontFace
from PIL import ImageEnhance,Image
# from matplotlib import pyplot
# from datetime import datetime
# from fpdf import Align
normalFont = FontFace(family='Times',emphasis='',size_pt=10)
pdfCreator = FPDF()
pdfCreator.bezier()
image = Image.open(r'c:\Users\WELCOME\Downloads\Agnie LOGO1.jpg').convert('RGBA')
pdfCreator.set_page_background(background=Image.blend(Image.new('RGBA',image.size,(255,255,255,255)),image,alpha=0.5))
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
pdfCreator.image(r'c:\Users\WELCOME\Downloads\029972cf-ca2e-4eff-bb51-eba3a3e15d8c.png',20,20,170,100,alt_text='Flow Chart',title='Sample Flow')
page3 = pdfCreator.add_page()
pdfCreator.set_link(sampleLink,page=3)
pdfCreator.cell(0,10,'Sample')
pdfCreator.text_annotation(20,20,'This is a Sample Text Annotation.',title='Annotation')
pdfCreator.add_text_markup_annotation(type="Highlight",text='Markup annotation',quad_points=[20, 30,80, 30,80, 38,20, 38,])
# pdfCreator.set_encryption(owner_password='Daniel',user_password='Nikish')
pdfCreator.output('samplePdf.pdf')