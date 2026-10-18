from nicegui import ui
import asyncio
import time

@ui.page('/')
def main():
    ui.label('Sync vs Async in NiceGUI').classes('text-2xl font-bold')
    status = ui.label('Click a button to start')
    def sync_task():
        status.set_text('Sync task running...')
        time.sleep(10)
        status.set_text('Sync task completed!')

    async def async_task():
        status.set_text('Async task running...')
        await asyncio.sleep(10)
        status.set_text('Async task completed!')
    ui.button('Run Sync Task', on_click=sync_task)
    ui.button('Run Async Task', on_click=async_task)

ui.run()