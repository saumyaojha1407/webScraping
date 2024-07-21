from uvicorn import run

from scrapingTool import create_app

app = create_app()

run(app, port=6102, host='127.0.0.1')
