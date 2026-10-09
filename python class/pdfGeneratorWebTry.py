from nicegui import ui,app
from fpdf import FPDF
from os import environ,path,mkdir
from matplotlib.figure import Figure
import time,pandas as pd

@ui.page('/')
def main():
    ui.add_css('''body {background-image:url("/Data/mylene2401-umbrella-4692572_1920.avif");background-size: cover;background-position:top center;}''')
    def pdfProperties():
        with ui.dialog() as propertiesDialog,ui.card().classes('w-1/2 h-3/4'):
            with ui.row().classes('w-full items-center justify-between gap-2 flex-wrap'):
                ui.label('PDF Properties').classes('font-bold').style('font-family:"Times New Roman";font-size:26px;font-weight:bold;')
                ui.button('',icon='save',color='green')
            ui.select(label='Orientation',options=['Portrait','Landscape'],value='Portrait').classes('w-full')
            encryptionCheck = ui.checkbox(text='Make PDF Encrypted').classes('w-full')
            ui.input(label="Creator's Password",placeholder="Enter Creator's Password").classes('w-full').bind_visibility_from(encryptionCheck,'value')
            ui.input(label="User's Password",placeholder="Enter User's Password").classes('w-full').bind_visibility_from(encryptionCheck,'value')
            for i in ['Author','Creator','Producer']:
                ui.input(label=i,placeholder=f"Enter PDF's {i}",value='').classes('w-full')
        propertiesDialog.open()

    async def generatePDF(currentPdf='output'):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)
            for currentWidget in widgetsSaved:
                widgetType = currentWidget.type
                currentInputs = currentWidget.inputs
                try:
                    if widgetType=='Text':
                        pdf.set_font(family=currentInputs[1].value,size=int(currentInputs[2].value),style='B' if currentInputs[3].value=='Bold' else 'I' if currentInputs[3].value=='Italic' else '')
                        pdf.write(10,str(currentInputs[0].value))
                    elif widgetType=='Link':pdf.write(10,text=currentInputs[0].value,link=currentInputs[1].value)
                    elif widgetType=='Table':
                        df = currentInputs[0]
                        with pdf.table() as dataTable:
                            row = dataTable.row()
                            for column in df.columns:
                                row.cell(str(column))
                            for _, data in df.iterrows():
                                row = dataTable.row()
                                for value in data:
                                    row.cell(str(value))
                    elif widgetType=='Image':
                        currentFilePath = currentInputs[0].value
                        if not path.exists(currentFilePath):ui.notify(f"File '{currentFilePath}' does not exist.", color='negative');return
                        try:pdf.image(currentFilePath)
                        except Exception as error:ui.notify(f"Error adding image '{currentFilePath}': {error}", color='negative');return
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
                            textFont = ui.select(label='Font',options=['Helvetica','Times','Courier'],value='Helvetica').classes('w-full').props('outlined dense')
                            fontSize = ui.input(label='Font Size',placeholder='Enter font size here',value='12').classes('w-full').props('outlined dense')
                            fontStyle = ui.select(label='Font Style',options=['Regular','Bold','Italic'],value='Regular').classes('w-full').props('outlined dense')
                    widgetMaster.inputs += [textWidget,textFont,fontSize,fontStyle]
                elif operation=='Link':
                    linkTextWidget = ui.input(label='Link Text',placeholder='Enter the Link Text').classes('w-full').props('outlined dense')
                    linkUrlWidget = ui.input(label='Link URL',placeholder='Enter link here').classes('w-full').props('outlined dense')
                    widgetMaster.inputs.append(linkTextWidget);widgetMaster.inputs.append(linkUrlWidget)
                elif operation=='Table':
                    with ui.tabs().classes('w-full') as tableTabs:
                        tableTab = ui.tab('Table Tab',label='Table Tab').classes('w-full h-full border border-gray-400 rounded-lg')
                        graphTab = ui.tab('Graph Tab',label='Graph Tab').classes('w-full h-full border border-gray-400 rounded-lg')
                    with ui.tab_panels(tableTabs,value=tableTab).classes('w-full border border-gray-400 rounded-lg'):
                        def fetchData():
                            df = pd.read_excel(filePath.value,sheet_name=sheetWidget.value)
                            df.dropna(how='all').dropna(axis=1,how='all')
                            df.columns = df.iloc[0]
                            widgetMaster.inputs = [df]
                            ui.notify('Data Loaded Successfully.',type='positive')
                        def readExcel(currentFilePath):
                            try:
                                sheets = pd.ExcelFile(currentFilePath).sheet_names
                                sheetWidget.options,sheetWidget.value = sheets,sheets[0]
                            except Exception as error:ui.notify(f'Error Loading File {error}',type='negative')
                        def readcsv(currentFilePath):
                            try:
                                df = pd.read_csv(currentFilePath)
                            except Exception as error:ui.notify(f'Error Loading File {error}',type='negative')
                        def fileLoader():
                            currentFilePath = filePath.value
                            file,extension = path.splitext(currentFilePath)
                            if extension=='.xlsx':readExcel(currentFilePath)
                            elif extension=='.csv':readcsv(currentFilePath)
                            else:ui.notify("This type of file can't be Uploaded.",type='warning')
                        with ui.tab_panel(tableTab).classes('w-full h-full border border-gray-400 rounded-lg'):
                            filePath = ui.input(label='Data File',placeholder='Enter the path of the data file').classes('w-full').props('outlined dense')
                            ui.button(text='Upload File',icon='refresh',on_click=fileLoader)
                            with ui.expansion() as excelExpansion:
                                sheetWidget = ui.select(label='Select the Sheet',options=[]).classes('w-full')
                            ui.button('Load Data',on_click=fetchData).bind_enabled_from(sheetWidget,'value')
                        with ui.tab_panel(graphTab).classes('w-full h-full border border-gray-400 rounded-lg'):
                            chartCheck = ui.checkbox(text='Add Chart for this Table').classes('w-full')
                            ui.select(label='Select Chart Type',options=['Bar Chart','Pie Chart','Line Chart'],value='Bar Chart').classes('w-full').bind_visibility_from(chartCheck,'value')
                elif operation=='Image':
                    filePath = ui.input(label='Image Path').classes('w-full').props('outlined dense')
                    widgetMaster.inputs.append(filePath)
                else:
                    inputWidget = ui.input(label=operation,placeholder=f'Enter {operation} here',value='5').classes('w-full').props('outlined dense')
                    widgetMaster.inputs.append(inputWidget)
                widgetMaster.type = operation

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
app.add_static_files('/pdfs',pdfFolderPath)
app.add_static_files('/Data','Data1')
ui.run(port=8085,title='PDF Generator')