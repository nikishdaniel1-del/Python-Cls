from nicegui import ui,app,run
from fpdf import FPDF
from os import path,environ,mkdir
import time,aiomysql

poolConnection = None
async def makeConnection():
    global poolConnection
    poolConnection = await aiomysql.create_pool(host='localhost',user='root',password='Nikish@2003',db='pdfUsers',autocommit=True)

@ui.page('/{currentPdf}/PDFEditor')
def main(currentPdf):
    def pdfProperties():
        with ui.dialog() as propertiesDialog,ui.card().classes('w-1/2 h-3/4'):
            with ui.row().classes('w-full items-center justify-between gap-2 flex-wrap'):
                ui.label('PDF Properties').classes('font-bold').style('font-family:"Times New Roman";font-size:26px;font-weight:bold;')
                ui.button('',icon='save',color='green')
            for i in ['Author','Creator',"Creator's Password","User's Password"]:
                ui.input(label=i,placeholder=f"Enter PDF's {i}").classes('w-full')
        propertiesDialog.open()
    ui.add_css('''body {background-image:url("/static/Original.webp");background-size: cover;background-position: center;;background-attachment: fixed;}''')
    
    def generatePDF():
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for currentWidget in widgetsSaved:
                widgetType = currentWidget.type
                currentInputs = currentWidget.inputs
                try:
                    if widgetType=='Text':pdf.set_x(pdf.l_margin);pdf.multi_cell(0,8,str(currentInputs[0].value))
                    elif widgetType=='Link':pdf.set_x(pdf.l_margin);pdf.write(10,text=currentInputs[0].value,link=currentInputs[1].value)
                    elif widgetType=='Line Break':pdf.ln(int(currentInputs[0].value))
                except Exception as error:ui.notify(f"Error processing widget '{widgetType}': {error}", color='negative');return
            pdf.output(pdfPath)
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
                    textWidget = ui.textarea(label=operation,placeholder='Enter text here').classes('w-full').props('outlined dense')
                    widgetMaster.inputs.append(textWidget)
                elif operation=='Link':
                    linkTextWidget = ui.input(label='Link Text',placeholder='Enter the Link Text').classes('w-full').props('outlined dense')
                    linkUrlWidget = ui.input(label='Link URL',placeholder='Enter link here').classes('w-full').props('outlined dense')
                    widgetMaster.inputs.append(linkTextWidget);widgetMaster.inputs.append(linkUrlWidget)
                else:
                    inputWidget = ui.input(label=operation,placeholder=f'Enter {operation} here',value='0').classes('w-full').props('outlined dense')
                    widgetMaster.inputs.append(inputWidget)
                widgetMaster.type = operation
            
    pdfWidgets = ['Text','Table','Link','Image','Line Break']
    with ui.row().classes('w-full gap-1'):
        with ui.card().classes('w-full').style('background-color: rgba(255,255,255,0.9); backdrop-filter: blur(0.5px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
            with ui.row().classes('w-full items-center justify-between gap-2 flex-wrap'):
                ui.button('Back',color='#00fff2',on_click=lambda:ui.navigate.to('/'),icon='arrow_back').classes('w-1/5')
                with ui.row().classes('w-1/2 items-center justify-center gap-2 flex-wrap'):
                    ui.label('Widgets').classes('text-2xl md:text-4xl font-bold').style('font-family:"Times New Roman";font-size:26px;font-weight:bold;')
                    with ui.dropdown_button('Select Widget',auto_close=True):
                        # loads the pdf widgets into dropdown widget
                        for i in pdfWidgets:
                            ui.item(i,on_click=lambda widget=i: add(widget)).classes('w-full')
                ui.button('Generate',icon='picture_as_pdf',on_click=generatePDF).classes('w-1/5')
                ui.button('',color='green',icon='settings',on_click=pdfProperties).classes('w-1/18')
        with ui.grid(columns='30% 70%').classes('gap-1 w-full'):
            # container for pdf widgets of the current pdf project
            widgetsSaved = ui.card().classes('w-full h-screen overflow-auto').style('background-color: rgba(1,1,1,0.6); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);')
            with ui.card().classes('w-full h-screen overflow-auto').style('background-color: rgba(1,1,1,0.6); backdrop-filter: blur(0.5px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
                if not path.exists(pdfFolder):mkdir(pdfFolder)
                pdfPath = path.join(pdfFolder,f'{currentPdf}.pdf')
                pdfViewer = ui.html('',sanitize=False).classes('w-full h-full')
                if path.exists(pdfPath):pdfViewer.set_content(f'''<iframe src="/pdfs/{currentPdf}.pdf?v={time.time_ns()}" style="width: 100%; height: 100%; border: none;"></iframe>''')
                else:pdfViewer.set_content(f'''<div class="w-full h-full flex items-center justify-center text-white text-2xl">No PDF Found</div>''')

@ui.page('/{email}/MyPDFs')
async def home(email):
    ui.add_css('''body {background-image:url("/static/foggy-forest-landscape-dark-silhouette-mysterious-atmosphere-generated-by-ai.avif");background-size: cover;background-position: center;background-attachment: fixed;}
               .my-fab .q-btn {width: 28px !important;height: 28px !important;min-width: 28px !important;min-height: 28px !important;display: flex !important;align-items: center !important;justify-content: center !important;}
               .my-fab .q-icon {font-size: 16px !important;}''')

    def addPdfs(id=0,name='',description=''):

        async def deletePdf(widget):
            try:
                async with poolConnection.acquire() as connection:
                    async with connection.cursor() as cursor:
                        await cursor.execute('delete from userspdf where email=%s and pdfName=%s',(email,pdfName.value,))
                        widget.delete()
            except Exception as error:ui.notify(str(error),type='negative')

        async def savePdfMysql(pdfNameValue,pdfDescriptionValue):
            try:
                async with poolConnection.acquire() as connection:
                    async with connection.cursor() as cursor:
                        await cursor.execute('insert into userspdf(pdfname,pdfdescription,email) values (%s,%s,%s)',(pdfNameValue,pdfDescriptionValue,email))
                        await cursor.close()
                        ui.notify('Saved Successfully',type='positive')                 
            except Exception as error:ui.notify(str(error),type='negative')

        async def savePdfs():
            pdfNameValue,pdfDescriptionValue = pdfName.value,pdfDescription.value
            if pdfNameValue=='':pdfName.run_method('focus');pdfName.style('border:2px solid red');return
            else:pdfName.style('border:2px white')
            if pdfDescriptionValue=='':pdfDescription.run_method('focus');pdfDescription.style('border:2px solid red');return
            else:pdfDescription.style('border:2px white')
            await savePdfMysql(pdfNameValue,pdfDescriptionValue)

        with pdfsHolder:
            currentPDF = ui.card().classes('w-full h-full hover-card object-cover aspect-rectangle').style('border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);')
            with currentPDF:
                with ui.row().classes('w-full'):
                    pdfName = ui.input('PDF Name',placeholder="Enter PDF's Name",value=name,validation={'PDF Already Exists':lambda x:x not in ['sample','sample2']}).classes('w-4/7').props('rounded outlined dense')
                    with ui.button('',icon='delete',color='red',on_click=lambda:deletePdf(currentPDF)).classes('w-1/6 h-1/6'):ui.tooltip('Delete')
                    saveButton = ui.button(text='',icon='save',color='green',on_click=savePdfs).classes('w-1/6 h-1/6')
                    if id:saveButton.pdfId = id
                    with saveButton:ui.tooltip('Save')
                with ui.row().classes('w-full'):
                    pdfDescription = ui.input('PDF Description',placeholder="Enter PDF's Description",value=description).classes('w-4/7').props('rounded outlined dense')
                    ui.button('Editor',icon='picture_as_pdf',on_click=lambda:ui.navigate.to(f'/{pdfName.value}/PDFEditor')).classes('w-1/3')

    ui.button('New PDF',icon='add',on_click=addPdfs)
    with ui.card().classes('p-4 w-full h-screen overflow-auto').style('background-color: rgba(1, 1, 1, 0.3); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
        pdfsHolder = ui.grid(columns=3).classes('w-full gap-2 items-start')
        try:
            async with poolConnection.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute('select id,pdfname,pdfdescription from userspdf where email=%s',(email,))
                    data = await cursor.fetchall()
                    for i in data:addPdfs(*i)
        except Exception as error:ui.notify(str(error),type='negative')
    ui.pagination(min=1,max=len(data)//9+1).classes('w-full item-center justify-center').props(f'v-model="current" :max="{len(data)//9+1}" direction-links boundary-links icon-first="skip_previous" icon-last="skip_next" icon-prev="fast_rewind" icon-next="fast_forward" color="grey" active-color="black"')

@ui.page('/Register')
def register():
    ui.button('Back',on_click=lambda:ui.navigate.to('/'))
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
    async def checkLogin():
        currentEmail = email.value
        currentPassword = password.value
        if currentEmail=='' or currentPassword=='':ui.notify('Please fill in all fields',type='warning');return
        try:
            async with poolConnection.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(f"select passwords from users where email = %s limit 1",(currentEmail,))
                    passwordCheck = await cursor.fetchone()
                    if not passwordCheck:ui.notify("Email doesn't exists.",type='info',color='red');return
                    elif currentPassword!=passwordCheck[0]:ui.notify('Invalid Password.');return
                    ui.notify('Login Successfully',type='positive')
                    ui.timer(1,lambda:ui.navigate.to(f'/{currentEmail}/MyPDFs'),immediate=False)
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
        ui.link('Forgot Password?')

ui.add_css('''.hover-card {transition: all 0.3s ease;}
           .hover-card:hover {transform: scale(1.03);box-shadow: 0 10px 25px rgba(0,0,0,0.2);}''',shared=True)
app.on_startup(makeConnection)
pdfFolder = path.join(environ["USERPROFILE"],'pdfs')
app.add_static_files('/static','Data')
app.add_static_files('/pdfs',pdfFolder)
ui.run(port=8085,)