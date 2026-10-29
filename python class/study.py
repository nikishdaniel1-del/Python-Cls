from nicegui import ui,app

@ui.page('/account')
def account():
    ui.label(f'Welcome User {app.storage.user['email']}')

@ui.page('/')
def main():
    def login():
        app.storage.user['authenticated'] = True
        app.storage.user['email'] = currentEmail.value
        ui.navigate.to('/account')
    currentEmail = ui.input('Email')
    ui.button('Login',color='red',on_click=login)
    
ui.run(storage_secret='mEDrMxog1H3DIAbCU4m9JHBSVZzVfRN6WYbng-vw7Fk')