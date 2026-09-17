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
    ui.add_css('''body {background-image:url("/static/foggy-forest-landscape-dark-silhouette-mysterious-atmosphere-generated-by-ai.avif");background-size: cover;background-position: center;background-attachment: fixed;}
               .my-fab .q-btn {width: 28px !important;height: 28px !important;min-width: 28px !important;min-height: 28px !important;display: flex !important;align-items: center !important;justify-content: center !important;}
               .my-fab .q-icon {font-size: 16px !important;}
               .hover-card {transition: all 0.3s ease;}
               .hover-card:hover {transform: scale(1.03);box-shadow: 0 10px 25px rgba(0,0,0,0.2);}''')
    def addPdfs():
        with pdfsHolder:
            currentPDF = ui.card().classes('w-full h-full hover-card object-cover aspect-rectangle').style('border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);')
            with currentPDF:
                with ui.grid(columns=2):
                    pdfName = ui.input('PDF Name',value=pdfsHolder.index)
                    pdfName.disable()
                    with ui.fab('more_vert',direction='left').classes('ml-auto my-fab'):
                        with ui.fab_action(icon='delete',on_click=lambda:currentPDF.delete(),auto_close=False):ui.tooltip('Delete')
                        with ui.fab_action(icon='edit',on_click=lambda:[saveFab.set_visibility(True),pdfName.enable(),pdfDescription.enable()],auto_close=False):ui.tooltip('Edit')
                        saveFab = ui.fab_action(icon='save',on_click=lambda:[saveFab.set_visibility(False),pdfName.disable(),pdfDescription.disable()],auto_close=False)
                        saveFab.set_visibility(False)
                        with saveFab:ui.tooltip('Save')
                pdfDescription = ui.input('PDF Description',value=pdfsHolder.index)
                pdfDescription.disable()
                pdfsHolder.index += 1
    ui.button('New PDF',on_click=addPdfs)
    with ui.card().classes('p-4 w-full h-screen overflow-auto').style('background-color: rgba(1, 1, 1, 0.3); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
        pdfsHolder = ui.grid(columns=3).classes('w-full gap-2 items-start')
        pdfsHolder.index = 0
        addPdfs()

app.add_static_files('/static','Data')
app.add_static_files('/pdfs','pdfs')
ui.run(port=8085,)