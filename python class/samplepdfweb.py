from nicegui import ui,app
from fpdf import FPDF
import time

@ui.page('/home')
def main():
    ui.add_css('''body {background-image:url("/static/Original.webp");background-size: cover;background-position:top center;}''')
    def generatePDF():
        pdfPath = "pdfs/output.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0,10,text.value)
        pdf.output(pdfPath)
        pdfViewer.set_content(f''' <iframe src="/pdfs/output.pdf?v={time.time_ns()}" style=" width: 100%; height: 100%; border: none; "> </iframe> ''')
    def add(operation):
        with widgetsSaved:
            ui.label(operation).classes('w-full')
    
    pdfWidgets = {'Text':'textarea','Table':'table','Link':'link','Image':'image','Line Break':'line_break'}
    with ui.row().classes('w-full gap-1'):
        with ui.card().classes('w-full').style('background-color: rgba(255,255,255,0.9); backdrop-filter: blur(0.5px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
            with ui.grid(columns='10% 10% 8% 30% 10% 15%').classes('w-full gap-2'):
                ui.button('Back',color='#00fff2',on_click=lambda:ui.navigate.to('/'),icon='arrow_back')
                ui.space().classes('w-full')
                ui.label('Widgets').classes('font-bold').props('dense').style('font-family:"Times New Roman";font-size:26px;font-weight:bold;')
                with ui.dropdown_button('Select Widget',auto_close=True):
                    ui.item('Text',on_click=lambda:add('Text')).classes('w-full')
                    ui.item('Table',on_click=lambda:add('Table')).classes('w-full')
                    ui.item('Link',on_click=lambda:add('Link')).classes('w-full')
                    ui.item('Image',on_click=lambda:add('Image')).classes('w-full')
                    ui.item('Line Break',on_click=lambda:add('Line Break')).classes('w-full')
                ui.space().classes('w-full')
                ui.button('Generate PDF',on_click=generatePDF).classes('w-full')
        with ui.grid(columns='30% 70%').classes('gap-1 w-full'):
            widgetsSaved = ui.card().classes('w-full h-screen overflow-auto').style('background-color: rgba(255,255,255,0.9); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);')
            with widgetsSaved:
                text = ui.textarea(placeholder='Enter your Text here')
            with ui.card().classes('w-full h-screen overflow-auto').style('background-color: rgba(1,1,1,0.6); backdrop-filter: blur(0.5px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
                pdfViewer = ui.html('',sanitize=False).classes('w-full h-full')

@ui.page('/')
def home():
    def addPdfs():
        with pdfsHolder:
            ui.card().classes('w-full h-30').style('border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);')
    with ui.card().classes('w-full'):
        ui.button('New PDF',on_click=addPdfs)
    with ui.card().classes('w-full h-screen'):
        pdfsHolder = ui.grid(columns=3).classes('w-full overflow-auto')
        with pdfsHolder:
            ui.card().classes('w-full h-30').style('border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);')

app.add_static_files('/static','Data')
app.add_static_files('/pdfs','pdfs')
ui.run(port=8085,)