from nicegui import ui,app,run
from fpdf import FPDF
from os import path,environ,mkdir,remove
import time,aiomysql,shutil,json,pandas as pd

poolConnection = None
# function that makes the startup
async def makeConnection():
    global poolConnection
    poolConnection = await aiomysql.create_pool(host='localhost',user='root',password='Nikish@2003',db='pdfUsers',autocommit=True)

links = {}
@ui.page('/PDFEditor')
async def main():
    email = app.storage.user['email']
    currentPdfName = app.storage.user['pdf']
    ui.add_css('''body {background-image:url("/static/Original.webp");background-size: cover;background-position: center;background-attachment: fixed;}''')
    # function that modifies the PDF's Properties
    def pdfProperties():
        with ui.dialog() as propertiesDialog,ui.card().classes('w-1/2 h-3/4'):
            with ui.row().classes('w-full items-center justify-between gap-2 flex-wrap'):
                ui.label('PDF Properties').classes('font-bold').style('font-family:"Times New Roman";font-size:26px;font-weight:bold;')
                ui.button('',icon='save',color='green',)
            ui.select(label='Orientation',options=['Portrait','Landscape'],value='Portrait').classes('w-full')
            ui.select(label='Page Format',options=['A3','A4','A5','Letter'],value='A4').classes('w-full')
            encryptionCheck = ui.checkbox(text='Make PDF Encrypted').classes('w-full')
            ui.input(label="Creator's Password",placeholder="Enter Creator's Password").classes('w-full').bind_visibility_from(encryptionCheck,'value')
            ui.input(label="User's Password",placeholder="Enter User's Password").classes('w-full').bind_visibility_from(encryptionCheck,'value')
            for i in ['Subject','Author','Creator','Producer']:
                ui.input(label=i,placeholder=f"Enter PDF's {i}",value='').classes('w-full')
        propertiesDialog.open()

    # function that generates pdf
    async def generatePDF(currentPdf='output'):
        try:
            pdf = FPDF(orientation='P',format='A4')
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)
            for currentWidget in widgetsSaved:
                widgetType = currentWidget.type
                currentInputs = currentWidget.inputs
                link,linkText,linkType = currentWidget.links
                try:
                    if widgetType=='New Page':pdf.add_page()
                    elif widgetType=='Text':
                        text,font,fontSize,fontStyle = currentInputs
                        currentText = str(text.value)
                        pdf.set_font(family=font.value,size=int(fontSize.value),style='B' if fontStyle.value=='Bold' else 'I' if fontStyle.value=='Italic' else '')
                        if link:
                            if linkType=='Add Link':
                                linkId = pdf.add_link()
                                pdf.write(10,currentText,link=linkId)
                                links[linkText] = linkId
                            else:
                                pdf.set_link(links[linkText])
                                pdf.write(10,currentText)
                        else:pdf.write(10,currentText)
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
                        pdf.set_link(links['Info'])
                        if not path.exists(currentFilePath):ui.notify(f"File '{currentFilePath}' does not exist.", color='negative');return
                        try:pdf.image(currentFilePath,w=100)
                        except Exception as error:ui.notify(f"Error adding image '{currentFilePath}': {error}", color='negative');return
                    elif widgetType=='Line Break':pdf.ln(int(currentInputs[0].value))
                except Exception as error:ui.notify(f"Error processing widget '{widgetType}': {error}", color='negative');return
            pdf.output(path.join(pdfFolderPath,f"{currentPdf}.pdf"))
            pdfViewer.set_content(f'''<iframe src="/pdfs/{currentPdf}.pdf?v={time.time_ns()}" style="width: 100%; height: 100%; border: none;"></iframe>''')
        except Exception as error:ui.notify(f"Error generating PDF: {error}", color='negative');return

    # function to add PDF Operations
    def add(operation):
        # function to remove the link wrt the checkbox
        def removeLinkName(linkText,value):
            if not value:linkText.value = ''

        # function to save the link
        def saveLinks(link,linkText,linkType):
            widgetMaster.links = [link,linkText,linkType]

        def linkMenu():
            with ui.dialog() as linkDialog,ui.card().classes('w-1/2'):
                link = ui.checkbox('Make it as a Link')
                linkText = ui.input(label='Link Text',placeholder='Enter the Link Text').classes('w-full').bind_enabled_from(link,'value')
                link.on_value_change(lambda x:removeLinkName(linkText,x.value))
                linkType = ui.select(options=['Add Link','Set Link'],value='Add Link',label='Link Type').classes('w-full').bind_enabled_from(link,'value')
                ui.button(text='Save',icon='save',color='green',on_click=lambda:[saveLinks(link.value,linkText.value,linkType.value),linkDialog.close()]).classes('w-full')
            linkDialog.open()

        with widgetsSaved:
            with ui.card().classes('w-full items-center gap-1 hover-card').style('background-color: rgba(255,255,255,0.9); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);') as widgetMaster:
                widgetMaster.inputs = []
                widgetMaster.links = ['','','']
                with ui.row().classes('w-full items-center justify-between gap-2 flex-wrap'):
                    ui.icon('drag_indicator').classes('handle cursor-grab active:cursor-grabbing')
                    ui.label(operation).classes('font-bold').style('font-family:"Algerian";font-size:25px;font-weight:bold;')
                    ui.button('',icon='delete',color='red',on_click=lambda:widgetMaster.delete())
                    if operation not in ['New Page','Line Break']:ui.button('',icon='link',on_click=linkMenu)
                with ui.expansion('Properties',icon='settings').classes('w-full'):
                    if operation=='Text':
                        with ui.tabs().classes('w-full') as textTabs:
                            textFieldTab = ui.tab('Text Field',label='Text Field').classes('w-full h-full border border-gray-400 rounded-lg')
                            textPropertiesTab = ui.tab('Text Properties',label='Text Properties').classes('w-full h-full border border-gray-400 rounded-lg')
                        with ui.tab_panels(textTabs,value=textFieldTab).classes('w-full border border-gray-400 rounded-lg'):
                            with ui.tab_panel(textFieldTab).classes('w-full border border-gray-400 rounded-lg'):
                                textWidget = ui.textarea(label=operation,placeholder='Enter text here').classes('w-full').props('outlined dense')
                            with ui.tab_panel(textPropertiesTab).classes('w-full border border-gray-400 rounded-lg'):
                                textFont = ui.select(label='Font',options=['Helvetica','Times','Courier'],value='Helvetica').classes('w-full').props('outlined dense')
                                fontSize = ui.input(label='Font Size',placeholder='Enter font size here',value='12').classes('w-full').props('outlined dense')
                                fontStyle = ui.select(label='Font Style',options=['Regular','Bold','Italic','Bold-Italic'],value='Regular').classes('w-full').props('outlined dense')
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
                            # function to fetch data from excel file
                            def fetchData():
                                df = pd.read_excel(filePath.value,sheet_name=sheetWidget.value)
                                df.dropna(how='all').dropna(axis=1,how='all')
                                df.columns = df.iloc[0]
                                widgetMaster.inputs = [df]
                                ui.notify('Data Loaded Successfully.',type='positive')
                            # function to fetch data from the json file
                            def readJson(currentFilePath):
                                pd.read_json(currentFilePath)
                            # function to fetch data from excel file
                            def readExcel(currentFilePath):
                                try:
                                    sheets = pd.ExcelFile(currentFilePath).sheet_names
                                    sheetWidget.options,sheetWidget.value = sheets,sheets[0]
                                except Exception as error:ui.notify(f'Error Loading File {error}',type='negative')
                            # function to fetch data from csv file
                            def readCsv(currentFilePath):
                                try:
                                    df = pd.read_csv(currentFilePath)
                                except Exception as error:ui.notify(f'Error Loading File {error}',type='negative')
                            # function that determines the file and it's extension
                            def fileLoader():
                                currentFilePath = filePath.value
                                file,extension = path.splitext(currentFilePath)
                                if extension=='.xlsx':excelExpansion.enable();excelExpansion.value=True;readExcel(currentFilePath)
                                elif extension=='.csv':csvExpansion.enable();csvExpansion.value=True;readCsv(currentFilePath)
                                elif extension=='.json':jsonExpansion.enable();jsonExpansion.value=True;readJson(currentFilePath)
                                else:ui.notify("This type of file can't be Uploaded.",type='warning')
                            with ui.tab_panel(tableTab).classes('w-full h-full border border-gray-400 rounded-lg'):
                                filePath = ui.input(label='Data File',placeholder='Enter the path of the data file').classes('w-full').props('outlined dense')
                                ui.button(text='Upload File',icon='refresh',on_click=fileLoader)
                                excelExpansion = ui.expansion(text='Excel File').classes('w-full')
                                excelExpansion.disable()
                                with excelExpansion:
                                    sheetWidget = ui.select(label='Select the Sheet',options=[]).classes('w-full')
                                    ui.button('Load Data',on_click=fetchData).bind_enabled_from(sheetWidget,'value')
                                csvExpansion = ui.expansion(text='CSV File').classes('w-full')
                                csvExpansion.disable()
                                with csvExpansion:
                                    ui.button('Load Data')
                                jsonExpansion = ui.expansion(text='JSON File').classes('w-full')
                                jsonExpansion.disable()
                                with jsonExpansion:
                                    ui.button('Load Data')
                            with ui.tab_panel(graphTab).classes('w-full h-full border border-gray-400 rounded-lg'):
                                chartCheck = ui.checkbox(text='Add Chart for this Table').classes('w-full')
                                ui.select(label='Select Chart Type',options=['Bar Chart','Pie Chart','Line Chart'],value='Bar Chart').classes('w-full').bind_visibility_from(chartCheck,'value')
                    elif operation=='Image':
                        filePath = ui.input(label='Image Path').classes('w-full').props('outlined dense')
                        widgetMaster.inputs.append(filePath)
                    elif operation=='Line Break':
                        inputWidget = ui.input(label=operation,placeholder=f'Enter {operation} here',value='5').classes('w-full').props('outlined dense')
                        widgetMaster.inputs.append(inputWidget)
                    widgetMaster.type = operation

    pdfWidgets = ['New Page','Text','Table','Link','Image','Line Break']
    with ui.row().classes('w-full gap-1'):
        with ui.card().classes('w-full').style('background-color: rgba(255,255,255,0.9); backdrop-filter: blur(0.5px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
            with ui.row().classes('w-full items-center justify-between gap-2 flex-wrap'):
                ui.button('Back',color='#00fff2',on_click=lambda:ui.navigate.to(f'/MyPDFs'),icon='arrow_back')
                with ui.row().classes('w-1/2 flex-wrap'):
                    ui.label('Widgets').classes('font-bold').props('dense').style('font-family:"Algerian";font-size:26px;font-weight:bold;')
                    with ui.dropdown_button('Select Widget',auto_close=True).classes('w-3/4'):
                        for i in pdfWidgets:
                            ui.item(i,on_click=lambda widget=i: add(widget)).classes('w-full')
                ui.button('Generate PDF',icon='picture_as_pdf',color='green',on_click=generatePDF)
                ui.button('Properties',icon='settings',color='red',on_click=pdfProperties)
        with ui.grid(columns='30% 70%').classes('gap-1 w-full'):
            widgetsSaved = ui.card().classes('w-full h-screen overflow-auto').style('background-color: rgba(1,1,1,0.6); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);')
            widgetsSaved.make_sortable(handle='.handle')
            with ui.card().classes('w-full h-screen overflow-auto').style('background-color: rgba(1,1,1,0.6); backdrop-filter: blur(0.5px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
                pdfViewer = ui.html('',sanitize=False).classes('w-full h-full')

@ui.page('/MyPDFs')
async def home():
    ui.add_css('''body {background-image:url("/static/foggy-forest-landscape-dark-silhouette-mysterious-atmosphere-generated-by-ai.avif");background-size: cover;background-position: center;background-attachment: fixed;}''')
    email = app.storage.user['email']
    # function to add widgets to PDF Holder
    def openPdfEditor(currentPdfName):
        app.storage.user['pdf'] = currentPdfName
        ui.navigate.to(f'/PDFEditor')

    async def addToWidget(currentPdfName,widgetPath):
        # fucntion to delete a pdf from database
        async def deletePdf(widget):
            try:
                async with poolConnection.acquire() as connection:
                    async with connection.cursor() as cursor:
                        await cursor.execute('delete from userspdf where email=%s and pdfName=%s',(email,currentPdfName,))
                        widget.delete();remove(widgetPath)
            except Exception as error:ui.notify(str(error),type='negative')

        with pdfsHolder:
            with ui.card().classes('w-full hover-card') as widget:
                ui.label(currentPdfName).classes('font-bold').style('font-family:"Arial Black";font-size:25px;font-weight:bold;')
                with ui.row().classes('w-full items-center justify-between gap-2 flex-wrap'):
                    ui.button('Delete',icon='delete',color='red',on_click=lambda:deletePdf(widget)).classes('flex-1')
                    ui.button('Editor',icon='picture_as_pdf',on_click=lambda:openPdfEditor(currentPdfName)).classes('flex-1')

    # function to create a new pdf
    async def addPdfs():
        # function to save in MySQL
        async def savePdfMysql(pdfNameValue,jsonPath):
            pdfSaveDialog.close()
            try:
                async with poolConnection.acquire() as connection:
                    async with connection.cursor() as cursor:
                        await cursor.execute('insert into userspdf(pdfname,email,widgets) values (%s,%s,%s)',(pdfNameValue,email,jsonPath))
                        await cursor.close();await addToWidget(pdfNameValue,jsonPath)
                ui.notify('Saved Successfully',type='positive')
            except Exception as error:ui.notify(str(error),type='negative')

        # function to validate the inputs and closes the dialog
        async def savePdfs():
            pdfNameValue = pdfName.value
            if pdfNameValue=='':pdfName.run_method('focus');pdfName.style('border:2px solid red');return
            else:pdfName.style('border:2px white')
            jsonPath = path.join(widgetFolder,pdfNameValue+'.json')
            currentPdfWidgets = {'Name':pdfNameValue,'Author':'','Creator':'','Producer':'','Orientation':'Portrait','Encrypted':False,'CreatorPassword':'','UserPassword':'','Widgets':[]}
            with open(jsonPath,'w') as jsonFile:json.dump(currentPdfWidgets,jsonFile)
            await savePdfMysql(pdfNameValue,jsonPath)

        with ui.dialog() as pdfSaveDialog,ui.card().classes('w-1/2'):
            pdfName = ui.input(label='PDF Name',placeholder='Enter the PDF Name').classes('w-full')
            ui.button('Save',icon='save',on_click=savePdfs,color='green').classes('w-full')
        pdfSaveDialog.open()

    ui.button('New PDF',icon='add',color='green',on_click=addPdfs)
    with ui.card().classes('p-4 w-full h-screen overflow-auto').style('background-color: rgba(1, 1, 1, 0.3); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
        pdfsHolder = ui.grid(columns=3).classes('w-full gap-2 items-start')
        data = []
        try:
            async with poolConnection.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute('select pdfname,widgets from userspdf where email=%s',(email,))
                    data = await cursor.fetchall()
                    for i in data:await addToWidget(*i)
                    await cursor.close()
        except Exception as error:ui.notify(str(error),type='negative')
    ui.pagination(min=1,max=len(data)//9+1).classes('w-full item-center justify-center').props(f'v-model="current" :max="{len(data)//9+1}" direction-links boundary-links icon-first="skip_previous" icon-last="skip_next" icon-prev="fast_rewind" icon-next="fast_forward" color="grey" active-color="black"')

@ui.page('/Register')
def register():
    ui.button('Back',color='red',on_click=lambda:ui.navigate.to('/'))
    # function to push data into mysql database
    async def pushData():
        currentEmail = email.value
        currentPassword = password.value
        if currentEmail=='' or currentPassword=='':ui.notify('Please fill in all fields',type='warning');return
        try:
            async with poolConnection.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(f"select passwords from users where email = %s limit 1",(currentEmail,))
                    existanceCheck = await cursor.fetchone()
                    if existanceCheck:ui.notify('Email already exists.',type='info',color='red');return
                    await cursor.execute(f"INSERT INTO users (email,passwords) VALUES ('{currentEmail}','{currentPassword}')")
                    ui.notify('Registered Successfully',type='positive')
        except Exception as error:ui.notify(str(error),type='negative')
    with ui.card().classes('absolute-center w-[50%] items-center').style('background-color: rgba(1, 1, 1, 0.7); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
        email = ui.input(label='Email',placeholder='Enter your Email').classes('w-full white-input').props('clearable')
        password = ui.input(label='Password',placeholder='Enter your Password',password=True,password_toggle_button=True).classes('w-full white-input').props('clearable')
        ui.button('Register',icon='person_add',on_click=pushData).classes('w-1/4')

@ui.page('/')
def home():
    # function to check in login 
    async def checkLogin():
        def login():
            app.storage.user['authenticated'] = True
            app.storage.user['email'] = currentEmail
            ui.navigate.to(f'/MyPDFs')
        currentEmail,currentPassword = email.value,password.value
        if currentEmail=='' or currentPassword=='':ui.notify('Please fill in all fields',type='warning');return
        try:
            async with poolConnection.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(f"select passwords from users where email = %s limit 1",(currentEmail,))
                    passwordCheck = await cursor.fetchone()
                    if not passwordCheck:ui.notify("Email doesn't exists.",type='info',color='red');return
                    elif currentPassword!=passwordCheck[0]:ui.notify('Invalid Password.');return
                    ui.notify('Login Successfully',type='positive')
                    ui.timer(0.6,lambda:login(),immediate=False)
        except Exception as error:ui.notify(str(error),type='negative')
    ui.add_css('''body {background-image: url("/static/mountain.webp");background-size: cover;background-position: center;background-attachment: fixed;}
               .white-input .q-field__label {color: white !important;}
               .white-input .q-field__native {color: white !important;}
               .white-input .q-field__control:before {border-bottom: 1px solid white !important;}
               .white-input .q-field__control:after {border-bottom: 2px solid white !important;}
               .white-input .q-field__append .q-icon {color: white !important;}
               .white-input .q-field__append .q-icon:hover {color: grey !important;}''',shared=True)
    ui.button('Study',on_click=lambda:ui.navigate.to('/Study'))
    with ui.card().classes('absolute-center w-[50%] items-center').style('background-color: rgba(1, 1, 1, 0.7); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
        email = ui.input(label='Email',placeholder='Enter your Email').classes('w-full white-input').props('clearable')
        password = ui.input(label='Password',placeholder='Enter your Password',password=True,password_toggle_button=True).classes('w-full white-input').props('clearable')
        with ui.row().classes('w-full flex-wrap gap-2 justify-center'):
            ui.button('Register',icon='person_add',on_click=lambda:ui.navigate.to('/Register')).classes('w-1/4 flex-1')
            ui.button('Login',icon='login',on_click=checkLogin,color="white").classes('w-1/4 flex-1')

ui.add_css('''.hover-card {transition: all 0.3s ease;}
           .hover-card:hover {transform: scale(1.02);box-shadow: 0 10px 25px rgba(0,0,0,0.2);}''',shared=True)
app.on_startup(makeConnection)
appBasePath = path.join(environ['USERPROFILE'],'PDF Creator')
if not path.exists(appBasePath):mkdir(appBasePath)
pdfFolderPath = path.join(appBasePath,'pdfs')
if not path.exists(pdfFolderPath):mkdir(pdfFolderPath)
fontFolder = path.join(appBasePath,'Fonts')
if not path.exists(fontFolder):mkdir(fontFolder)
widgetFolder = path.join(appBasePath,'widgets')
if not path.exists(widgetFolder):mkdir(widgetFolder)
app.add_static_files('/static','Data')
app.add_static_files('/pdfs',pdfFolderPath)
ui.run(port=8085,storage_secret='')