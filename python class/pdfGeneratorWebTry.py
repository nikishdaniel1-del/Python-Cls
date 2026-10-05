from nicegui import ui,app
from fpdf import FPDF
from os import environ,path,mkdir
import time

@ui.page('/')
def main():
    ui.add_css('''body {background-image:url("/Data/mylene2401-umbrella-4692572_1920.jpg");background-size: cover;background-position:top center;}''')
    def pdfProperties():
        with ui.dialog() as propertiesDialog,ui.card().classes('w-1/2 h-3/4'):
            with ui.row().classes('w-full items-center justify-between gap-2 flex-wrap'):
                ui.label('PDF Properties').classes('font-bold').style('font-family:"Times New Roman";font-size:26px;font-weight:bold;')
                ui.button('',icon='save',color='green')
            for i in ['Author','Creator',"Creator's Password","User's Password"]:
                ui.input(label=i,placeholder=f"Enter PDF's {i}",value='').classes('w-full')
            with ui.row().classes('w-full'):
                ui.checkbox('Header',on_change=lambda x:headerText.enable() if x.value else headerText.disable())
                headerText = ui.input('Header Text');headerText.disable()
            with ui.row().classes('w-full'):
                ui.checkbox('Footer',on_change=lambda x:footerText.enable() if x.value else footerText.disable())
                footerText = ui.input('Footer Text');footerText.disable()
        propertiesDialog.open()

    async def generatePDF(currentPdf='output',fontStyle='Arial',fontSize=12):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font(fontStyle, size=fontSize)
            for currentWidget in widgetsSaved:
                widgetType = currentWidget.type
                currentInputs = currentWidget.inputs
                try:
                    if widgetType=='Text':pdf.write(10,str(currentInputs[0].value))
                    elif widgetType=='Link':pdf.write(10,text=currentInputs[0].value,link=currentInputs[1].value)
                    elif widgetType=='Table':
                        with pdf.table() as table:
                            row = table.row()
                            for header in currentInputs[0].value.split(','):row.cell(header)
                            for data in currentInputs[1].value.split(';'):
                                row = table.row()
                                for currentData in data.split(','):row.cell(currentData)
                    elif widgetType=='Image':pdf.image(path.join(dataFolderPath,currentInputs[0].value),w=100,)
                    elif widgetType=='Editor':pdf.set_x(pdf.l_margin);pdf.write_html(currentInputs[0].value)
                    elif widgetType=='Line Break':pdf.ln(int(currentInputs[0].value))
                except Exception as error:ui.notify(f"Error processing widget '{widgetType}': {error}", color='negative');return
            pdf.output(path.join(pdfFolderPath,f"{currentPdf}.pdf"))
            pdfViewer.set_content(f'''<iframe src="/pdfs/{currentPdf}.pdf?v={time.time_ns()}" style="width: 100%; height: 100%; border: none;"></iframe>''')
        except Exception as error:ui.notify(f"Error generating PDF: {error}", color='negative');return

    def add(operation):
        with widgetsSaved:
            with ui.card().classes('w-full hover-card').style('background-color: rgba(255,255,255,0.9); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);') as widgetMaster:
                widgetMaster.inputs = []
                with ui.row().classes('w-full items-center justify-between gap-2 flex-wrap'):
                    ui.label(operation).classes('font-bold').style('font-family:"Ink Free";font-size:25px;font-weight:bold;')
                    ui.button('',icon='delete',color='red',on_click=lambda:widgetMaster.delete())
                if operation=='Text':
                    with ui.tabs().classes('w-full') as textTabs:
                        textFieldTab = ui.tab('Text Field',label='Text Field').classes('w-full h-full border border-gray-400 rounded-lg')
                        textFontTab = ui.tab('Text Font',label='Text Font').classes('w-full h-full border border-gray-400 rounded-lg')
                    with ui.tab_panels(textTabs,value=textFieldTab).classes('w-full border border-gray-400 rounded-lg'):
                        with ui.tab_panel(textFieldTab).classes('w-full h-full border border-gray-400 rounded-lg'):
                            textWidget = ui.textarea(label=operation,placeholder='Enter text here').classes('w-full').props('outlined dense')
                        with ui.tab_panel(textFontTab).classes('w-full h-full border border-gray-400 rounded-lg'):
                            textFont = ui.select(label='Font',options=['Arial','Times New Roman','Courier New']).classes('w-full').props('outlined dense')
                            fontSize = ui.input(label='Font Size',placeholder='Enter font size here',value='12').classes('w-full').props('outlined dense')
                            fontStyle = ui.select(label='Font Style',options=['Regular','Bold','Italic']).classes('w-full').props('outlined dense')
                    widgetMaster.inputs += [textWidget,textFont,fontSize,fontStyle]
                elif operation=='Link':
                    linkTextWidget = ui.input(label='Link Text',placeholder='Enter the Link Text').classes('w-full').props('outlined dense')
                    linkUrlWidget = ui.input(label='Link URL',placeholder='Enter link here').classes('w-full').props('outlined dense')
                    widgetMaster.inputs.append(linkTextWidget);widgetMaster.inputs.append(linkUrlWidget)
                elif operation=='Table':
                    tableHeaderWidget = ui.input(label='Table Header',placeholder='Enter table header here').classes('w-full').props('outlined dense')
                    tableDataWidget = ui.textarea(label='Table Data',placeholder='Enter table data here').classes('w-full').props('outlined dense')
                    widgetMaster.inputs.append(tableHeaderWidget);widgetMaster.inputs.append(tableDataWidget)
                elif operation=='Image':
                    async def handleUpload(e):
                        try:
                            fileName = e.file.name
                            filePath.value = fileName
                            with open(path.join(dataFolderPath,fileName), 'wb') as f:f.write(await e.file.read())
                        except Exception as error:ui.notify(f"Error reading image: {error}", color='negative'); return
                    uploader = ui.upload(on_upload=handleUpload, auto_upload=True).props('accept="image/*"').classes('hidden')
                    with ui.row().classes('w-full items-center justify-between gap-2 flex-wrap'):
                        filePath = ui.input(label='Uploaded Image').classes('w-8/10')
                        filePath.disable()
                        ui.button('',icon='upload',color='green',on_click=lambda:uploader.run_method('pickFiles'))
                    widgetMaster.inputs.append(filePath)
                elif operation=='Editor':
                    editorWidget = ui.editor().classes('w-full').props('outlined dense')
                    widgetMaster.inputs.append(editorWidget)
                else:
                    inputWidget = ui.input(label=operation,placeholder=f'Enter {operation} here',value='5').classes('w-full').props('outlined dense')
                    widgetMaster.inputs.append(inputWidget)
                widgetMaster.type = operation

    pdfWidgets = ['Text','Table','Link','Image','Line Break','Editor']
    with ui.row().classes('w-full gap-1'):
        with ui.card().classes('w-full').style('background-color: rgba(255,255,255,0.9); backdrop-filter: blur(0.5px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
            with ui.row().classes('w-full items-center justify-between gap-2 flex-wrap'):
                ui.button('Back',color='#00fff2',on_click=lambda:ui.navigate.to('/'),icon='arrow_back')
                with ui.row().classes('w-1/2 flex-wrap'):
                    ui.label('Widgets').classes('font-bold').props('dense').style('font-family:"Times New Roman";font-size:26px;font-weight:bold;')
                    with ui.dropdown_button('Select Widget',auto_close=True).classes('w-3/4'):
                        for i in pdfWidgets:
                            ui.item(i,on_click=lambda widget=i: add(widget)).classes('w-full')
                ui.button('Generate PDF',icon='picture_as_pdf',on_click=generatePDF)
                ui.button('Properties',icon='settings',color='green',on_click=pdfProperties)
        with ui.grid(columns='30% 70%').classes('gap-1 w-full'):
            widgetsSaved = ui.card().classes('w-full h-screen overflow-auto').style('background-color: rgba(1,1,1,0.6); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);')
            with ui.card().classes('w-full h-screen overflow-auto').style('background-color: rgba(1,1,1,0.6); backdrop-filter: blur(0.5px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
                pdfViewer = ui.html('',sanitize=False).classes('w-full h-full')

appBasePath = path.join(environ['USERPROFILE'],'PDF Creator')
if not path.exists(appBasePath):mkdir(appBasePath)
pdfFolderPath = path.join(appBasePath,'pdfs')
if not path.exists(pdfFolderPath):mkdir(pdfFolderPath)
dataFolderPath = path.join(appBasePath,'Data')
if not path.exists(dataFolderPath):mkdir(dataFolderPath)
app.add_static_files('/pdfs',pdfFolderPath)
app.add_static_files('/Data','Data1')
ui.run(port=8085,title='PDF Generator')