from nicegui import ui, app

app.add_static_files('/pdfs', 'pdfs')

with ui.column().classes('w-full h-screen'):
    ui.label('PDF Viewer').classes('text-h5')

    ui.html('''
        <iframe
            src="/pdfs/output.pdf"
            style="width:100%; height:100%; border:none;">
        </iframe>
    ''',sanitize=False).classes('w-full h-full')

ui.run(port=8085)