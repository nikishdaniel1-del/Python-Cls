from fpdf import FPDF
pdfCreator = FPDF()
pdfCreator.add_page()
pdfCreator.line(10,10,200,10)
pdfCreator.set_font('Times','B',18)
pdfCreator.cell(10,10,'Hi Welcome to FPDF.')
pdfCreator.output('samplePdf.pdf')