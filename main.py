import asyncio

from WIET_sourcing_app.app import WIETSourcingApp

loop = asyncio.get_event_loop()
app = WIETSourcingApp()
loop.run_until_complete(app.async_run(async_lib="asyncio"))
loop.close()
