from nicegui import ui,app
from fpdf import FPDF
import time

@ui.page('/')
def main():
    ui.add_css('''body {background-image:url("/static/Original.webp");background-size: cover;background-position:top center;}''')
    def pdfProperties():
        with ui.dialog() as propertiesDialog,ui.card().classes('w-1/2 h-3/4'):
            with ui.row().classes('w-full items-center justify-between gap-2 flex-wrap'):
                ui.label('PDF Properties').classes('font-bold').style('font-family:"Times New Roman";font-size:26px;font-weight:bold;')
                ui.button('',icon='save',color='green')
            for i in ['Author','Creator',"Creator's Password","User's Password"]:
                ui.input(label=i,placeholder=f"Enter PDF's {i}").classes('w-full')
        propertiesDialog.open()

    def generatePDF():
        pdfPath = "pdfs/output.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for i in widgetsSaved:
            widgetType = i.type
            if widgetType=='Text':pdf.multi_cell(0, 8, str(i.value))
            elif widgetType=='Link':pdf.write(8, str(i.value), i.value)
            elif widgetType=='Input':pdf.ln(int(i.value))
        pdf.output(pdfPath)
        pdfViewer.set_content(f'''<iframe src="/pdfs/output.pdf?v={time.time_ns()}" style=" width: 100%; height: 100%; border: none; "> </iframe>''')

    def add(operation):
        with widgetsSaved:
            if operation=='Text':widget = ui.textarea(label=operation,placeholder='Enter text here').classes('w-full')
            elif operation=='Link':
                with ui.card() as widget:
                    ui.input(label='Link Text',placeholder='Enter the Link Text').classes('w-full')
                    ui.input(label='Link URL',placeholder='Enter link here').classes('w-full')
            else:widget = ui.input(label=operation,placeholder=f'Enter {operation} here',value='0').classes('w-full')
            widget.type = operation

    def uploadImage(e):
        try:
            image_data = e.file.read()
            print(image_data)
        except Exception as error:ui.notify(f"Error reading image: {error}", color='negative'); return

    pdfWidgets = ['Text','Table','Link','Image','Line Break']
    with ui.row().classes('w-full gap-1'):
        with ui.card().classes('w-full').style('background-color: rgba(255,255,255,0.9); backdrop-filter: blur(0.5px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
            with ui.row().classes('w-full items-center justify-between gap-2 flex-wrap'):
                ui.button('Back',color='#00fff2',on_click=lambda:ui.navigate.to('/'),icon='arrow_back')
                with ui.row().classes('w-1/2 flex-wrap'):
                    ui.label('Widgets').classes('font-bold').props('dense').style('font-family:"Times New Roman";font-size:26px;font-weight:bold;')
                    with ui.dropdown_button('Select Widget',auto_close=True).classes('w-3/4'):
                        for i in pdfWidgets:
                            ui.item(i,on_click=lambda widget=i: add(widget)).classes('w-full')
                ui.button('Generate PDF',on_click=generatePDF)
                ui.button('Properties',on_click=pdfProperties)
        with ui.grid(columns='30% 70%').classes('gap-1 w-full'):
            widgetsSaved = ui.card().classes('w-full h-screen overflow-auto').style('background-color: rgba(255,255,255,0.9); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);')
            with ui.card().classes('w-full h-screen overflow-auto').style('background-color: rgba(1,1,1,0.6); backdrop-filter: blur(0.5px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
                pdfViewer = ui.html('',sanitize=False).classes('w-full h-full')

app.add_static_files('/static','Data')
app.add_static_files('/pdfs','pdfs')
ui.run(port=8085,title='PDF Generator')