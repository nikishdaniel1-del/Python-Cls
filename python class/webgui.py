from nicegui import ui,app
from fpdf import FPDF
import time,aiomysql

poolConnection = None
async def makeConnection():
    global poolConnection
    poolConnection = await aiomysql.create_pool(host='localhost',user='root',password='Nikish@2003',db='pdfUsers',autocommit=True)
    
@ui.page('/Study')
def study():
    with ui.card().classes('overflow-auto h-screen'):
        ui.label('Main Page').classes('font-bold')
        backButton = ui.button('Back',color='#00fff2',on_click=lambda:ui.navigate.to('/'),icon='arrow_back')
        ui.textarea('Address',placeholder='Enter your Address').props('clearable')
        ui.color_input('Pick a Color',placeholder='Picked Color',on_change=lambda x:backButton.props(f'style="background-color: {x.value}"'))
        circular = ui.circular_progress(max=5)
        def updater():
            if circular.value==5:circular.value = -1
            circular.value += 1
        ui.slide_item('Daniel')
        ui.date()
        ui.editor()
        ui.rating(icon='star',size='lg')
        ui.button('Update',on_click=updater)
        ui.code('''name = 'Nikish Daniel'\nprint('Hello Python')''')

@ui.page('/Main')
def main():
    ui.add_css('''body {background-image:url("/static/Original.webp");background-size: cover;background-position: center;background-attachment: fixed;}''')
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
            ui.label(operation).classes('w-full h-full')
    pdfWidgets = ['Text','Table','Link','Image','Line Break']
    with ui.row().classes('w-full gap-1'):
        with ui.card().classes('w-full').style('background-color: rgba(255,255,255,0.9); backdrop-filter: blur(0.5px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
            with ui.grid(columns='10% 10% 8% 30% 10% 15%').classes('w-full gap-2'):
                ui.button('Back',color='#00fff2',on_click=lambda:ui.navigate.to('/'),icon='arrow_back')
                ui.space().classes('w-full')
                ui.label('Widgets').classes('font-bold').props('dense').style('font-family:"Times New Roman";font-size:26px;font-weight:bold;')
                ui.select(label='Select Widget',options=pdfWidgets,clearable=True,on_change=lambda x:add(x.value)).props('dense')
                ui.space().classes('w-full')
                ui.button('Generate PDF',on_click=generatePDF).classes('w-full')
        with ui.grid(columns='30% 70%').classes('gap-1 w-full'):
            widgetsSaved = ui.card().classes('w-full h-screen overflow-auto').style('background-color: rgba(255,255,255,0.9); backdrop-filter: blur(1px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);')
            with widgetsSaved:
                text = ui.textarea(placeholder='Enter your Text here')
                ui.button('Fetch',on_click=lambda:print(text.value))
            with ui.card().classes('w-full h-screen overflow-auto').style('background-color: rgba(1,1,1,0.6); backdrop-filter: blur(0.5px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
                pdfViewer = ui.html('',sanitize=False).classes('w-full h-full')

@ui.page('/{email}/MyPDFs')
def usersPdf(email):
    ui.add_css('''body {background-image:url("/static/Original.webp");background-size: cover;background-position: center;background-attachment: fixed;}''')
    ui.label(email)

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
                    ui.timer(2,lambda:ui.navigate.to(f'/{currentEmail}/MyPDFs'),immediate=False)
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