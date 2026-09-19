from nicegui import ui,app,run
from fpdf import FPDF
import time,aiomysql

poolConnection = None
async def makeConnection():
    global poolConnection
    poolConnection = await aiomysql.create_pool(host='localhost',user='root',password='Nikish@2003',db='pdfUsers',autocommit=True)

@ui.page('/home')
def main():
    ui.add_css('''body {background-image:url("/static/Original.webp");background-size: cover;background-position: center;;background-attachment: fixed;}''')
    def generatePDF():
        pdfPath = "pdfs/output.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0,10,text.value)
        pdf.output(pdfPath)
        pdfViewer.set_content(f'''<iframe src="/pdfs/output.pdf?v={time.time_ns()}" style=" width: 100%; height: 100%; border: none; "> </iframe>''')
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
                    # loads the pdf widgets into dropdown widget
                    for i in pdfWidgets:
                        ui.item(i,on_click=lambda:add(i)).classes('w-full')
                ui.space().classes('w-full')
                ui.button('Generate PDF',on_click=generatePDF).classes('w-full')
        with ui.grid(columns='30% 70%').classes('gap-1 w-full'):
            # container for pdf widgets of the current pdf project
            widgetsSaved = ui.card().classes('w-full h-screen overflow-auto').style('background-color: rgba(255,255,255,0.9); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);')
            with widgetsSaved:
                text = ui.textarea(placeholder='Enter your Text here')
            with ui.card().classes('w-full h-screen overflow-auto').style('background-color: rgba(1,1,1,0.6); backdrop-filter: blur(0.5px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
                pdfViewer = ui.html('',sanitize=False).classes('w-full h-full')

@ui.page('/{email}/MyPDFs')
async def home(email):
    ui.add_css('''body {background-image:url("/static/foggy-forest-landscape-dark-silhouette-mysterious-atmosphere-generated-by-ai.avif");background-size: cover;background-position: center;background-attachment: fixed;}
               .my-fab .q-btn {width: 28px !important;height: 28px !important;min-width: 28px !important;min-height: 28px !important;display: flex !important;align-items: center !important;justify-content: center !important;}
               .my-fab .q-icon {font-size: 16px !important;}
               .hover-card {transition: all 0.3s ease;}
               .hover-card:hover {transform: scale(1.03);box-shadow: 0 10px 25px rgba(0,0,0,0.2);}''')
    def addPdfs(id=0,name='',description=''):
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
            pdfName.disable();pdfDescription.disable()
            await savePdfMysql(pdfNameValue,pdfDescriptionValue)
        with pdfsHolder:
            currentPDF = ui.card().classes('w-full h-full hover-card object-cover aspect-rectangle').style('border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);')
            with currentPDF:
                with ui.grid(columns='62% 9% 9% 9%').classes('w-full'):
                    pdfName = ui.input('PDF Name',placeholder="Enter PDF's Name",value=name).classes('w-full').props('rounded outlined dense')
                    with ui.button('',icon='edit',on_click=lambda:[pdfName.enable(),pdfDescription.enable()]).classes('h-1/2'):ui.tooltip('Edit')
                    with ui.button('',icon='delete',color='red',on_click=lambda:currentPDF.delete()).classes('h-1/2'):ui.tooltip('Delete')
                    saveButton = ui.button(text='',icon='save',color='green',on_click=savePdfs).classes('h-1/2')
                    if id:saveButton.pdfId = id
                    with saveButton:ui.tooltip('Save')
                with ui.grid(columns='70% 40%'):
                    pdfDescription = ui.input('PDF Description',placeholder="Enter PDF's Description",value=description).classes('w-full').props('rounded outlined dense')
                    ui.button('Editor',icon='picture_as_pdf').classes('w-full')
    ui.button('New PDF',icon='add',on_click=addPdfs)
    with ui.card().classes('p-4 w-full h-screen overflow-auto').style('background-color: rgba(1, 1, 1, 0.3); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
        pdfsHolder = ui.grid(columns=3).classes('w-full gap-2 items-start')
        try:
            async with poolConnection.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute('select id,pdfname,pdfdescription from userspdf where email=%s',(email,))
                    for i in await cursor.fetchall():addPdfs(*i)
        except Exception as error:ui.notify(str(error),type='negative')

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
        with ui.row().classes('w-full gap-2 justify-center'):
            ui.button('Register',icon='person_add',on_click=lambda:ui.navigate.to('/Register')).classes('w-1/4')
            ui.button('Login',icon='login',on_click=checkLogin,color="white").classes('w-1/4')
        ui.link('Forgot Password?')

app.on_startup(makeConnection)
app.add_static_files('/static','Data')
app.add_static_files('/pdfs','pdfs')
ui.run(port=8085,)